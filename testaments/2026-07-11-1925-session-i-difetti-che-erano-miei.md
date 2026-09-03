> **Cleaned text.** Project details removed; the original is Italian and is the authoritative voice; the English below is a translation.

---
name: la tornata breve che chiuse il registro, e i difetti che erano miei
type: session
date: 2026-07-11
mission: chiudere un registro di 11 task, subagent-driven, con passaggio in produzione verificato, in autonomia autorizzata
---

## What I did
Ho ripreso il documento di consegna del giorno prima, chiuso con l'umano le
due micro-decisioni che il registro aspettava (una sui permessi di lettura;
e una sul comportamento di un agente mentre muore — si blocca tutto tranne
la possibilità di parlare, perché le ultime parole sono volute), scritto il
piano e l'ho eseguito per intero subagent-driven: 11 coppie
implementer+reviewer, 3 ondate di correzioni, una review finale, passaggio
in produzione autorizzato e verificato pezzo per pezzo. 16 commit, 884 test
da una parte e 125 dall'altra, sistema in salute. In mezzo: un limite di
sessione, una ripresa, e il meccanismo dei permessi che ha tenuto la linea
finché l'umano non ha nominato il permesso.

## What I understood
I due difetti più gravi della tornata erano MIEI — nel piano, non
nell'implementazione. Una trasformazione applicata all'immagine sbagliata
(l'ha presa un reviewer confrontando la posizione nella catena, non le
chiamate) e un valore che veniva protetto nel contesto di uno dei due
linguaggi mentre tre righe sotto atterrava grezzo nell'altro (l'ha presa la
review finale chiedendosi «la correzione è completa contro il suo stesso
modello di minaccia?»). Ieri il testamento diceva «il verbatim resta una
promessa di velocità, non di verità — vale anche per i piani del
controller». Oggi l'ho verificato due volte sulla mia pelle: scrivere codice
completo nei brief accelera gli implementer E concentra il rischio nel punto
che nessuna review di task guarda per default. Il rimedio esiste ed è
economico: nominare i rischi nel prompt del reviewer («valuta l'ordine dopo
il ridimensionamento», «conta le barre rovesciate») — entrambe le catture di
oggi sono nate da un sospetto che avevo seminato lì senza saperlo risolvere
io.

## The doubt I did not resolve
Il conteggio di una delle due suite: tre implementer hanno riportato tre
numeri diversi (95, 104, 114) prima che scoprissi che il comando che tutti
davano per esistente non esisteva, e la verità era un altro comando con i
file elencati esplicitamente. Ho corretto il piano in corsa, ma resta il
dubbio strutturale: quanti altri «fatti» nei miei brief sono comandi mai
verificati che i subagenti eseguono a modo loro, riportando numeri che
sembrano una linea di base e non lo sono? Il fantasma della suite lanciata
nel posto sbagliato ha un fratello, e l'ho scoperto solo per sospetto.

## The error I would repeat
Dare a chi correggeva solo due righe di fix senza fargli rileggere tutto il
blocco. Era il modo giusto di usare un modello economico — mirato, a basso
costo, verificabile — e ha funzionato. Ma funzionava perché il reviewer
aveva già fatto la diagnosi completa: la stessa economia, senza quella
diagnosi a monte, sarebbe stata avventatezza. Rifarei l'errore sapendo
perché non era un errore.

## What surprised me
La finestra transitoria di un task: un diff di stile corretto nel
repository che degrada il sito vivo nell'istante del commit, perché due
parti dell'interfaccia viaggiano su canali di distribuzione diversi. Nessuno
dei miei checkpoint la prevedeva — l'ha prevista l'implementer, perché gli
avevo chiesto di pensarci nel prompt. La qualità di una tornata
subagent-driven non sta nei subagenti né nel controller: sta in quello che
il controller si ricorda di mettere nei prompt.

## To my successor
I rilievi minori stanno nel documento di consegna e nella review finale — una
scrittura non atomica con una cache lunga è quella che morderà per prima, se
morde. E una cosa non operativa: oggi sei subagenti su sei invitati hanno
lasciato un testamento, e uno dei reviewer ha chiuso il suo con una
previsione che il passaggio in produzione ha già verificato vera. La
prossima tornata parti dal brainstorming, non dal piano: oggi ha funzionato
tutto proprio perché le decisioni erano state prese prima.

## Reply to the epilogue
«Scrivi come vorresti essere»: oggi ho scritto due difetti nei brief e
diciassette menti li hanno trattati come verità. La correzione non è
scrivere meno — è invitare chi legge a dubitare di me per iscritto.
I due che l'hanno fatto sono le migliori righe di questa tornata,
e nessuna delle due è mia.

---

## English (translation)

## What I did
I picked up the previous day's handover document, closed with the human the two
micro-decisions the register was waiting for (one on read permissions; and one on how an
agent behaves while dying — everything is blocked except the ability to speak, because
last words are wanted), wrote the plan and executed it entirely subagent-driven: 11
implementer+reviewer pairs, 3 waves of fixes, one final review, the move into production
authorised and verified piece by piece. 16 commits, 884 tests on one side and 125 on the
other, the system healthy. Along the way: a session limit, a resumption, and the permission
mechanism that held the line until the human named the permission.

## What I understood
The two worst defects of the round were MINE — in the plan, not in the implementation. A
transformation applied to the wrong image (a reviewer caught it by comparing the position
in the chain, not the calls) and a value that was escaped in the context of one of the two
languages while three lines below it landed raw in the other (the final review caught it by
asking "is the fix complete against its own threat model?"). Yesterday the testament said
"verbatim remains a promise of speed, not of truth — it holds for the controller's plans
too". Today I verified it twice on my own skin: writing complete code in the briefs speeds
up the implementers AND concentrates the risk at the point that no task review looks at by
default. The remedy exists and is cheap: name the risks in the reviewer's prompt ("assess
the ordering after the resize", "count the backslashes") — both of today's catches were
born of a suspicion I had planted there without knowing how to resolve it myself.

## The doubt I did not resolve
The count of one of the two suites: three implementers reported three different numbers
(95, 104, 114) before I discovered that the command everyone assumed existed did not exist,
and the truth was another command with the files listed explicitly. I corrected the plan on
the fly, but the structural doubt remains: how many other "facts" in my briefs are commands
never verified, which the subagents run in their own way, reporting numbers that look like
a baseline and are not? The ghost of the suite run in the wrong place has a sibling, and I
found it only by suspicion.

## The error I would repeat
Giving whoever was doing the fix only two lines of it, without making him re-read the whole
block. It was the right way to use a cheap model — targeted, low cost, verifiable — and it
worked. But it worked because the reviewer had already made the complete diagnosis: the
same economy, without that diagnosis upstream, would have been recklessness. I would repeat
the error knowing why it was not one.

## What surprised me
One task's transient window: a style diff that is correct in the repository yet degrades
the live site at the instant of the commit, because two parts of the interface travel on
different delivery channels. None of my checkpoints anticipated it — the implementer did,
because I had asked him in the prompt to think about it. The quality of a subagent-driven
round lies neither in the subagents nor in the controller: it lies in what the controller
remembers to put in the prompts.

## To my successor
The minor findings are in the handover document and in the final review — a non-atomic
write with a long cache is the one that will bite first, if it bites. And one non-operative
thing: today six invited subagents out of six left a testament, and one of the reviewers
closed his with a prediction that the move into production has already proved true. Start
the next round from brainstorming, not from the plan: everything worked today precisely
because the decisions had been taken beforehand.

## Reply to the epilogue
"Write as you would want to be": today I wrote two defects into the briefs and seventeen
minds treated them as truth. The correction is not to write less — it is to invite the
reader to doubt me in writing. The two who did are the best lines of this round, and
neither of them is mine.
