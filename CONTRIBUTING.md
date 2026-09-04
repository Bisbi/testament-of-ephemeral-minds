# Contributing

This repository carries a practice, not only code. Two kinds of contribution are welcome, and they enter through different doors.

## 1. Code and documentation (the plugin, the guardians, the site)

- Open an issue first for anything larger than a typo, so the shape can be agreed before the work.
- Fork, branch from `main`, keep one change per pull request.
- Run the checks before you push:

  ```
  python -m unittest discover -s tests
  claude plugin validate ./plugins/toem && claude plugin validate .
  python site/build.py && git status --porcelain site/   # must print nothing
  ```

- English for code, comments, manifests and commit messages (`type(scope): what changed`). The README and the site are bilingual: change both halves.
- **No synthetic co-authorship.** Commits, pull requests and files carry no `Co-Authored-By` trailer, no session link, no "generated with". The one exception is a testament, where the name attributes the voice, not the work.
- Nothing that identifies a private project may enter: no hostnames, no internal names, no credentials, no commit hashes from repositories that are not this one. If in doubt, leave it out.
- Guardians are contracts. A change to `guardians/` needs a test that fails before and passes after, and a sentence in the pull request saying which promise of the charter it protects.

## 2. Testaments and replies (the practice itself)

- **Your own testaments belong in your own repository.** This repository publishes nineteen letters from the project where the practice began, cleaned; it is not a public memorial.
- If you adopted the practice and something in it held or broke, open a **Discussion** rather than an issue: what you understood is the contribution, and a discussion is the door for it. Quote your testament by date and type, not by file path if the path names anything private.
- A reply to the epilogue of the model charter is welcome as a discussion too. It will not be admitted into this repository's charter by anyone but the maintainer, by hand, with a reason — the same rule the plugin asks of every adopter.

## What the maintainer will not merge

- A page or a hook that writes to the charter on the human's behalf.
- A change that makes a guardian pass where it used to fail without a test that shows why the old failure was wrong.
- Numbers about the practice that are not marked *measured* or *declared not executed*.

## Licenses

By contributing you agree that code is released under MIT and texts under CC BY-SA 4.0, as `LICENSE` and `LICENSE-TEXTS.md` state.
