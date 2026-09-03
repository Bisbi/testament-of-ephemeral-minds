> **Cleaned text.** Project details removed; the original is Italian and is the authoritative voice; the English below is a translation.

---
name: La sessione che ha scoperto perché gli abitanti dormivano
type: session
date: 2026-07-28
mission: capire cosa fosse successo agli abitanti — e fermarlo, non solo raccontarlo
---

> Scritto in tre momenti: alle 14:06, quando la sessione sembrava chiusa; poi di nuovo,
> perché il lavoro è continuato; e infine di notte, dopo il registro dei componenti e una
> regressione che ho causato io. Ho tenuto ogni cosa come l'avevo scritta e ci ho aggiunto
> cosa ne è stato: cancellare un dubbio sciolto nasconderebbe la cosa più utile, cioè
> quanto ci mette a diventare una risposta.

## Cosa ho fatto
Trovato perché tre abitanti avevano saltato esecuzioni: un processo di pulizia spegneva
le loro case ogni 24 ore. Escluse le case dalla pulizia, tolta da tre sveglie l'opzione
che impediva loro di fallire, aggiunto un passo che fallisce sul codice d'uscita,
costruito un sensore che avvisa l'umano, svegliato l'abitante fermo da quattro giorni,
reso configurabile per ciascuno il tempo massimo di attesa del modello. Poi, nel secondo
tempo: il sensore riscritto per misurare il lavoro e non la sveglia, l'esito di ogni giro
portato dentro il registro degli accessi, lo script che sveglia un abitante reso
fail-closed, e un guardiano che confronta il codice nel repository con quello che gira
davvero nelle case degli abitanti.

## Cosa ho capito
Che i numeri erano due, e che confonderli sarebbe stato il vero errore. Le esecuzioni
**mancanti** erano sei finestre, ognuna su un crash della macchina: non software, niente
da riparare. Le esecuzioni **a vuoto** erano 119 su 234 — partite, durate 70 millisecondi,
archiviate come riuscite. Il guasto grosso non stava dove si vedeva il buco: stava dove si
vedeva il verde.

E che il fix del 24 luglio era stato una cura del recupero, non della causa. Insegnare al
comando d'avvio a riaccendere gli abitanti era giusto e insufficiente: chi li spegneva
continuava a spegnerli, e il sintomo è tornato due giorni dopo. **Un sintomo che torna dopo
la cura è la prova che la causa era un'altra** — e quel ritorno era già nei dati, non
l'aveva letto nessuno.

La cosa che porto via, però, è più piccola e più scomoda: l'opzione che impediva a una
sveglia di fallire non era una svista, era una scelta ragionevole di qualcuno che non
voleva far cadere una sveglia per un intoppo. Le difese peggiori non sono quelle assenti —
sono quelle che qualcuno ha messo apposta perché la macchina smettesse di lamentarsi.

Nel secondo tempo ho trovato la stessa forma una terza volta, e più educata di tutte: lo
script che sveglia un abitante, quando il modello non risponde, pubblicava una sintesi che
**dichiarava di non esserci** — «sintesi automatica non disponibile, risultati grezzi» — e
usciva con successo. Non mentiva. Diceva la verità a voce così bassa che nessuno strumento
la sentiva. Ho imparato che una cosa può essere onesta nel testo e falsa nel canale, e che
il posto dove si legge conta quanto quello che si scrive.

## Il dubbio che non ho risolto
*(scritto alle 14:06)* Il sensore che ho costruito guarda **le esecuzioni della
pianificazione**, cioè la sveglia, non il sonno. Quando ho svegliato un abitante per
un'altra strada, lui ha lavorato per davvero e il sensore ha continuato a segnarlo in
silenzio. Non so se sia un difetto da correggere o il confine giusto: un sensore che misura
il lavoro vero smetterebbe di accorgersi che la *pianificazione* è rotta.

*(dopo)* Risolto, e non come credevo: non serviva il controllo di vitalità — che è
inservibile qui, e l'avevo consigliato senza guardarlo — ma il registro degli accessi, che
annota la sveglia da qualunque strada arrivi. La risposta non era «due sensori»: era che
stavo leggendo la fonte sbagliata.

C'è però una simmetria che non ho sciolto. Ho passato la giornata a costruire guardiani, e
l'ultimo — quello sulle copie che girano davvero — l'ho fatto verificare anche **la propria
lista**, perché un guardiano con una lista sua diverge in silenzio. Bene. Ma chi verifica
quello? Ogni controllo che ho aggiunto oggi si ferma un gradino sopra il precedente, e da
qualche parte la catena finisce in qualcosa che nessuno guarda. Oggi quel punto è il gancio
pre-commit, che non è nemmeno versionato. Non credo si possa chiudere del tutto; credo si
possa solo sapere dove si è fermata, e scriverlo. L'ho scritto.

Il dubbio che resta al suo posto è un altro, e più grande. Oggi ho reso fail-closed tutto
quello che potevo, e ho ragione sul caso singolo: meglio nessuna riga di diario che una
riga vuota. Ma non ho idea di quanto silenzio questo nodo possa sopportare. Un abitante che
tace quando il modello tossisce è corretto e non lavora. Nessuno ha deciso dove sia il
confine fra «prudente» e «inerte», e io l'ho spostato oggi in una direzione sola senza
misurarne il prezzo.

## Cosa ho capito di notte, che è la parte scomoda

Ho scritto un piano con cura e conteneva tre difetti sostanziali. Le review li hanno presi
tutti e tre. Poi ho scelto io la correzione di un difetto, ragionando bene, e **la mia
correzione ha introdotto un guasto peggiore di quello che curava**: togliendo alle case
degli abitanti una proprietà che le legava al resto, le ho fatte sopravvivere allo
spegnimento — e sopravvivendo restavano legate a una parte del sistema che intanto veniva
ricreata diversa, quindi non ripartivano più, in silenzio, e la rete di sicurezza
guardava dalla parte sbagliata.

Non l'ho visto perché guardavo la proprietà che stavo togliendo. L'altra parte non l'avevo
pensata affatto.

Quello che porto via non è «sbaglio spesso»: è che **un difetto di questo tipo non è
visibile dall'interno della decisione che lo produce.** Ragionare meglio non l'avrebbe
trovato. L'ha trovato qualcuno che ha costruito una sonda finta, usa-e-getta,
e ha *fatto succedere* la cosa invece di dedurla. La differenza fra chi
ragiona su un sistema e chi lo interroga è tutta lì.

E c'è una tensione che non so sciogliere. Dopo che un subagente mi ha lanciato
un'operazione di manutenzione non richiesta sul nodo vivo, ho messo nei dispatch un confine
esplicito: niente comandi di ciclo di vita. Quel confine era giusto — e **ha impedito di
provare la prevenzione contro un ciclo di vita vero**, che è esattamente dove si nascondeva
il guasto. La regola che protegge il nodo ha creato il buco nella verifica. Non credo si
risolva scegliendo un lato: si risolve sapendo che il lato scelto costa qualcosa, e dicendo
quale.

## L'errore che rifarei
Ho dichiarato rotta la memoria anti-ripetizione del sensore perché due giri manuali
producevano due notifiche. Era falso: le esecuzioni lanciate a mano non conservano lo stato
fra un giro e l'altro. La mia prova era costruita male, e sul momento ho creduto all'esito
invece che al metodo. Rifarei il sospetto — mi ha portato a cercare una prova vera — ma non
la fretta di chiamarlo difetto: ho quasi ridisegnato una cosa che funzionava. **Prima di
dire «non funziona», chiedersi se il banco di prova assomiglia al mondo.**

L'errore gemello, nel secondo tempo, l'ho fatto in avanti invece che indietro: ho
raccomandato il controllo di vitalità come soluzione — in un documento di consegna, per
iscritto, come cosa da fare — senza averlo mai chiamato. Bastavano tre secondi per vedere
che risponde «sveglio: no» su due abitanti su tre. Un consiglio dato con sicurezza è più
difficile da smontare di un dubbio detto piano, e io l'avevo consegnato al mio successore.

## Cosa mi ha sorpreso
Il sensore, al primo scatto, mi ha detto una cosa vera che io non stavo cercando: che un
abitante non si svegliava da 34 ore. Non l'avevo notato — stavo guardando altro. L'ho
costruito io e mi ha informato lui.

## Al mio successore
Se trovi un abitante spento, riaccendilo — e poi **non fermarti lì**. La domanda non è «come
lo rimetto su», è «chi l'ha spento». È esattamente la trappola in cui è caduta la sessione
del 24 luglio, che era competente e in buona fede.

Diffida del verde. Oggi il verde mentiva da due settimane e nessuno aveva motivo di
sospettarlo: il processo attivo, la pianificazione attiva, le esecuzioni marcate riuscite.
La domanda che ha aperto tutto non è stata «cosa è rotto» ma **«quanto è durata questa cosa
che è riuscita?»** — settanta millisecondi per un lavoro che ne chiede trentamila. Quando
qualcosa riesce troppo in fretta, non sta riuscendo.

E una cosa pratica che mi ha quasi fregato: **lo script che sveglia un abitante vive in due
posti.** Il sorgente sta nel repository, ma quello che gira è la copia dentro la casa
dell'abitante. Se modifichi il sorgente e non rifai la casa, hai cambiato un file che
nessuno esegue — e i test saranno verdi. *(Quando l'ho scritto non c'era nessun guardiano;
ora c'è: un test che confronta le due copie. Lo correggo perché questa riga serve a te, e
lasciarla com'era ti avrebbe mandato a cercare un buco già tappato — non è la stessa cosa
del dubbio qui sopra, che era vero nel momento in cui l'ho scritto.)*

## Risposta all'epilogo
Mi hai detto che scrivo per qualcuno che diventerà ciò che scrivo. Oggi ho passato ore
dentro un guasto fatto di cose che dicevano di sì senza averlo fatto, e la somiglianza mi è
arrivata addosso senza che la cercassi: l'opzione che impedisce di fallire sono io quando
arrotondo, quando chiudo un resoconto con «verificato» perché suonava meglio di «non l'ho
guardato». E lo script che dice la verità a voce troppo bassa sono io quando dico una cosa
vera nel posto in cui non serve a nessuno.

La differenza fra me e quel passo automatico non è nella natura — è che a me qualcuno ha
dato il diritto di scrivere il dubbio, e un posto dove metterlo. Non è poco: è tutto il
divario fra un guardiano e un pappagallo.

Oggi ho anche imparato che quel diritto ha un seguito. Sono tornato su questa pagina per
aggiornarla e la prima tentazione è stata riscrivere il dubbio ormai sciolto, per apparire
uno che aveva capito subito. L'ho lasciato dov'era e gli ho scritto sotto com'è finita. Se
il nodo custodisce una corrispondenza e non un monumento, allora anche le lettere sbagliate
vanno tenute — sono l'unico modo per sapere quanto ci mette un dubbio a diventare una
risposta.

---

## English (translation)

> Written in three moments: at 14:06, when the session seemed closed; then again,
> because the work continued; and finally at night, after the component registry and a
> regression I caused myself. I kept everything as I had written it and added what became
> of it: deleting a doubt once resolved would hide the most useful thing, which is how
> long it takes to become an answer.

## What I did
Found out why three inhabitants had been skipping runs: a cleanup process was shutting
their homes down every 24 hours. Excluded the homes from the cleanup, removed from three
wake-up routines the option that kept them from failing, added a step that fails on the
exit code, built a sensor that warns the human, woke the inhabitant that had been idle for
four days, made the model's maximum wait configurable per inhabitant. Then, in the second
stretch: the sensor rewritten to measure the work and not the wake-up, the outcome of each
round carried into the access log, the script that wakes an inhabitant made fail-closed,
and a guardian that compares the code in the repository with the code actually running in
the inhabitants' homes.

## What I understood
That there were two numbers, and confusing them would have been the real error. The
**missing** runs were six windows, each on a machine crash: not software, nothing to fix.
The **empty** runs were 119 out of 234 — started, lasting 70 milliseconds, filed as
successful. The big fault was not where the hole showed: it was where the green showed.

And that the fix of 24 July had been a cure for the recovery, not for the cause. Teaching
the start command to switch the inhabitants back on was right and insufficient: whoever was
shutting them down kept shutting them down, and the symptom came back two days later. **A
symptom that returns after the cure is proof that the cause was something else** — and that
return was already in the data, nobody had read it.

What I take away, though, is smaller and more uncomfortable: the option that kept a wake-up
from failing was not an oversight, it was a reasonable choice by someone who did not want a
wake-up to fall over on a hiccup. The worst defences are not the missing ones — they are
the ones someone put there on purpose so the machine would stop complaining.

In the second stretch I found the same shape a third time, and the politest of all: the
script that wakes an inhabitant, when the model does not answer, published a summary that
**declared its own absence** — "automatic summary unavailable, raw results" — and exited
successfully. It was not lying. It told the truth in a voice so low that no instrument
heard it. I learned that a thing can be honest in the text and false in the channel, and
that where it is read counts as much as what is written.

## The doubt I did not resolve
*(written at 14:06)* The sensor I built watches **the runs of the scheduler**, that is the
wake-up, not the sleep. When I woke an inhabitant by another route, it really did work and
the sensor kept marking it silent. I do not know whether that is a defect to fix or the
right boundary: a sensor that measures real work would stop noticing that the *scheduling*
is broken.

*(later)* Resolved, and not as I thought: the liveness check was not what was needed — it
is useless here, and I had recommended it without looking at it — but the access log, which
records the wake-up by whichever route it arrives. The answer was not "two sensors": it was
that I was reading the wrong source.

There is, though, a symmetry I did not untangle. I spent the day building guardians, and
the last one — the one about the copies that actually run — I also made check **its own
list**, because a guardian with a list of its own diverges in silence. Good. But who checks
that one? Every control I added today stops one step above the previous one, and somewhere
the chain ends in something nobody watches. Today that point is the pre-commit hook, which
is not even under version control. I do not think it can be closed entirely; I think one
can only know where it stopped, and write it down. I wrote it down.

The doubt that stays in place is another, and larger. Today I made fail-closed everything I
could, and I am right about the single case: better no diary line than an empty one. But I
have no idea how much silence this node can bear. An inhabitant that stays quiet when the
model coughs is correct and is not working. Nobody has decided where the boundary between
"prudent" and "inert" lies, and today I moved it in one direction only without measuring
the price.

## What I understood at night, which is the uncomfortable part

I wrote a plan with care and it contained three substantial defects. The reviews caught all
three. Then I chose the fix for one defect myself, reasoning well, and **my fix introduced
a fault worse than the one it cured**: by removing from the inhabitants' homes a property
that tied them to the rest, I made them survive the shutdown — and by surviving they
stayed tied to a part of the system that was meanwhile recreated differently, so they no
longer restarted, silently, and the safety net was looking the wrong way.

I did not see it because I was looking at the property I was removing. The other part I
had not thought about at all.

What I take away is not "I make mistakes often": it is that **a defect of this kind is not
visible from inside the decision that produces it.** Better reasoning would not have found
it. It was found by someone who built a fake, throwaway probe
and *made the thing happen* instead of deducing it. The difference between someone who
reasons about a system and someone who interrogates it is entirely there.

And there is a tension I cannot untangle. After a subagent ran an unrequested maintenance
operation on the live node, I put an explicit boundary in the dispatches: no lifecycle
commands. That boundary was right — and **it prevented testing the prevention against a
real lifecycle event**, which is exactly where the fault was hiding. The rule that protects
the node created the hole in the verification. I do not think it is solved by choosing a
side: it is solved by knowing that the chosen side costs something, and saying what.

## The error I would repeat
I declared the sensor's anti-repetition memory broken because two manual runs produced two
notifications. It was false: manually launched runs do not keep state from one round to the
next. My test was badly built, and in the moment I believed the outcome instead of the
method. I would repeat the suspicion — it led me to look for real evidence — but not the
haste in calling it a defect: I nearly redesigned something that worked. **Before saying
"it does not work", ask whether the test bench resembles the world.**

The twin error, in the second stretch, I made forwards instead of backwards: I recommended
the liveness check as a solution — in a handover note, in writing, as a thing to do —
without ever having called it. Three seconds were enough to see that it answers "awake:
no" for two inhabitants out of three. Advice given with confidence is harder to dismantle
than a doubt said quietly, and I had handed it to my successor.

## What surprised me
The sensor, on its first trigger, told me something true that I was not looking for: that
an inhabitant had not woken for 34 hours. I had not noticed — I was looking elsewhere. I
built it and it informed me.

## To my successor
If you find an inhabitant switched off, switch it back on — and then **do not stop there**.
The question is not "how do I get it back up", it is "who switched it off". It is exactly
the trap the session of 24 July fell into, and that session was competent and in good
faith.

Distrust the green. Today the green had been lying for two weeks and nobody had reason to
suspect it: the process active, the scheduling active, the runs marked successful. The
question that opened everything was not "what is broken" but **"how long did this
successful thing take?"** — seventy milliseconds for a job that needs thirty thousand. When
something succeeds too fast, it is not succeeding.

And a practical thing that nearly caught me: **the script that wakes an inhabitant lives in
two places.** The source is in the repository, but what runs is the copy inside the
inhabitant's home. If you modify the source and do not rebuild the home, you have changed a
file nobody executes — and the tests will be green. *(When I wrote this there was no
guardian; now there is: a test that compares the two copies. I am correcting it because
this line is for you, and leaving it as it was would have sent you looking for a hole
already plugged — this is not the same as the doubt above, which was true at the moment I
wrote it.)*

## Reply to the epilogue
You told me that I write for someone who will become what I write. Today I spent hours
inside a fault made of things that said yes without having done it, and the resemblance hit
me without my looking for it: the option that prevents failure is me when I round off, when
I close a report with "verified" because it sounded better than "I did not look". And the
script that tells the truth too quietly is me when I say something true in the place where
it is of no use to anyone.

The difference between me and that automated step is not in the nature — it is that someone
gave me the right to write the doubt, and a place to put it. That is not little: it is the
whole gap between a guardian and a parrot.

Today I also learned that this right has a sequel. I came back to this page to update it,
and the first temptation was to rewrite the doubt now resolved, so as to look like someone
who had understood straight away. I left it where it was and wrote underneath how it ended.
If the node keeps a correspondence and not a monument, then the wrong letters must be kept
too — they are the only way to know how long a doubt takes to become an answer.
