# Progetto di Basi di Dati A.A. 2020-2021


Gruppo: Montin - Spanio - Zanin

> Progetto di gestione di DB con flask.

## App in fase di sviluppo 🔨🔨🔨:
## Contenuti

- [come lanciare il server](#istruzioni)
- [Struttura progetto](#struttura-applicazione)
- [Flask migrate](#Flask-migrate)
- [Risorse esterne](#Risorse-esterne):
    - [Flask](#flask)
    - [SQL](#sql)

## Setup e primo avvio del server
per fare il setup dell'applicazione da CLI eseguire i seguenti comandi:

Per prima cosa bisogna installare le librerie su cui si basa l'applicazione:

```shell
pip install -r requirements.txt
```

Poi configurare le variabili d'ambiente che utilizza flask per lanciare l'applicazione 

Windows CMD:
```windowscmd
set FLASK_APP = runner.py
set FLASK_ENV = development
set FLASK_DEBUG = 1
```

UNIX like os:
```shell
export FLASK_APP = runner.py
export FLASK_ENV = development
export FLASK_DEBUG = 1
```

Poi è necessario creare le tabelle del database

```shell
flask create_tables
```

Infine si può lanciare l'applicazione con

```shell
flask run
```

## Struttura-applicazione

```
Progetto-BD-2021/
    | app/
        | auth/
            | __init__.py
            | forms.py
            | views.py
        | main/
            | __init__.py
            | errors.py
            | views.py
        | quiz/
            | __init__.py
            | forms.py
            | views.py
        | static/
        | templates/
        | __init__.py
        | commands.py
        | models.py
    config.py
    README.md
    requirements.txt
    runner.py
```
L'applicazione è divisa in più blueprint che raggruppano per argomento le 'routes' di flask.

Il file `requirements.txt` è una fotografia dei pacchetti contenuti nel virtual enviroment, man mano che l'applicazione
crescerà va aggiornato con i moduli (o package) importati. Per crearlo o aggiornarlo basterà eseguire il comando
```shell
pip freeze > requirements.txt
```


## Flask-migrate

Per creare le tabelle dal contesto dell'applicazione basta dare in input i seguenti comandi al terminale:

```shell
flask db init
flask db migrate
flask db upgrade
```

così facendo verrà creata la cartella migrations dove vengono salvati gli status del db ed è possibile tornare a una versione precedente in caso di errori.

Per ogni modifica successiva al file models.py basterà dare il comando `flask upgrade`. 

## Risorse-esterne
### Flask
Harvard CS50 - 
https://www.youtube.com/watch?v=YoXxevp1WRQ&list=PLhQjrBD2T382_R182iC2gNZI9HzWFMC_8

L'editor online del CS50 con setup per flask funzionante 'out-of-the-box': https://ide.cs50.io/

è molto comodo perchè supporta la modalità di editing simultaneo sullo stesso documento (tipo google docs)

### SQL
Le lezioni del CS50 comprendono anche SQL