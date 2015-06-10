# -*- coding: utf-8 -*-
'''
Models for the user module of CorpScores.
'''

import datetime as dt

from flask.ext.security import UserMixin, RoleMixin

from dci_notify.extensions import bcrypt
from dci_notify.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)
from dci_notify.sms import carrier_slugs, send_sms


class Role(SurrogatePK, Model, RoleMixin):
    '''Role database model.'''
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False) # Flask-Security wants name and description fields
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    '''User database model.'''
    __tablename__ = 'users'
    username = Column(db.String(80), nullable=True)
    email = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    corps = Column(db.String(80), nullable=True)
    carrier = Column(db.Enum(*carrier_slugs, name='Carriers'), nullable=True)
    phone_num = Column(db.String(10), unique=True, nullable=True)
    phone_active = Column(db.Boolean(), default=False)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, email, **kwargs):
        db.Model.__init__(self, email=email, phone_active=True, **kwargs)
        # Send SMS confirmation message
        message = 'You are now signed up for CorpScores. To disable SMS visit https://corpscores.herokuapp.com/users/'
        if self.carrier and self.phone_num and self.phone_active:
            send_sms(self.carrier, self.phone_num, message)


    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({email!r})>'.format(email=self.email)


class CompetitionEvent(SurrogatePK, Model):
    __tablename__ = 'competition_events'
    uuid = Column(db.String(), unique=True, nullable=False)
    name = Column(db.String())
    date = Column(db.String())
    city = Column(db.String())
    state = Column(db.String())

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<CompetitionEvent({name})>'.format(name=self.name)
