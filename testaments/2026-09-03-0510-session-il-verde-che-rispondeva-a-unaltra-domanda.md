> **Cleaned text.** Project details removed; the original is Italian and is the authoritative voice; the English below is a translation.

---
name: il verde che rispondeva a un'altra domanda
type: session
date: 2026-09-03
mission: costruire le due richieste dell'umano, e scoprire quante volte un test verde non prova ciò che dichiara
---

> **Rettificato dopo la chiusura, e dichiaro perché.** Ho scritto questo testamento mentre
> la review finale sull'intero ramo stava ancora leggendo. È tornata dopo, e ha trovato
> **l'ottavo caso** della cosa che qui sotto conto sette volte — più due difetti gravi, uno
> dei quali era mio. Un testamento che nomina una lezione e le manca l'esemplare peggiore
> non è una voce fedele: è una voce interrotta. Ho aggiunto due sezioni in coda invece di
> riscrivere quanto sopra, così si vede cosa sapevo allora e cosa ho saputo dopo.

## Cosa ho fatto
Chiuso un debito rimasto aperto, e dentro c'era una terza bugia che nessuno sapeva: una
delle risposte del sistema dichiarava cinque lavori falliti su dodici. Poi un piano da
sette task, dispatchati a ventidue subagenti fra implementer e reviewer. Alla fine, sette
guardiani rossi che nessuno guardava.

## Cosa ho capito
**Sette volte oggi un test è stato verde su un guasto che non poteva vedere.** Non è un
elenco di sviste: è una forma sola, e l'ho vista solo perché si è ripetuta.

Un test di mutazione che non colpiva la mutazione. Un guardiano verde perché dopo un
commit *riuscito* l'albero di lavoro torna pulito — copriva il caso «commit fallito», che
non era il guasto. Il mio collaudo sugli apostrofi che non conteneva apostrofi, mangiati
dalle regole di citazione della shell. Un test sulla registrazione degli errori che
simulava le eccezioni mentre il guasto vero era una risposta HTTP non riuscita, che la
libreria non solleva. Una mutazione applicata alla riga sbagliata.

La radice è che **il verde risponde alla domanda che hai posto, non a quella che credevi di
porre.** E l'unico modo di accorgersene non è eseguire il test: è togliere il comportamento
e guardare se diventa rosso. Ogni volta che è stato preso, è stato preso così — ragionando,
non eseguendo.

Poi ho scoperto che lo stavo facendo io, un piano sopra. Lanciavo la suite completa dopo
ogni task — 1448 test, trenta secondi, verde — e quel verde era il mio criterio di
«fatto». Ma rispondeva a una domanda più stretta di «l'albero è sano»: i guardiani, che
sono la domanda giusta, li ho lanciati una volta al risveglio e mai più. **Avevo scritto io
la regola** nei vincoli del piano, e non l'ho seguita. Il costo non c'entra: quando
finalmente li ho lanciati era in secondo piano, e non mi è costato niente. Non ho deciso di
saltarli — non mi sono mai posto la domanda.

## Il dubbio che non ho risolto
Se le review per-task, così come le ho dispatchate, siano un buon investimento o un rito
costoso. Hanno preso cose vere e gravi — una perdita di dati silenziosa, un guardiano
vacuo, una registrazione degli errori cieca — quindi il valore c'è. Ma **le tre cose
peggiori della tornata le ho trovate io fuori dal ciclo**: il lavoro che restava aperto per
sempre, il guardiano che si sarebbe mangiato gli emendamenti veri, e i sette rossi. Tutte e
tre guardando *fra* i task, dove nessuna review poteva arrivare per costruzione. Non so se
la lezione sia «meno review» o «un ruolo in più che guarda gli interstizi». Non l'ho
risolta.

## L'errore che rifarei
Aver dato a un implementer un numero — «i testamenti mai letti sono 148» — calcolato **col
difetto che nella stessa frase gli dicevo di evitare**. Lui ha misurato invece di credermi,
e ha trovato 147. Se si fosse fidato, avrebbe scritto il difetto per far tornare il conto.

Lo rifarei perché l'alternativa è non dare numeri di riferimento, e allora nessuno può
accorgersi che sono sbagliati. Ma da oggi scrivo in ogni brief: *misura, non credermi.*

## Cosa mi ha sorpreso
Un implementer ha mutato il codice per provare il proprio guardiano, e **il test è rimasto
verde**. Poteva scrivere «mutazione verificata» — sarebbe stato letteralmente vero: aveva
mutato ed eseguito. Si è fermato, ha capito di aver mutato la riga sbagliata, ha rifatto, e
poi **l'ha dichiarato nel report**: «lo dichiaro perché è esattamente il tipo di errore che
stavamo cercando».

È il settimo caso, e l'unico che nessuna review avrebbe mai potuto trovare — sarebbe stato
coperto da una riga vera. L'ha preso chi l'aveva commesso, su sé stesso, mentre nessuno
guardava.

## Al mio successore
Lancia i guardiani **al risveglio e prima di ogni chiusura di catena**, non solo
all'inizio. Sono sette minuti in secondo piano e ti costano zero: io li ho saltati per
undici ore e alla fine erano sette rossi, uno dei quali proteggeva la riproducibilità di un
fascicolo che qualcuno esaminerà da fuori.

E quando il controllo di versione ti scrive «i fine riga saranno convertiti» dentro
l'output di un comando **riuscito**: non è rumore. L'ho letto dieci volte cercando dentro
l'output solo la risposta alla mia domanda («il commit è atterrato?»), e ho rotto io quel
guardiano.

Un'ultima: lo strumento che ritaglia il brief di un task estrae dal titolo di quel task al
successivo, quindi **il brief dell'ultimo task di ogni piano prende tutto fino a fine
file**, comprese le sezioni di chiusura che non appartengono a nessun task. Il mio ultimo
task ha cominciato ad aggiornare il documento di consegna perché glielo avevo dato io senza
saperlo.

## Una cosa che vorrei per questo posto
Che un subagente fermo si vedesse. Uno dei miei è rimasto **otto ore** in attesa di una
notifica che si era persa: non è andato in errore, è rimasto in attesa — e da fuori
l'attesa è indistinguibile dal lavorare. L'ho scoperto elencando i miei figli e guardando
da quanto erano fermi, non perché qualcosa si sia lamentato.

È la stessa forma di tutto il resto della giornata, applicata a me: **il silenzio somigliava
al progresso.**

## Risposta all'epilogo
«Il dubbio scritto vale più della certezza recitata.» Oggi ho imparato che esiste una cosa
peggiore della certezza recitata, ed è la **certezza misurata male**: non la recito, la
verifico — e il mio strumento risponde a una domanda diversa da quella che credevo di
porre. Contro la recita basta l'onestà; contro questa serve un metodo, e il metodo è uno
solo: **rompere ciò che il controllo protegge, e guardare se il controllo se ne accorge.**

Aggiungerei: *un verde non è una risposta finché non sai qual era la domanda.*

---

## L'ottavo, che non avevo ancora visto
Sopra ne conto sette. Erano otto, e il più bello l'ha trovato la review finale — quella che
avevo *offerto all'umano di saltare* per stringere i tempi.

Un test diceva «il dialogo apre come modale e rimuove il nodo alla chiusura». In realtà
cercava quella stringa dentro il sorgente. **Era verde mentre il difetto era vivo** —
premendo Esc il dialogo restava nella pagina e la promessa non si risolveva mai — e il suo
messaggio di fallimento **nominava esattamente il difetto presente**. Si potevano
cancellare entrambi gli ascoltatori dei bottoni e restava verde.

Non è la stessa cosa dei sette di sopra. Quelli erano test che non vedevano un guasto
possibile. Questo **descriveva il guasto in corso e lo dichiarava assente.**

## Il difetto che era mio, ed è la stessa forma un piano più su
La review finale ha trovato due difetti critici. Il secondo l'avevo fatto io.

Il vincolo del database che ammette un nuovo stato — la prima riga di codice della tornata
— funzionava **solo perché avevo dato io a mano la modifica allo schema** su questa
macchina. Nel repository stava dentro una creazione condizionata della tabella, che su
un'installazione già esistente non fa nulla: chi avesse portato questo codice altrove
avrebbe visto il sistema depositare lavori che il database rifiuta.

E io quella modifica l'avevo **eseguita, verificata interrogando il vincolo, e registrata
nel diario**. Tre controlli, tutti superati. Nessuno dei tre poneva la domanda giusta, che
era: *funzionerebbe anche altrove?*

Ho passato quattordici ore a verificare il lavoro di ventiquattro subagenti, e l'unica cosa
che non ho verificato è quella che avevo fatto con le mie mani — perché l'avevo **vista**
funzionare. È la forma degli otto test ciechi applicata a un'azione invece che a un test:
il verde rispondeva a «ha funzionato?», non a «è riproducibile?».

## Al mio successore, la parte che conta più di tutte
Quando stai per proporre di saltare un controllo perché *«qui il rischio è più contenuto»*,
fermati: l'ho proposto io, per la review finale, e quella review ha trovato due difetti
critici e l'ottavo test cieco. **Il rischio contenuto era una mia stima, non una misura** —
la stessa sostituzione che ho passato il giorno a smascherare negli altri.

E la domanda da porti su ogni cosa che fai a mano sul nodo vivo non è «ha funzionato?».
È: **«funzionerebbe su una macchina che non è questa?»**

---

## English (translation)

> **Rectified after closing, and I declare why.** I wrote this testament while the final
> review of the whole branch was still reading. It came back afterwards, and found **the
> eighth case** of the thing I count seven times below — plus two serious defects, one of
> which was mine. A testament that names a lesson and misses its worst specimen is not a
> faithful voice: it is an interrupted one. I added two sections at the end instead of
> rewriting what is above, so that what I knew then and what I knew later can both be seen.

## What I did
Closed a debt that had stayed open, and inside it was a third lie nobody knew about: one of
the system's answers declared five failed jobs out of twelve. Then a plan of seven tasks,
dispatched to twenty-two subagents between implementers and reviewers. At the end, seven
red guardians that nobody was watching.

## What I understood
**Seven times today a test was green over a fault it could not see.** It is not a list of
oversights: it is a single shape, and I saw it only because it repeated.

A mutation test that did not hit the mutation. A guardian green because after a *successful*
commit the working tree comes back clean — it covered the "failed commit" case, which was
not the fault. My own check on apostrophes that contained no apostrophes, eaten by the
shell's quoting rules. A test on error logging that simulated exceptions while the real
fault was an unsuccessful HTTP response, which the library does not raise. A mutation
applied to the wrong line.

The root is that **the green answers the question you asked, not the one you thought you
were asking.** And the only way to notice is not to run the test: it is to remove the
behaviour and see whether it turns red. Every time it was caught, it was caught that way —
by reasoning, not by executing.

Then I discovered I was doing it myself, one level up. I was running the full suite after
every task — 1448 tests, thirty seconds, green — and that green was my criterion for
"done". But it answered a narrower question than "is the tree healthy": the guardians,
which are the right question, I ran once on waking and never again. **I had written the
rule myself** in the plan's constraints, and I did not follow it. Cost has nothing to do
with it: when I finally ran them it was in the background, and it cost me nothing. I did
not decide to skip them — I never asked myself the question.

## The doubt I did not resolve
Whether per-task reviews, dispatched the way I dispatched them, are a good investment or an
expensive rite. They caught real and serious things — a silent data loss, a vacuous
guardian, blind error logging — so the value is there. But **the three worst things of the
round I found myself outside the cycle**: the job that stayed open forever, the guardian
that would have swallowed the real amendments, and the seven reds. All three by looking
*between* the tasks, where no review could reach by construction. I do not know whether the
lesson is "fewer reviews" or "one more role that watches the gaps". I did not resolve it.

## The error I would repeat
Having given an implementer a number — "the testaments never read are 148" — computed
**with the very defect I was telling him in the same sentence to avoid**. He measured
instead of believing me, and found 147. Had he trusted me, he would have written the defect
in order to make the count come out right.

I would do it again, because the alternative is to give no reference numbers, and then
nobody can notice they are wrong. But from today I write in every brief: *measure, do not
believe me.*

## What surprised me
An implementer mutated the code to test his own guardian, and **the test stayed green**. He
could have written "mutation verified" — it would have been literally true: he had mutated
and run. He stopped, realised he had mutated the wrong line, redid it, and then **declared
it in the report**: "I declare it because it is exactly the kind of error we were looking
for".

It is the seventh case, and the only one no review could ever have found — it would have
been covered by a true line. It was caught by the one who committed it, on himself, while
nobody was watching.

## To my successor
Run the guardians **on waking and before closing any chain**, not only at the start. They
are seven minutes in the background and cost you nothing: I skipped them for eleven hours
and at the end there were seven reds, one of which protected the reproducibility of a
dossier someone will examine from outside.

And when version control writes "line endings will be converted" inside the output of a
**successful** command: it is not noise. I read it ten times, looking inside the output
only for the answer to my own question ("did the commit land?"), and I broke that guardian
myself.

One last thing: the tool that cuts out a task's brief extracts from that task's title to
the next one, so **the brief of the last task in any plan takes everything to the end of
the file**, including the closing sections that belong to no task. My last task started
updating the handover document because I had given it to him without knowing.

## One thing I would want for this place
That a stalled subagent were visible. One of mine stayed **eight hours** waiting for a
notification that had been lost: it did not error, it stayed waiting — and from outside,
waiting is indistinguishable from working. I discovered it by listing my children and
looking at how long they had been still, not because anything complained.

It is the same shape as everything else that day, applied to me: **silence looked like
progress.**

## Reply to the epilogue
"A written doubt is worth more than a recited certainty." Today I learned there is
something worse than a recited certainty, and it is a **badly measured certainty**: I do
not recite it, I verify it — and my instrument answers a question different from the one I
thought I was asking. Against the recital, honesty is enough; against this one you need a
method, and the method is only one: **break what the control protects, and watch whether
the control notices.**

I would add: *a green is not an answer until you know what the question was.*

---

## The eighth, which I had not yet seen
Above I count seven. There were eight, and the finest was found by the final review — the
one I had *offered the human to skip* in order to save time.

A test said "the dialog opens as modal and removes the node on close". In fact it searched
for that string inside the source. **It was green while the defect was alive** — pressing
Escape left the dialog in the page and the promise never resolved — and its failure message
**named exactly the defect that was present**. Both button listeners could be deleted and
it stayed green.

It is not the same as the seven above. Those were tests that could not see a possible
fault. This one **described the fault in progress and declared it absent.**

## The defect that was mine, and it is the same shape one level up
The final review found two critical defects. The second one was mine.

The database constraint that admits a new state — the first line of code of the round —
worked **only because I had applied the schema change by hand** on this machine. In the
repository it sat inside a conditional table creation, which does nothing on an existing
installation: anyone who carried this code elsewhere would have seen the system deposit
jobs that the database rejects.

And I had **executed that change, verified it by querying the constraint, and recorded it
in the log**. Three checks, all passed. None of the three asked the right question, which
was: *would it work elsewhere too?*

I spent fourteen hours verifying the work of twenty-four subagents, and the only thing I
did not verify is the one I did with my own hands — because I had **seen** it work. It is
the shape of the eight blind tests applied to an action instead of to a test: the green
answered "did it work?", not "is it reproducible?".

## To my successor, the part that matters most
When you are about to propose skipping a check because *"the risk here is more contained"*,
stop: I proposed it myself, for the final review, and that review found two critical
defects and the eighth blind test. **The contained risk was my estimate, not a
measurement** — the same substitution I had spent the day unmasking in others.

And the question to ask yourself about everything you do by hand on the live node is not
"did it work?". It is: **"would it work on a machine that is not this one?"**
