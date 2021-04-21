# Progetto di Basi di Dati A.A. 2020-2021


Gruppo: Montin - Spanio - Zanin

> Progetto di gestione di DB con flask.

### App in fase di sviluppo 🔨🔨🔨:
il file `requirements.txt` è una fotografia dei pacchetti contenuti nel virtual enviroment, man mano che l'applicazione crescerà va aggiornato con i moduli (o package) importati

## Contenuti

- [come lanciare il server](#istruzioni)
- [Struttura progetto](#struttura dell'applicazione)
- Risorse esterne:
    - [Flask](#Risorse da consultare per Flask)
    - [SQL](#sql)

### Istruzioni
per lanciare l'applicazione da CLI eseguire i seguenti comandi:

Windows CMD:
```windowscmd
> set FLASK_APP=hello
> flask run
```

Windows PowerShell:
```PowerShell
> $env:FLASK_APP = "hello"
> flask run
```

UNIX like os:
```shell
$ export FLASK_APP=hello
$ flask run
```

## Struttura dell'applicazione

```
Progetto-BD-2021/
    | sources/
        | app/
            | __init__.py
            | auth.py
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



## Risorse da consultare per Flask
Harvard CS50 - 
https://www.youtube.com/watch?v=YoXxevp1WRQ&list=PLhQjrBD2T382_R182iC2gNZI9HzWFMC_8

L'editor online del CS50 con setup per flask funzionante 'out-of-the-box': https://ide.cs50.io/

è molto comodo perchè supporta la modalità di editing simultaneo sullo stesso documento (tipo google docs)

## SQL
Le lezioni del CS50 comprendono anche SQL