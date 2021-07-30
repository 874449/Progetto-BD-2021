# Progetto di Basi di Dati A.A. 2020-2021


Gruppo: Montin - Spanio - Zanin

> Progetto di gestione di DB con flask.

### App in fase di sviluppo 🔨🔨🔨:
il file `requirements.txt` è una fotografia dei pacchetti contenuti nel virtual enviroment, man mano che l'applicazione crescerà va aggiornato con i moduli (o package) importati

## Contenuti

- [come lanciare il server](#istruzioni)
- [Struttura progetto](#struttura-applicazione)
- [Flask migrate](#Flask-migrate)
- [Risorse esterne](#Risorse-esterne):
    - [Flask](#flask)
    - [SQL](#sql)

## Istruzioni
per lanciare l'applicazione da CLI eseguire i seguenti comandi:

Windows CMD:
```windowscmd
> set FLASK_APP=runner
> flask run
```

Windows PowerShell:
```PowerShell
> $env:FLASK_APP = "runner"
> flask run
```

UNIX like os:
```shell
$ export FLASK_APP=runner
$ flask run
```
oppure
```shell
$ python runner.py
```

## Struttura-applicazione

```
Progetto-BD-2021/
    | sources/
        | auth/
            | __init__.py
            | forms.py
            | views.py
        | main/
            | __init__.py
            | errors.py
            | views.py
        | static/
        | templates/
        | __init__.py
        | models.py
    README.md
    requirements.txt
    runner.py
```

## Flask-migrate

Per creare le tabelle dal contesto dell'applicazione basta dare in input i seguenti comandi al terminale:

```shell
flask db init
flask db migrate
flask db update
```

così facendo verrà creata la cartella migrations dove vengono salvati gli status del db ed è possibile tornare a una versione precedente in caso di errori.

Per ogni modifica successiva al file models.py basterà dare il comando `flask update`. 

## Risorse-esterne
### Flask
Harvard CS50 - 
https://www.youtube.com/watch?v=YoXxevp1WRQ&list=PLhQjrBD2T382_R182iC2gNZI9HzWFMC_8

L'editor online del CS50 con setup per flask funzionante 'out-of-the-box': https://ide.cs50.io/

è molto comodo perchè supporta la modalità di editing simultaneo sullo stesso documento (tipo google docs)

### SQL
Le lezioni del CS50 comprendono anche SQL