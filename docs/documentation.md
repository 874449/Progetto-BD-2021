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
interfacciarsi con semplicità ed efficacia allo sviluppo del progetto. 
Il codice è stato condiviso tra i vari membri del gruppo tramite
GitHub in modo che ognuno potesse lavorare sulla versione più recente
possibile, inoltre il database è stato condiviso tramite Heroku, che
ha permesso a tutti i membri di lanciare l'applicazione usando lo
stessa base di dati per la fase di testing.
Il gruppo ha inoltre deciso di creare un gruppo Whatsapp dedicato al
progetto in cui tutti i membri erano sempre raggiungibili per 
eventuale necessità

libro mighel 

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

file diviso in blueprint, init.py principale, la dentro
si crea una funzione crea applicazione che inizializza
le librerie utili all-utilizzo e si registrano le 
bleuprint. logicamente diviso in multiple blueprint 

auth autenticazione

main interfaccia utente di base

quiz editor questionari renderizzazione questionari

rimozione domande

errors.py per gli errori piu ricorrenti

**v. Implementazione delle funzioni di Login/Sign-in**

accenno e basta e poi spiego
dall'altra parte
cartella auth, route specifica 
usato username al posto di id per sicurezza aggiuntiva 
del server (cosi uno non puo barare e trovare gli id del
server) 

ORM gia di suo controlla SQLInj percio è piu
controllo di errore umano

**vi. Analisi dei dati dei questionari**

esperienza utilizzo analisi dei dati (google moduli) view 
delle risposte del questionario (es grafico a torta o percentuali)

**vii. Definizione di ruoli**

heroku non permette ruoli percio non li abbiamo creati,
abbiamo tabella ruoli in database che clona questa
funzionalità

### 3. Misure di sicurezza

**i. Hash e passwords**

un sacco di funzioni per gestire le passwords degli utenti
in models, passwords hashate per protezione degli utenti
due volte stessa password non riproduce stesso hash
classe users password hash crittografia particolare

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
tramite HTML e CSS

macro 

