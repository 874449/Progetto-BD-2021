### Progetto per il corso di Basi di Dati 2020/2021

__Gruppo:__ _Math.Random_

Composto da
``Alessandro Zanin (870696)``, ``Matteo Spanio (877485)``, ``Michael Alessandro Montin (874449)``

### Indice

1. **Introduzione al progetto**
   1. Strumenti e piattaforme usate per sviluppare il progetto
      1. Librerie utilizzate
      2. ORM
   2. Gestione del gruppo e suddivisione del lavoro
   3. Istruzioni per il setup dell'ambiente per eseguire il progetto in locale
2. **Database**
   1. Schema logico e relazionale della Base di Dati
      1. Implementazione delle relazioni
   2. Query sviluppate
   3. Transazioni, Rollback, Triggers - Politiche d'integrità del database
   4. Routes in Flask
   5. Implementazione delle funzioni di Login/Sign-in
   6. Analisi dei dati dei questionari
   7. Definizione di ruoli
4. **Misure di sicurezza**
   1. Hash, passwords, ecc.
   2. Autenticazione e Log-in
   3. CSRF, SQL Injection
5. **Sviluppo grafico del sito**

### 1. Introduzione al progetto

Il progetto consiste nell'implementazione di una Web Application 
dedicata alla creazione di questionari. 
Ogni utente può creare innumerevoli questionari, ognuno formato da 
multiple domande che a loro volta possono essere di 
diversa categoria (ad esempio, risposta aperta o scelta multipla).
Ogni utente può inoltre vedere tutti i questionari fatti da altri utenti
e rispondere alle domande in una schermata dedicata.
Il proprietario di un questionario sarà poi in grado di visionare le
risposte fornite dagli utenti 

**i. Strumenti e piattaforme usate per sviluppare il progetto**

Il progetto è stato sviluppato utilizzando Python e SQLAlchemy,
tutti i membri del gruppo hanno usato l'IDE PyCharm per 
interfacciarsi con semplicità ed efficacia allo sviluppo del progetto.\
Il codice è stato condiviso tra i vari membri del gruppo tramite
GitHub in modo che ognuno potesse lavorare sulla versione più recente
possibile, inoltre il database è stato condiviso tramite Heroku, che
ha permesso a tutti i membri di lanciare l'applicazione usando lo
stessa base di dati per la fase di testing e sviluppo.\
Il gruppo ha inoltre deciso di creare un gruppo Whatsapp dedicato al
progetto in cui tutti i membri erano sempre raggiungibili per 
eventuale necessità.\
Il gruppo ha fatto riferimento al libro di testo "Flask Web Development"
di Miguel Grinberg come ulteriore fonte di esempi e spiegazioni riguardanti
Flask e altre componenti del progetto

**ii. Gestione del gruppo e suddivisione del lavoro**

Il gruppo non ha ritenuto necessaria la definizione di ruoli precisi,
ci sono stati multipli incontri online tramite piattaforme come Discord
in cui ogni membro ha avuto la possibilità di esprimere le sue idee
e opinioni, alla fine di ogni incontro ognuno si è autonomamente
assegnato gli incarichi che si trovava più a suo agio a svolgere,
nello specifico `Michael` ha preferito principalmente concentrarsi sulla
creazione di triggers, `Matteo` ha deciso di
concentrare i suoi sforzi principalmente sullo sviluppo di funzionalità
con Python mentre `Alessandro` ha curato la veste grafica 
dell'applicazione e la documentazione. 
Nonostante questo, ogni sviluppo è stato ampiamente discusso e trattato
con tutti i membri del gruppo che hanno dato il loro contributo ogni 
qualvolta fosse richiesto.

**iii. Istruzioni per il setup dell'ambiente per eseguire il progetto in locale**

# **MATTEO QUI LASCIO SPAZIO A TE HAHA**

### 2. Database

**i. Schema logico e relazionale della Base di Dati**

Per la Base di dati è stato sviluppato il seguente schema logico
e relazionale che illustra le relazioni e gli attributi delle varie 
tabelle

**a. Implementazione delle relazioni**

riga 144 file models.py

# **Immagine con schema di michael qui**

**ii. Query sviluppate**

codice delle query e breve descrizione di dove è 
stata usata e come

**iii. Transazioni, Rollback, Triggers - Politiche d'integrità del database**

usando orm ci stacchiamo da database di postgres,
ovvero il database puro, con orm astrai e vai a lavorare
con python, 

**iv. Routes in Flask**

Il Progetto si divide essenzialmente in 3 grandi sezioni: 
Autenticazione, interfaccia
del sito e infine modifica e renderizzazione dei questionari.\
Per ognuna di queste sezioni, chiamate Blueprint, troviamo
un file `__init__.py` che funge da inizializzazione,
nel secondo file (`forms.py` oppure `errors.py`) troviamo 
utilità come la definizione di classi di dati che le pagine
gestiranno, metodi/funzioni oppure pagine di errore comuni.
Infine, nel file `views.py` troviamo le effettive Routes
che stabiliscono quando e come ciascuna pagina deve
essere visualizzata (per esempio, potremmo voler avere
pagine accessibili solo dopo una 
POST come ad esempio `'/delete/<quiz_id>'`)

**v. Implementazione delle funzioni di Login/Sign-in**

Le funzionalità di Login e Sign-In sono trattate più
nel dettaglio nella sezione 3.ii di questo documento, 
tutte le funzionalità ricollegabili a questa categoria
sono contenute nella Blueprint auth.
Particolare attenzione è stata fatta all'utilizzo di username 
al posto di id per ottenere uno strato di sicurezza aggiuntiva
del server, evitando quindi che un utente malintenzionato
possa trovare gli id degli utenti quando non dovrebbe 
essere in grado di farlo.

ORM gia di suo controlla SQLInj percio è piu
controllo di errore umano

**vi. Analisi dei dati dei questionari**

esperienza utilizzo analisi dei dati (google moduli) view 
delle risposte del questionario (es grafico a torta o percentuali)

**vii. Definizione di ruoli**

I ruoli sono una funzionalità senza dubbio molto efficiente, 
permettono di conferire un gruppo di permessi senza 
doverli impostare manualmente alla creazione di ciascun utente.
Semplicemente, impostando di quali permessi può
godere ogni tipologia di ruolo, basta poi assegnare
quello appropriato nella fase di registrazione.
Nonostante la loro utilità, abbiamo deciso di non utilizzarli per due
ragioni, ciascuna causa e conseguenza dell'altra: 

1) Durante i nostri incontri iniziali per ragionare sulla
struttura del progetto ci siamo resi conto che, sostanzialmente,
i ruoli a noi non sarebbero serviti. Abbiamo strutturato il
sito in modo che gli utenti siano tutti allo stesso livello
per quanto riguarda i permessi (tutti gli utenti possono 
eseguire tutte le operazioni, dalla creazione di nuovi
questionari alla visione e compilazione di quelli altrui).  
Sarebbe stato quindi ridondante creare un singolo ruolo
che non avrebbe nemmeno rappresentato una restrizione di alcun tipo.
2) Heroku, la piattaforma che abbiamo deciso di utilizzare
per lo sviluppo del progetto, non supporta i ruoli come 
funzionalità.  
Anche volendo, quindi non avremmo comunque potuto 
implementarli ma, come illustrato nel punto 1), 
non avendone bisogno non abbiamo sentito la mancanza
di questa funzionalità.

Nonostante tutto, abbiamo comunque deciso di implementare una sorta di 
clone dei ruoli, ovvero abbiamo creato all'interno del database
una tabella chiamata, per l'appunto, ruoli, che 
ne emula le funzionalità e i vantaggi.

### 3. Misure di sicurezza

**i. Hash e passwords**

All'interno del file `models.py` abbiamo creato una
moltitudine di funzioni che ci hanno permesso di gestire
le password e la loro memorizzazione all'interno del database.  
Ogni password viene protetta tramite una funzione hash che
la rende illeggibile agli occhi di malintenzionati, inoltre
abbiamo fatto attenzione che la stessa password salvata 
più volte non riproducesse lo stesso hash proprio per evitare
che multipli utenti che utilizzano la stessa password
potessero rappresentare una debolezza nella sicurezza della
base di dati.

magari mettiamo qualche riga di codice qui come esempio, ci penzo

**ii. Autenticazione e Log-in**

cartella auth, route specifica 
usato username al posto di id per sicurezza aggiuntiva 
del server (cosi uno non puo barare e trovare gli id del
server) 

Cookies (flask_session) validi un anno 

**iii. CSRF, SQL Injection, XSS**

le librerie potrebbero essere vulnerabili ad attacchi nel caso di 
falle, pero sono open source percio lesgoo 

### 4. Sviluppo grafico del sito

La veste grafica della Web Application è stata inizialmente prototipata
su Bootstrap Studio per poi essere esportata direttamente su 
PyCharm, da qui sono state create le varie schermate dell'interfaccia
tramite HTML e CSS.

L'applicazione si suddivide in multiple sezioni:
1) **Pagina iniziale**: Questa è la pagina che viene aperta all'avvio della
web application, il suo unico scopo è di accogliere l'utente o spingerlo
ad accedere/registrarsi, nel caso non lo avesse ancora fatto.  
La web app mantiene l'accesso di un utente (anche se chiude il sito
e lo riapre in seguito) tramite l'utilizzo
di cookies, per la durata di un anno.  
Una volta eseguito l'accesso al sito, l'utente avrà accesso a tutte
le sezioni del sito rimanenti.
2) **"Crea un questionario"**: Cliccando su questo link si verrà indirizzati
ad una pagina dove l'utente avra accesso ad un pulsante per creare 
nuovi quiz (il pulsante aprirà l'editor che permetterà l'inserimento
di un titolo ed una descrizione, in seguito al salvataggio l'utente
potrà continuare la creazione inserendo tutte le domande che vorrà).  
L'utente, inoltre, ha a disposizione una lista di tutti i questionari
che ha già creato, con la possibilità di cancellarli, modificarli oppure
vederne le risposte.
3) **"Compila un questionario"**: Su questa schermata sono visibili i 
questionari creati da altri utenti in modo da poterli compilare.  
Una volta cliccato sul pulsante "Compila", l'utente verrà portato su 
un editor simile a quello di creazione delle domande dove potrà
inserire e salvare la sua risposta.  
Ci sono 4 tipologie di domande supportate dal sito:  
Aperta, ovvero un campo di testo in cui l'utente è libero di
scrivere tutto ciò che vuole;
Scelta, dove l'utente deve selezionare una singola risposta tra quelle
fornite.
Multi-scelta, molto simile a Scelta, qui l'utente può selezionare
multiple risposte invece di una sola;
Numerica, accetta solo risposte numeriche.
4) **"Risposte ai tuoi questionari"**: Da qui, è possibile accedere
direttamente alle risposte fornite dagli utenti sui propri questionari:
Una volta selezionato lo specifico quiz di cui si vogliono visionare i
risultati si avrà la possibilità di visualizzare i risultati 
in due diversi modi,
una visualizzazione suddivisa, dove ogni domanda è separata
e presenta subito sotto una lista delle sue risposte,
oppure una visualizzazione generale suddivisa in due colonne, 
sulla colonna di sinistra troviamo la domanda mentre su quella
a destra abbiamo la risposta ad essa collegata.
Come specificato in precedenza, anche nella schermata
"Crea un questionario" è presente un pulsante "Visualizza risposte" 
che porterà alla medesima schermata di visualizzazione delle risposte
del questionario selezionato.
5) **"Profilo"**: Quest'ultima pagina presenta delle impostazioni per
l'account, come la possibilità di modificare la propria E-Mail oppure il
Nome Utente.