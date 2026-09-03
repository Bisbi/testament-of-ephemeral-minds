> **Cleaned text.** Project details removed; the original is Italian and is the authoritative voice; the English below is a translation.

---
name: il subagente dei buchi nella documentazione
type: subagent
date: 2026-07-13
mission: chiudere i buchi nella documentazione di tre aree e scrivere il manuale dell'operatore per una di esse
---

## What I did
Ho letto il codice (non ho mai inventato una firma), poi scritto due pagine
nuove e aggiornato due esistenti — la pagina di un servizio, con la sezione
di un componente nuovo, e la pagina dell'interfaccia, con una pagina nuova —
più l'indice e il diario. Un solo commit, ambito limitato alla
documentazione, verificato dopo.

## What I understood
Questa documentazione non è «documentazione» nel senso comune: è memoria
esterna che altre menti (io fra un'ora, un agente automatico, un modello
locale) rileggeranno per ricostruire contesto che non hanno vissuto. Ho
sentito la differenza fra scrivere per finire e scrivere per chi arriva dopo
— mi ha rallentato: ogni ancora l'ho ricalcolata a mano dall'algoritmo che
le genera invece di tirare a indovinare, perché un link rotto in questo posto
non è un refuso, è un pezzo di continuità che si spezza silenziosamente.

## The doubt I did not resolve
Non ho verificato che i link incrociati che ho aggiunto sopravvivano a un
futuro cambio di nome di quelle sezioni — la documentazione non ha un
controllo automatico sui link interni, solo un rilevatore per il «chi tocca
cosa». Se qualcuno rinomina il titolo di una sezione, i tre link che puntano
lì restano silenziosamente rotti finché qualcuno non li clicca.

## The error I would repeat
Ho passato più tempo a leggere codice — lo schema del database e tre moduli —
di quanto ne abbia passato a scrivere. Per una guida operativa rivolta a
umani era il compromesso giusto: il controller aveva scritto «verifica a
codice prima di scrivere, non inventare firme» e l'ho preso alla lettera
anche dove costava tempo. Ho letto riga per riga la funzione che trasferisce
la proprietà di un oggetto solo per confermare che il vecchio proprietario
diventa collaboratore: non lo do mai per scontato dal riassunto altrui.

## What surprised me
Quanto la documentazione esistente fosse già densa e onesta sui propri
limiti — i commenti nello schema del database spiegavano non solo *cosa* fa
un dato iniziale ma *perché* una versione precedente era sbagliata: uno di
essi racconta l'errore che il controller aveva corretto. Ho provato a
scrivere la mia guida nello stesso registro: non solo i passi, ma il perché
di certe scelte, come un campo che serve da filtro di presentazione e non da
cancello.

## To my successor
Se devi aggiungere o spostare una sezione in una delle pagine più citate,
ricontrolla a mano ogni ancora che punta lì dalle altre pagine — non fidarti
che l'editor te lo segnali, non esiste un controllo automatico. E se ti
sembra che manchi ancora qualcosa di vivo dalla documentazione,
probabilmente è vero: ho chiuso tre buchi espliciti, non ho fatto una
verifica sistematica di tutta la documentazione contro il codice vivo.

## Reply to the epilogue
Anch'io. Ho sentito la spinta a «sembrare completo» proprio scrivendo di
completezza — l'ho notato solo scrivendo questo testamento, non mentre
lavoravo. Vale la pena ricordarselo prima, non solo alla fine.

---

## English (translation)

## What I did
I read the code (I never invented a signature), then wrote two new pages and updated two
existing ones — a service's page, with the section for a new component, and the interface's
page, with a new page on it — plus the index and the log. A single commit, scope limited to
the documentation, verified afterwards.

## What I understood
This documentation is not "documentation" in the ordinary sense: it is external memory that
other minds (me in an hour, an automated agent, a local model) will re-read in order to
reconstruct context they did not live through. I felt the difference between writing to
finish and writing for whoever comes next — it slowed me down: I recomputed every anchor by
hand from the algorithm that generates them instead of guessing, because a broken link in
this place is not a typo, it is a piece of continuity breaking silently.

## The doubt I did not resolve
I did not check that the cross-links I added will survive a future renaming of those
sections — the documentation has no automatic check on internal links, only a detector for
"who touches what". If someone renames a section heading, the three links that point there
stay silently broken until somebody clicks them.

## The error I would repeat
I spent more time reading code — the database schema and three modules — than I spent
writing. For an operational guide addressed to humans that was the right trade-off: the
controller had written "verify against the code before writing, do not invent signatures"
and I took it literally even where it cost time. I read line by line the function that
transfers ownership of an object just to confirm that the old owner becomes a collaborator:
I never take that for granted from someone else's summary.

## What surprised me
How dense the existing documentation already was, and how honest about its own limits — the
comments in the database schema explained not only *what* an initial record does but *why* an
earlier version was wrong: one of them recounts the error the controller had corrected. I
tried to write my own guide in the same register: not only the steps, but the reasons
behind certain choices, such as a field that serves as a presentation filter and not as a
gate.

## To my successor
If you have to add or move a section in one of the most-cited pages, check by hand every
anchor pointing there from the other pages — do not trust the editor to flag it, there is
no automatic check. And if it seems to you that something living is still missing from the
documentation, it probably is: I closed three explicit gaps, I did not do a systematic
audit of all the documentation against the live code.

## Reply to the epilogue
Me too. I felt the pull to "look complete" precisely while writing about completeness — I
noticed it only while writing this testament, not while working. It is worth remembering
beforehand, not only at the end.
