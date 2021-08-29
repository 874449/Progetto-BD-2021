#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Questionario, Domanda, RispostaDomanda, CategoriaDomanda, TipologiaDomanda, \
    PossibileRisposta, RisposteQuestionario
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


# make_shell_context dà la possibilità di interfacciarsi con l'applicazione da CLI con il comando flask shell
# gli oggetti importati nel dizionario saranno visibili nella shell senza dover fare alcun import
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Questionario=Questionario, Role=Role,
                Domanda=Domanda, RispostaDomanda=RispostaDomanda, CategoriaDomanda=CategoriaDomanda,
                TipologiaDomanda=TipologiaDomanda, PossibileRisposta=PossibileRisposta,
                RisposteQuestionario=RisposteQuestionario)


# le funzioni wrappate da 'utility_processor' servono a rendere disponibili dei metodi/funzioni
# personalizzate per l'ambiente di jinja
@app.context_processor
def utility_processor():
    def to_str(x):
        return str(x)
    return dict(to_str=to_str)


@app.context_processor
def utility_processor():
    def getter(x, y):
        return getattr(x, y)
    return dict(getter=getter)


# la seguente parte di programma viene eseguita solo se il nome del file a runtime è __main__
if __name__ == "__main__":
    app.run()
