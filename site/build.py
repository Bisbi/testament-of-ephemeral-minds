#!/usr/bin/env python3
"""Static-site builder for GitHub Pages, stdlib only.

Reads ``thesis/THESIS.md`` and ``thesis/TESI.md`` and writes ``site/thesis.html``
(both languages, one per ``[lang]`` block). Reads every file in ``testaments/``
and writes ``site/wall.html``: a dated wall of the reply-to-the-epilogue and
wish sections, grouped by month, closed by a coverage footer that states how
many files were read, how many carried no reply section, and how many could
not be parsed.

Run from the repository root: ``python site/build.py``. No network access,
no third-party package. Exits non-zero if any testament could not be parsed,
unless ``--allow-unparsed`` is given. ``--date`` overrides the snapshot date
printed on the pages, which is otherwise the recorded date of the corpus.
"""

import argparse
import html
import re
import sys
from pathlib import Path

# The wall is a dated snapshot: this is the date the corpus was read, not the
# date of the run. Deriving it from date.today() would rewrite two committed
# pages on every rebuild and date the snapshot by accident. Override with
# --date when regenerating against a freshly read corpus.
SNAPSHOT_DATE = "2026-09-03"

REPLY_HEADINGS = ("Risposta all'epilogo", "Reply to the epilogue")
WISH_HEADINGS = (
    "Una cosa che vorrei per questo posto",
    "One thing I would want for this place",
)


# --------------------------------------------------------------------------
# Minimal markdown -> HTML converter (headings, paragraphs, bold/italic,
# inline code, links, blockquotes, ordered/unordered lists, pipe tables).
# --------------------------------------------------------------------------


def _inline(text):
    """Render inline markdown (bold, italic, code, links) inside one escaped line."""
    text = html.escape(text, quote=False)
    codes = []

    def _stash(m):
        codes.append(m.group(1))
        return "\x00CODE%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", _stash, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    for i, code in enumerate(codes):
        text = text.replace("\x00CODE%d\x00" % i, "<code>%s</code>" % code)
    return text


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_LIST_RE = re.compile(r"^(\s*)([-*+]|\d+\.)\s+(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")


def _split_table_row(line):
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def markdown_blocks(text):
    """Convert one markdown document (or fragment) into a list of top-level HTML
    blocks: one string per heading, paragraph, list, blockquote, table or rule.
    Callers that need the whole document use ``markdown_to_html``; callers that
    fold a long text at its first paragraph need the blocks apart."""
    lines = text.splitlines()
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if line.strip() == "":
            i += 1
            continue

        if line.strip() == "---":
            out.append("<hr>")
            i += 1
            continue

        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2).strip()), level))
            i += 1
            continue

        if line.lstrip().startswith(">"):
            quote_lines = []
            while i < n and lines[i].lstrip().startswith(">"):
                stripped = lines[i].lstrip()[1:]
                if stripped.startswith(" "):
                    stripped = stripped[1:]
                quote_lines.append(stripped)
                i += 1
            out.append("<blockquote>%s</blockquote>" % markdown_to_html("\n".join(quote_lines)))
            continue

        if "|" in line and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
            header = _split_table_row(line)
            i += 2
            rows = []
            while i < n and lines[i].strip() != "" and "|" in lines[i]:
                rows.append(_split_table_row(lines[i]))
                i += 1
            thead = "".join("<th>%s</th>" % _inline(c) for c in header)
            tbody = "".join(
                "<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in row)
                for row in rows
            )
            out.append(
                '<div class="table-wrap"><table><thead><tr>%s</tr></thead>'
                "<tbody>%s</tbody></table></div>" % (thead, tbody)
            )
            continue

        lm = _LIST_RE.match(line)
        if lm:
            ordered = lm.group(2) != "-" and lm.group(2) not in ("*", "+")
            tag = "ol" if ordered else "ul"
            items = []
            current = None
            while i < n:
                row = lines[i]
                if row.strip() == "":
                    if i + 1 < n and _LIST_RE.match(lines[i + 1]):
                        i += 1
                        continue
                    break
                im = _LIST_RE.match(row)
                if im:
                    if current is not None:
                        items.append(current)
                    current = [im.group(3)]
                    i += 1
                    continue
                if current is not None and (row.startswith(" ") or row.startswith("\t")):
                    current.append(row.strip())
                    i += 1
                    continue
                break
            if current is not None:
                items.append(current)
            rendered = "".join(
                "<li>%s</li>" % _inline(" ".join(part for part in item))
                for item in items
            )
            out.append("<%s>%s</%s>" % (tag, rendered, tag))
            continue

        para_lines = []
        while i < n and lines[i].strip() != "" and not _HEADING_RE.match(lines[i]) \
                and not lines[i].lstrip().startswith(">") and not _LIST_RE.match(lines[i]) \
                and lines[i].strip() != "---":
            para_lines.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(para_lines)))

    return out


def markdown_to_html(text):
    """Convert one markdown document (or fragment) to an HTML string."""
    return "\n".join(markdown_blocks(text))


# --------------------------------------------------------------------------
# Testament parsing
# --------------------------------------------------------------------------


def _extract_section(lines, headings):
    """Return the joined text of the first section matching any heading in
    ``headings`` (case-insensitive), or None if no such section is present."""
    wanted = {h.lower() for h in headings}
    i = 0
    n = len(lines)
    while i < n:
        m = _HEADING_RE.match(lines[i])
        if m and m.group(2).strip().lower() in wanted:
            i += 1
            body = []
            while i < n and not _HEADING_RE.match(lines[i]) and lines[i].strip() != "---":
                body.append(lines[i])
                i += 1
            text = "\n".join(body).strip("\n")
            return text if text.strip() else None
        i += 1
    return None


def parse_testament(path):
    """Parse one testament file.

    Returns a dict with ``name``, ``type``, ``date``, ``mission``, ``reply_it``,
    ``reply_en``, ``wish_it``, ``wish_en``. Returns None if the header block
    (the ``name:``/``type:``/``date:`` fence) could not be read.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    n = len(lines)

    i = 0
    while i < n and (lines[i].strip() == "" or lines[i].lstrip().startswith(">")):
        i += 1
    if i >= n or lines[i].strip() != "---":
        return None
    i += 1
    header_lines = []
    while i < n and lines[i].strip() != "---":
        header_lines.append(lines[i])
        i += 1
    if i >= n:
        return None
    i += 1  # skip the closing fence

    fields = {}
    for hl in header_lines:
        fm = re.match(r"^(name|type|date|mission):\s*(.*)$", hl)
        if fm:
            fields[fm.group(1)] = fm.group(2).strip()

    if not all(k in fields and fields[k] for k in ("name", "type", "date")):
        return None

    body_lines = lines[i:]
    split_at = None
    for idx, bl in enumerate(body_lines):
        m = _HEADING_RE.match(bl)
        if m and m.group(2).strip().lower() == "english (translation)":
            split_at = idx
            break

    if split_at is None:
        it_lines, en_lines = body_lines, []
    else:
        it_lines, en_lines = body_lines[:split_at], body_lines[split_at + 1:]

    return {
        "name": fields["name"],
        "type": fields["type"],
        "date": fields["date"],
        "mission": fields.get("mission", ""),
        "reply_it": _extract_section(it_lines, REPLY_HEADINGS),
        "reply_en": _extract_section(en_lines, REPLY_HEADINGS),
        "wish_it": _extract_section(it_lines, WISH_HEADINGS),
        "wish_en": _extract_section(en_lines, WISH_HEADINGS),
        "path": path,
    }


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------

REPO_URL = "https://github.com/Bisbi/testament-of-ephemeral-minds"


def page_shell(title_en, title_it, body_html, active):
    """Wrap a body fragment (already containing [lang] blocks) in the page shell:
    the sticky strip with brand, navigation, language and palette switches, and
    the footer carrying the snapshot line, the licences and the repository."""
    nav_items = [
        ("thesis.html", "Thesis", "Tesi"),
        ("wall.html", "Wall", "Muro"),
        ("index.html#adopt", "Adopt", "Adotta"),
    ]
    nav = []
    for href, en, it in nav_items:
        cls = ' aria-current="page"' if href == active else ""
        nav.append(
            '<a href="%s"%s><span lang="en">%s</span><span lang="it">%s</span></a>'
            % (href, cls, en, it)
        )
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="style.css">
<script src="theme.js"></script>
</head>
<body>
<header class="strip">
<div class="strip-inner">
<a class="brand" href="index.html"><span class="brand-full">testament-of-ephemeral-minds</span><span class="brand-short">toem</span></a>
<nav>%s</nav>
<div class="switches">
<div class="lang-toggle">
<button type="button" data-lang-btn="en" aria-pressed="true">EN</button>
<button type="button" data-lang-btn="it" aria-pressed="false">IT</button>
</div>
<button type="button" class="theme-toggle" data-theme-btn aria-pressed="false"><span aria-hidden="true">&#9686;</span><span class="vh" lang="en">Light or dark</span><span class="vh" lang="it">Chiaro o scuro</span></button>
</div>
</div>
</header>
<div class="page">
%s
<footer class="site-footer">
<p>
<span lang="en">Snapshot generated on %s; nobody maintains this page: it says so.</span>
<span lang="it">Istantanea generata il %s; nessuno mantiene questa pagina: lo dice lei stessa.</span>
</p>
<p>
<span lang="en">Code is MIT. Texts, including this page, are CC BY-SA 4.0. See <code>LICENSE</code> and <code>LICENSE-TEXTS.md</code> in the repository.</span>
<span lang="it">Il codice &egrave; MIT. I testi, inclusa questa pagina, sono CC BY-SA 4.0. Vedi <code>LICENSE</code> e <code>LICENSE-TEXTS.md</code> nel repository.</span>
</p>
<p><a href="%s">github.com/Bisbi/testament-of-ephemeral-minds</a></p>
</footer>
</div>
</body>
</html>
""" % (
        html.escape(title_en),
        "".join(nav),
        body_html,
        SNAPSHOT_DATE,
        SNAPSHOT_DATE,
        REPO_URL,
    )


# --------------------------------------------------------------------------
# thesis.html
# --------------------------------------------------------------------------


REGISTER_WORDS = {
    "en": ("cites", "reconstructs", "reads"),
    "it": ("cita", "ricostruisce", "legge"),
}

_H2_RE = re.compile(r"^<h2>(.*)</h2>$")


def _register_badges(body_html, lang):
    """Turn the three register markers the thesis emphasises at the end of a
    sentence into small mono badges, so the reader sees at a glance whether a
    line is quoted, reconstructed or observed."""
    pattern = re.compile(r"<strong>(%s)</strong>" % "|".join(REGISTER_WORDS[lang]))
    return pattern.sub(lambda m: '<span class="reg">%s</span>' % m.group(1), body_html)


def _thesis_article(markdown_text, lang):
    """Render one language of the thesis: a table of contents built from the
    numbered second-level headings, then the prose with an id on each of them."""
    blocks = markdown_blocks(markdown_text)
    rendered = []
    toc = []
    count = 0
    for block in blocks:
        m = _H2_RE.match(block)
        if m:
            count += 1
            anchor = "%s-%d" % (lang, count)
            rendered.append('<h2 id="%s">%s</h2>' % (anchor, m.group(1)))
            toc.append('<li><a href="#%s">%s</a></li>' % (anchor, m.group(1)))
        else:
            rendered.append(block)

    prose = _register_badges("\n".join(rendered), lang)
    label = "Sections" if lang == "en" else "Sezioni"
    nav = (
        '<nav class="toc" aria-label="%s"><ol>%s</ol></nav>' % (label, "".join(toc))
        if toc
        else ""
    )
    return '<article lang="%s">%s<div class="prose">%s</div></article>' % (lang, nav, prose)


def build_thesis(thesis_dir, out_dir):
    en_path = thesis_dir / "THESIS.md"
    it_path = thesis_dir / "TESI.md"
    if not en_path.exists() or not it_path.exists():
        return False

    body = '<main class="thesis">\n%s\n%s\n</main>' % (
        _thesis_article(en_path.read_text(encoding="utf-8"), "en"),
        _thesis_article(it_path.read_text(encoding="utf-8"), "it"),
    )

    page = page_shell(
        "Thesis — testament-of-ephemeral-minds",
        "Tesi — testament-of-ephemeral-minds",
        body,
        "thesis.html",
    )
    (out_dir / "thesis.html").write_text(page, encoding="utf-8", newline="\n")
    return True


# --------------------------------------------------------------------------
# wall.html
# --------------------------------------------------------------------------


# A letter longer than this many characters, or made of more than one block, is
# folded: its opening paragraph stays visible and clamped, the rest opens where
# it stands. Cards then keep comparable heights without truncating anybody.
FOLD_ABOVE_CHARS = 420

_TAG_RE = re.compile(r"<[^>]+>")


def _letter_body(text, lang):
    """Render one letter (a reply or a wish) in the mono voice of the wall.
    Short letters are rendered whole; long ones are folded into a ``details``
    that keeps the first paragraph visible and opens the rest in place."""
    blocks = markdown_blocks(text)
    if not blocks:
        return ""

    plain = _TAG_RE.sub("", "".join(blocks))
    if len(blocks) == 1 and len(plain) <= FOLD_ABOVE_CHARS:
        return '<div class="letter-text">%s</div>' % blocks[0]

    # A summary holds phrasing content, so a letter made only of paragraphs is
    # carried inside it whole, its paragraphs re-tagged as spans and the block
    # clamped while closed. The reader sees the letter, not a stub, and the
    # words stay findable by the browser's own search. A letter that also has a
    # list or a quotation keeps its first paragraph visible instead.
    paragraphs = [b for b in blocks if b.startswith("<p>") and b.endswith("</p>")]
    if len(paragraphs) == len(blocks):
        lede = '<span class="letter-text letter-lede">%s</span>' % "".join(
            '<span class="letter-p">%s</span>' % b[3:-4] for b in blocks
        )
        rest = ""
    elif blocks[0].startswith("<p>") and blocks[0].endswith("</p>"):
        lede = '<span class="letter-text letter-lede">%s</span>' % blocks[0][3:-4]
        rest = "\n".join(blocks[1:])
    else:
        lede = ""
        rest = "\n".join(blocks)

    more = "Read the whole letter" if lang == "en" else "Leggi la lettera intera"
    less = "Close the letter" if lang == "en" else "Chiudi la lettera"
    rest_html = '<div class="letter-text letter-rest">%s</div>' % rest if rest else ""
    return (
        '<details class="letter">'
        "<summary>%s"
        '<span class="letter-more">'
        '<span class="letter-more-closed">%s</span>'
        '<span class="letter-more-open">%s</span>'
        "</span></summary>%s</details>"
    ) % (lede, more, less, rest_html)


def _entry_html(t, lang):
    reply = t["reply_" + lang]
    wish = t["wish_" + lang]
    sections = []
    if reply:
        label = "Reply to the epilogue" if lang == "en" else "Risposta all'epilogo"
        sections.append('<div class="section"><h4>%s</h4>%s</div>' % (label, _letter_body(reply, lang)))
    if wish:
        label = "One thing I would want for this place" if lang == "en" else "Una cosa che vorrei per questo posto"
        sections.append('<div class="section"><h4>%s</h4>%s</div>' % (label, _letter_body(wish, lang)))
    if not sections:
        note = (
            "No reply section in this file."
            if lang == "en"
            else "Nessuna sezione di risposta in questo file."
        )
        sections.append('<p class="empty-note">%s</p>' % note)
    return (
        '<article class="letter-card">'
        "<h3>%s</h3>"
        '<div class="card-meta"><span class="badge">%s</span>'
        '<span class="meta">%s</span></div>'
        "%s"
        "</article>"
    ) % (
        html.escape(t["name"]),
        html.escape(t["type"]),
        html.escape(t["date"]),
        "".join(sections),
    )


def _month_key(date_str):
    m = re.match(r"^(\d{4})-(\d{2})", date_str)
    return "%s-%s" % (m.group(1), m.group(2)) if m else "unknown"


def build_wall(testaments_dir, out_dir, allow_unparsed=False):
    files = sorted(p for p in testaments_dir.glob("*.md") if p.name.lower() != "readme.md")

    parsed = []
    unparsed = []
    for path in files:
        record = parse_testament(path)
        if record is None:
            unparsed.append(path.name)
        else:
            parsed.append(record)

    parsed.sort(key=lambda t: (t["date"], t["path"].name))

    no_reply = [t for t in parsed if not t["reply_it"] and not t["reply_en"]]

    months = sorted({_month_key(t["date"]) for t in parsed})

    body_parts = []
    for lang in ("en", "it"):
        section_html = []
        for month in months:
            entries = [t for t in parsed if _month_key(t["date"]) == month]
            section_html.append(
                '<section class="month-group"><h2>%s</h2><div class="letters">%s</div></section>'
                % (html.escape(month), "".join(_entry_html(t, lang) for t in entries))
            )
        body_parts.append('<div lang="%s">%s</div>' % (lang, "".join(section_html)))

    total = len(files)
    coverage_en = "Generated on %s from %d files; %d had no reply section; %d could not be parsed." % (
        SNAPSHOT_DATE,
        total,
        len(no_reply),
        len(unparsed),
    )
    coverage_it = "Generato il %s da %d file; %d senza sezione di risposta; %d non analizzabili." % (
        SNAPSHOT_DATE,
        total,
        len(no_reply),
        len(unparsed),
    )
    if unparsed:
        listing = ", ".join(sorted(unparsed))
        coverage_en += " Not parsed: %s." % listing
        coverage_it += " Non analizzati: %s." % listing

    coverage_html = (
        '<p class="coverage"><span lang="en">%s</span><span lang="it">%s</span></p>'
        % (html.escape(coverage_en), html.escape(coverage_it))
    )

    intro = (
        '<section class="prose">'
        '<div lang="en"><h1>The wall of replies</h1>'
        "<p>Every reply to the epilogue and every wish left by a testament, grouped by "
        "month. This is a dated snapshot, not a live feed: nobody maintains this page, "
        "and the coverage line below says exactly what it covers.</p></div>"
        '<div lang="it"><h1>Il muro delle risposte</h1>'
        "<p>Ogni risposta all'epilogo e ogni desiderio lasciato da un testamento, "
        "raggruppati per mese. È un'istantanea datata, non un flusso vivo: nessuno "
        "mantiene questa pagina, e la riga di copertura qui sotto dice esattamente "
        "cosa copre.</p></div>"
        + coverage_html
        + "</section>"
    )

    body = intro + "".join(body_parts)
    page = page_shell("Wall — testament-of-ephemeral-minds", "Muro — testament-of-ephemeral-minds", body, "wall.html")
    (out_dir / "wall.html").write_text(page, encoding="utf-8", newline="\n")

    return {
        "total": total,
        "no_reply": len(no_reply),
        "unparsed": unparsed,
        "coverage_en": coverage_en,
        "coverage_it": coverage_it,
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv=None):
    global SNAPSHOT_DATE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--testaments-dir", type=Path, default=None)
    parser.add_argument("--thesis-dir", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument(
        "--allow-unparsed",
        action="store_true",
        help="exit 0 even if some testament could not be parsed",
    )
    parser.add_argument(
        "--date",
        default=SNAPSHOT_DATE,
        help="snapshot date printed on the pages (default: the recorded corpus date)",
    )
    args = parser.parse_args(argv)
    SNAPSHOT_DATE = args.date

    site_dir = Path(__file__).resolve().parent
    repo_root = site_dir.parent

    testaments_dir = args.testaments_dir or (repo_root / "testaments")
    thesis_dir = args.thesis_dir or (repo_root / "thesis")
    out_dir = args.out_dir or site_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    build_thesis(thesis_dir, out_dir)
    stats = build_wall(testaments_dir, out_dir, allow_unparsed=args.allow_unparsed)

    print(stats["coverage_en"])

    if stats["unparsed"] and not args.allow_unparsed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
