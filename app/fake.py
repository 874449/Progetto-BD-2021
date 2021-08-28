from random import randint
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Questionario, Domanda


def users(count=100):
    fake = Faker('it_IT')
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 first_name=fake.first_name(),
                 last_name=fake.last_name(),
                 location=fake.city(),
                 member_since=fake.past_date(),
                 last_seen=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def questionari(count=100):
    fake = Faker('it_IT')
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        q = Questionario(uuid=uuid4(),
                         title=fake.catch_phrase(),
                         description=fake.sentence(),
                         timestamp=fake.past_date(),
                         author_id=u.id)
        db.session.add(q)
        db.session.commit()
        for j in range(randint(1, 10)):
            d = Domanda(text=fake.text(), quiz_id=q.id, type_id=1)
            db.session.add(d)
            db.session.commit()
    db.session.commit()

