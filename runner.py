#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Questionario, Domanda, RispostaDomanda, CategoriaDomanda, TipologiaDomanda, \
    PossibileRisposta, RisposteQuestionario
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Questionario=Questionario, Role=Role,
                Domanda=Domanda, RispostaDomanda=RispostaDomanda, CategoriaDomanda=CategoriaDomanda,
                TipologiaDomanda=TipologiaDomanda, PossibileRisposta=PossibileRisposta,
                RisposteQuestionario=RisposteQuestionario)


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
