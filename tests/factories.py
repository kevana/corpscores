# -*- coding: utf-8 -*-
'''
Object factories for testing.
'''

from factory import Sequence, PostGenerationMethodCall
from factory.alchemy import SQLAlchemyModelFactory
from random import randint

from dci_notify.user.models import User
from dci_notify.database import db


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        session = cls.FACTORY_SESSION
        obj = target_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    phone_num = Sequence(lambda n: '555' + str(randint(1000000, 9999999)))
    carrier = 'at&t'
    password = PostGenerationMethodCall('set_password', 'example')
    active = True
    #phone_active = True
