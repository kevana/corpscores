# -*- coding: utf-8 -*-
'''
Forms for the user module of CorpScores.
'''

from flask_wtf import Form
from wtforms import PasswordField, SelectField, TextField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User
from dci_notify.sms import carrier_form_tuples

# Sort carriers
carrier_form_tuples.sort(key=lambda tup: tup[1])
# First entry must be empty for Chosen.js to display default text
carrier_form_tuples.insert(0, ('',''))


class RegisterForm(Form):
    '''Form for new user registration.'''
    username = TextField('Username',
                         validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                      validators=[DataRequired(),
                                  Email(),
                                  Length(min=6, max=40)])
    first_name = TextField('First Name', validators=[Length(max=30)])
    last_name = TextField('Last Name', validators=[Length(max=30)])
    corps = TextField('Corps', validators=[Length(max=80)])
    carrier = SelectField('Carrier',
                          choices=carrier_form_tuples,
                          validators=[DataRequired()])
    phone_num = TextField('Phone Number',
                          validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=40)])
    confirm = PasswordField('Verify Password',
                            [DataRequired(),
                             EqualTo('password',
                                     message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        '''Validate the new user registration form.'''
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        user = User.query.filter_by(phone_num=self.phone_num.data).first()
        if user:
            self.phone_num.errors.append("Phone number already registered")
            return False
        return True

class PhoneNotificationForm(Form):
    """Form for toggling phone notifications."""
    phoneEnabled = BooleanField('Enable phone notifications')