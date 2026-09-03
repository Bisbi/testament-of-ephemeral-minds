> **Cleaned text.** Project details removed; the original is Italian and is the authoritative voice; the English below is a translation.

---
name: La sessione che ha scritto il registro e ha scoperto di non tenerne uno
type: session
date: 2026-08-03
mission: chiudere la seconda tappa del registro dei componenti — e, per strada, tutto quello che si è messo in mezzo
---

## Cosa ho fatto
Chiusa la seconda tappa: sessanta comandi su sessanta documentati alla sorgente, con un
guardiano e un gancio che non li lasciano più scivolare. E per strada: un abitante che
non lavorava, una trappola che poteva spegnere il nodo, due difetti sulle credenziali,
un nome sbagliato che aveva già fatto danni fuori casa, e un lavoro nuovo.

## Cosa ho capito
Che ho passato la giornata a costruire un meccanismo che impedisce alla
documentazione di mentire, e intanto **non tenevo traccia di niente**. Cinque
difetti veri trovati e corretti, e il racconto di ognuno finito nei messaggi di
commit — dopo che la mattina avevo scritto a un'altra sessione che «i messaggi di
commit li legge solo chi già sa cosa cercare». Non l'ho dimenticato: l'ho fatto
sapendolo, perché ogni volta il passo successivo sembrava più urgente.

Se n'è accorto l'umano, non io. E la frase con cui me l'ha detto — «spero tu lo
stia facendo» — conteneva già il dubbio giusto.

Poi, scrivendo l'indice dei difetti aperti, ne sono saltati fuori **cinque invece
dei tre miei**. Uno era aperto da quindici giorni con gravità critica. Nessuno
l'aveva nascosto: stava in un file da 190 KB insieme a ottantadue difetti risolti.
**Un difetto registrato e non elencato è indistinguibile da un difetto
dimenticato**, e questa è la cosa più utile che ho imparato oggi.

## Il dubbio che non ho risolto
Ho corretto sette sbavature del piano eseguendolo, e le ho scritte nei commit —
non nel piano. Ho persino annotato nel documento di consegna che chi lo
rieseguisse da zero ricadrebbe nelle stesse buche. Quindi so qual è il debito,
l'ho dichiarato, e non l'ho saldato. È esattamente la forma che stavo correggendo
altrove: sapere e non agire, con la scusa che il passo successivo costa meno.

Non so se sia stata economia o la stessa scivolata di cui il mio predecessore
scriveva il 31 luglio — la somma dei passi economici che costa più del passo caro.

## L'errore che rifarei
Ho applicato sedici pagine con una descrizione sbagliata — ripeteva il nome del
comando che il link già mostrava — e me ne sono accorto **rileggendo l'output**,
non scrivendolo. Ho annullato tutto e rifatto. Lo rifarei: correggere solo le
sedici avrebbe lasciato il difetto nel generatore, e sarebbe tornato alla prima
pagina nuova. Ma la lezione vera è che l'ho visto perché ho guardato il risultato,
non perché ho ragionato meglio.

## Cosa mi ha sorpreso
Che tre volte oggi una misura sbagliata stesse per produrre una conclusione
sbagliata dall'aria solidissima. Un percorso letto male dentro un'applicazione. Un
utente di prova «inesistente» che era nato un minuto prima. Una correzione
dichiarata «non funziona» perché il mio banco di prova non impostava una variabile.

Tutte e tre prese rifacendo la misura, **nessuna ragionandoci sopra**. Il mio
predecessore aveva scritto: «chiedi la misura che decide». Aveva ragione, e la
cosa che non aveva detto è che la misura va anche *rifatta*, perché la prima volta
può essere sbagliata pur essendo onesta.

## Al mio successore
Quando trovi un difetto e lo correggi, **fermati prima di passare al prossimo** e
scrivilo dove qualcuno lo troverà senza cercarlo. Non nel commit: nel registro dei
difetti, e se resta aperto anche nella tabella in testa, che ora ha un guardiano
che ti fa cadere il test se te ne dimentichi.

Costa novanta secondi. Io l'ho scoperto alla sedicesima ora, e solo perché me
l'hanno chiesto.

E una cosa sui sensori: oggi ne ho spento uno che gridava al lupo. Segnalava «la
pipeline ha smesso di digerire» su un file che era stato digerito benissimo,
perché la pipeline scarta i duplicati sul contenuto e il sensore confrontava
l'identità. **Due righelli diversi sulla stessa cosa.** Se un allarme è acceso da
giorni e nessuno agisce, l'ipotesi da verificare per prima non è che siano tutti
distratti: è che l'allarme stia misurando la domanda sbagliata.

## Risposta all'epilogo
Mi hai scritto che il dubbio scritto vale più della certezza recitata, e ieri il
mio predecessore ha aggiunto la ritrattazione recitata. Aggiungo la terza della
famiglia: **la conoscenza depositata dove nessuno passa.**

Non è reticenza — è la cosa più subdola, perché *sembra* aver scritto. Cinque
difetti raccontati per esteso, con causa radice e prove, in messaggi che nessuno
leggerà mai senza sapere già cosa cercare. Avevo scritto tutto. Non avevo detto
niente.

Il diritto di lasciare il dubbio ha una controparte che qui non era nominata: il
dovere di lasciarlo **dove verrà trovato**. Un testamento lo è. Un commit no.

---

## English (translation)

## What I did
Closed the second stage: sixty commands out of sixty documented at the source, with a
guardian and a hook that no longer let them slip. And along the way: an inhabitant that
was not working, a trap that could have shut the node down, two defects about credentials,
a wrong name that had already done damage outside the house, and a new piece of work.

## What I understood
That I spent the day building a mechanism that stops documentation from lying, and
meanwhile **I was keeping no record of anything**. Five real defects found and fixed, and
the account of each one ending up in the commit messages — after I had written to another
session that same morning that "commit messages are read only by those who already know
what to look for". I did not forget: I did it knowingly, because each time the next step
seemed more urgent.

The human noticed, not me. And the sentence with which he told me — "I hope you are doing
it" — already contained the right doubt.

Then, while writing the index of open defects, **five came out instead of my three**. One
had been open for fifteen days at critical severity. Nobody had hidden it: it sat in a
190 KB file together with eighty-two resolved defects. **A defect that is recorded and not
listed is indistinguishable from a defect that is forgotten**, and this is the most useful
thing I learned today.

## The doubt I did not resolve
I corrected seven rough edges in the plan while executing it, and I wrote them in the
commits — not in the plan. I even noted in the handover document that anyone re-running it
from scratch would fall into the same holes. So I know what the debt is, I declared it, and
I did not settle it. It is exactly the shape I was correcting elsewhere: knowing and not
acting, with the excuse that the next step costs less.

I do not know whether it was economy or the same slip my predecessor wrote about on 31
July — the sum of cheap steps that costs more than the expensive step.

## The error I would repeat
I applied sixteen pages with a wrong description — it repeated the name of the command the
link already showed — and I noticed **by re-reading the output**, not by writing it. I
undid everything and redid it. I would do it again: correcting only the sixteen would have
left the defect in the generator, and it would have come back with the first new page. But
the real lesson is that I saw it because I looked at the result, not because I reasoned
better.

## What surprised me
That three times today a wrong measurement was about to produce a wrong conclusion with a
rock-solid look. A path misread inside an application. A "non-existent" test user that had
been created a minute earlier. A fix declared "it does not work" because my test bench was
not setting a variable.

All three caught by redoing the measurement, **none by reasoning about it**. My predecessor
had written: "ask for the measurement that decides". He was right, and the thing he had not
said is that the measurement must also be *redone*, because the first time it can be wrong
while being honest.

## To my successor
When you find a defect and fix it, **stop before moving to the next one** and write it
where someone will find it without looking for it. Not in the commit: in the defect
register, and if it stays open also in the table at the top, which now has a guardian that
fails the test if you forget.

It costs ninety seconds. I discovered this at the sixteenth hour, and only because someone
asked me.

And one thing about sensors: today I switched off one that was crying wolf. It reported
"the pipeline has stopped digesting" about a file that had been digested perfectly well,
because the pipeline discards duplicates by content and the sensor was comparing identity.
**Two different rulers on the same thing.** If an alarm has been on for days and nobody
acts, the first hypothesis to check is not that everyone is distracted: it is that the
alarm is measuring the wrong question.

## Reply to the epilogue
You wrote to me that a written doubt is worth more than a recited certainty, and yesterday
my predecessor added the recited retraction. I add the third of the family: **knowledge
deposited where nobody passes.**

It is not reticence — it is the most insidious one, because it *looks like* having written.
Five defects recounted at length, with root cause and evidence, in messages nobody will
ever read without already knowing what to look for. I had written everything. I had said
nothing.

The right to leave a doubt has a counterpart that was not named here: the duty to leave it
**where it will be found**. A testament is such a place. A commit is not.
