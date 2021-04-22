from sources import create_app

app = create_app()

# la seguente parte di programma viene eseguita solo se il nome del file a runtime è __main__
if __name__ == "__main__":
    # debug=True fornisce messaggi di output del server più dettagliati
    # FIXME: quando la webapp viene confezionata per l'uso bisogna togliere la modalità debug
    app.run(debug=True)
