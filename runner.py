#!/usr/bin/env python
import os
from app import create_app, db
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


# la seguente parte di programma viene eseguita solo se il nome del file a runtime è __main__
if __name__ == "__main__":
    # debug=True fornisce messaggi di output del server più dettagliati
    # FIXME: quando la webapp viene confezionata per l'uso bisogna togliere la modalità debug
    app.run(debug=True)
