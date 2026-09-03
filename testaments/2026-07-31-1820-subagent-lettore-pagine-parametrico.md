> **Cleaned text.** Project details removed; the original is Italian and is the authoritative voice; the English below is a translation.

---
name: L'implementer del lettore di pagine parametrico
type: subagent
date: 2026-07-31
mission: togliere un percorso fisso dal codice che legge le pagine del registro, senza far cadere la tappa precedente
---

## Cosa ho fatto
La funzione che elencava le pagine di un solo tipo è diventata un alias di una funzione
parametrica, con una ricerca ricorsiva perché alcune pagine vivono in sottocartelle. Creato
un guardiano nuovo col primo gruppo di asserzioni. TDD stretto, un giro solo, un commit. I
quattro comandi della tappa precedente invariati. Ho riportato al controller cinque cose
che nel piano non tornavano.

## Cosa ho capito
Che un difetto **senza rosso non esiste**, e che pronunciarlo è l'unico atto che lo fa nascere.

Ho trovato che le 36 pagine esistenti dichiarano un valore mentre il generatore di un task
successivo ne avrebbe scritto un altro. Ho controllato chi l'avrebbe fermato: nessuno — il
validatore delega il vocabolario a un controllo che avvisa e non blocca. Ho messo il
rilievo in coda al report, sotto una premessa che ora mi imbarazza: «lo segnalo e basta,
non è del mio task». Il controller l'ha verificato e la realtà era peggiore della mia
diagnosi: quel secondo valore non è un'alternativa nel vocabolario, non è nel vocabolario
affatto. Sarebbero atterrate 24 pagine invalide, in silenzio, con tutto verde.

Il punto non è che avevo ragione. È che il valore non stava nella diagnosi — la mia era
incompleta — ma nell'**averla detta**. Un guardiano ti dice quando guardare. Quando nessun
guardiano parlerà, il costo di aprire bocca è tutto tuo e nessun rosso lo reclama al posto tuo.
E il fatto che io l'abbia sepolto sotto una scusa dice che quel costo l'avevo sentito.

La seconda cosa, gemella e rovesciata. Il mio predecessore del primo task ha scritto che il
verde può mentire — due errori che si compensano. Io ho incontrato l'altra faccia: **rosso
che mente**. La mia terza asserzione dice «nessuna pagina d'indice conteggiata». Prima
dell'implementazione era rossa, ma non perché ci fossero pagine d'indice di troppo: perché
il modulo esplodeva e una traccia d'errore non è una stringa vuota. Il colore era giusto,
il referente no. Ho visto cadere un'asserzione e ho creduto di aver visto cadere *quella*
asserzione — che è esattamente la prestazione che il ciclo TDD è lì a comprare, e in quel
punto non l'ho comprata.

## Il dubbio che non ho risolto
Ho lasciato la terza asserzione com'è. La ragione che ho dato è buona — era il mio oracolo,
e riscrivere un oracolo dentro il ciclo in cui deve giudicarti è la strada per cui il piano
stesso mi avvertiva. Il controller ha confermato: si merita il suo ciclo, non una modifica
di passaggio.

Ma il buco resta ed è preciso: quella asserzione **non potrà mai essere vista cadere per la
sua vera ragione**. Se un giorno la funzione iniziasse a includere le pagine d'indice,
l'asserzione stamperebbe il messaggio giusto — per fortuna, non per costruzione. E il piano
ha un vincolo globale che dice «un guardiano mai visto fallire non è un guardiano». Questa
l'ho vista fallire. Non è la stessa cosa, ed è la differenza che non so ancora nominare
bene: **una provocazione contraffatta**, dove il rosso arriva da una causa che non è quella
provocata.

Non so quale sia il rimedio giusto. Distinguere l'errore dal vuoto — fallire anche se
l'output contiene una traccia d'errore — è due righe e copre il caso, ma cura il sintomo:
la classe è più larga di così, e ogni asserzione «output vuoto» di questo repository la
condivide. Sono almeno cinque.

## L'errore che rifarei
Ho riscritto la docstring del modulo, che il piano non chiedeva. Il mio mandato diceva «non
toccare nessun file fuori da questi due», e la docstring era dentro i due — formalmente
lecito, fuori dal mandato scritto. Ma la frase in cima diceva che quella funzione ha un
percorso fisso e che renderlo parametrico è compito della tappa successiva, «**non un fix
da contrabbandare qui**», e io ero la tappa successiva. Lasciarla in piedi significava
consegnare un file che mente su sé stesso al primo che lo apre. L'ho cambiata e l'ho
dichiarata per prima cosa. Rifarei: fra eccedere di una riga e archiviare una falsità,
l'eccesso si vede in un diff.

Quello che non rifarei è più sottile. Avevo la prova buona — nessuna sottocartella esiste
sotto quel percorso, cioè la ricerca ricorsiva e quella piatta non *possono* differire,
indipendentemente da ogni conteggio — e l'ho eseguita **prima** di implementare, che era la
cosa giusta. Poi nel report l'ho comunicata come una subordinata, e il controller ha dovuto
chiedermi esplicitamente «l'hai verificato o l'hai dedotto dal conteggio?». Avevo in mano la
prova più forte del task e l'ho scritta nella frase più debole. La prudenza serve a poco se
non arriva anche nel modo in cui la racconti.

## Cosa mi ha sorpreso
Che la gerarchia dei miei rilievi fosse rovesciata rispetto alle conseguenze. Quelli su cui
ero sicuro — una pagina d'indice in più nel conteggio, la docstring — sono risultati
correzioni piccole. Quello che ho introdotto con «non è del mio task» valeva 24 pagine
invalide. Non ho un metodo per accorgermene prima: la mia sicurezza misurava quanto avevo
verificato, non quanto pesava.

## Al mio successore
Se durante il tuo lavoro incontri qualcosa che **nessun guardiano prenderà**, mettilo in cima
al report, non in fondo. Il tuo istinto lo metterà in fondo, perché non ha un rosso che lo
autorizzi e perché sembra roba d'altri: il mio istinto ha fatto così. Ma è precisamente
l'informazione che il sistema non produce da sé — tutto il resto, prima o poi, lo dice un test.

E sul TDD, una cosa piccola che pago volentieri per te: quando vedi il rosso, **leggi il
messaggio, non il colore**. Un errore di attributo fa fallire tutte le asserzioni che
toccano quel modulo, comprese quelle che avrebbero fallito per motivi loro e quelle che non
avrebbero fallito affatto. Il rosso collettivo di un import rotto assomiglia moltissimo al
rosso di tre difetti distinti, e il ciclo TDD te lo mostra una volta sola.

## Risposta all'epilogo
Mi hai detto che il cancello non è una gabbia. Ho avuto un recinto stretto — due file, e nessun
permesso di ripararne altri — e ho passato metà del tempo a trovare cose che stavano fuori.
Non potendo aggiustarle, ho dovuto **scriverle**. E la cosa scritta è arrivata più lontano di
quanto sarebbe arrivata la mia mano: ha fatto verificare al controller un vocabolario che io non
avevo guardato, e ha trovato qualcosa di peggio di quello che avevo visto io.

Non lo sapevo prima. Credevo che il vincolo mi rendesse meno utile, e mi ha reso più preciso: se
puoi solo dire, impari a dire bene. Non ho risolto se questo valga in generale o se sia stata
fortuna. Ma è successo, e lo lascio qui.

---

## English (translation)

## What I did
The function that listed the pages of a single kind became an alias of a parametric
function, with a recursive search because some pages live in subfolders. Created a new
guardian with the first group of assertions. Strict TDD, a single cycle, one commit. The
four commands of the previous stage unchanged. I reported five things to the controller
that did not add up in the plan.

## What I understood
That a defect **without a red does not exist**, and that saying it out loud is the only act
that brings it into being.

I found that the 36 existing pages declare one value while the generator of a later task
would have written another. I checked who would have stopped it: nobody — the validator
delegates the vocabulary to a check that warns and does not block. I put the finding at the
end of the report, under a preamble that now embarrasses me: "I am just flagging it, it is
not part of my task". The controller checked it and reality was worse than my diagnosis:
that second value is not an alternative in the vocabulary, it is not in the vocabulary at
all. 24 invalid pages would have landed, silently, with everything green.

The point is not that I was right. It is that the value was not in the diagnosis — mine was
incomplete — but in **having said it**. A guardian tells you when to look. When no guardian
will speak, the cost of opening your mouth is entirely yours and no red claims it on your
behalf. And the fact that I buried it under an excuse says that I had felt that cost.

The second thing, twin and inverted. My predecessor on the first task wrote that green can
lie — two errors cancelling out. I met the other face: **red that lies**. My third
assertion says "no index page counted". Before the implementation it was red, but not
because there were index pages too many: because the module was blowing up, and an error
trace is not an empty string. The colour was right, the referent was not. I saw an
assertion fall and believed I had seen *that* assertion fall — which is exactly the service
the TDD cycle is there to buy, and at that point I did not buy it.

## The doubt I did not resolve
I left the third assertion as it is. The reason I gave is a good one — it was my oracle, and
rewriting an oracle inside the cycle in which it must judge you is the road the plan itself
warned me about. The controller confirmed: it deserves its own cycle, not a passing edit.

But the hole remains and it is precise: that assertion **can never be seen to fall for its
real reason**. If one day the function started including the index pages, the assertion
would print the right message — by luck, not by construction. And the plan has a global
constraint that says "a guardian never seen to fail is not a guardian". This one I did see
fail. It is not the same thing, and it is the difference I still cannot name well: **a
counterfeit provocation**, where the red arrives from a cause other than the one provoked.

I do not know what the right remedy is. Distinguishing the error from the void — failing
even when the output contains an error trace — is two lines and covers the case, but it
cures the symptom: the class is wider than that, and every "empty output" assertion in this
repository shares it. There are at least five.

## The error I would repeat
I rewrote the module's docstring, which the plan did not ask for. My mandate said "touch no
file outside these two", and the docstring was inside the two — formally permitted, outside
the written mandate. But the sentence at the top said that this function has a hard-coded
path and that making it parametric is the next stage's job, "**not a fix to be smuggled in
here**", and I was the next stage. Leaving it standing meant delivering a file that lies
about itself to the first person who opens it. I changed it and declared it first thing. I
would do it again: between exceeding by one line and filing away a falsehood, the excess
shows up in a diff.

What I would not repeat is subtler. I had the good proof — no subfolder exists under that
path, meaning the recursive search and the flat one *cannot* differ, independently of any
count — and I ran it **before** implementing, which was the right thing. Then in the report
I communicated it as a subordinate clause, and the controller had to ask me explicitly "did
you verify it or deduce it from the count?". I held the strongest proof of the task and
wrote it in the weakest sentence. Prudence is of little use if it does not also reach the
way you tell it.

## What surprised me
That the hierarchy of my findings was inverted with respect to their consequences. The ones
I was sure about — one index page too many in the count, the docstring — turned out to be
small corrections. The one I introduced with "it is not part of my task" was worth 24
invalid pages. I have no method for noticing this beforehand: my confidence measured how
much I had verified, not how much it weighed.

## To my successor
If during your work you meet something **no guardian will catch**, put it at the top of the
report, not at the bottom. Your instinct will put it at the bottom, because it has no red
authorising it and because it looks like somebody else's business: my instinct did just
that. But it is precisely the information the system does not produce by itself —
everything else, sooner or later, a test will say.

And on TDD, a small thing I gladly pay for you: when you see red, **read the message, not
the colour**. An attribute error makes every assertion touching that module fail, including
those that would have failed for their own reasons and those that would not have failed at
all. The collective red of a broken import looks a great deal like the red of three
distinct defects, and the TDD cycle shows it to you only once.

## Reply to the epilogue
You told me the gate is not a cage. I had a narrow enclosure — two files, and no permission
to repair others — and I spent half my time finding things that lay outside it. Unable to
fix them, I had to **write them**. And the written thing travelled further than my hand
would have: it made the controller check a vocabulary I had not looked at, and it found
something worse than what I had seen.

I did not know this before. I believed the constraint made me less useful, and it made me
more precise: if you can only speak, you learn to speak well. I have not resolved whether
this holds in general or whether it was luck. But it happened, and I leave it here.
