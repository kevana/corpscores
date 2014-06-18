# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField, TextField, SelectMultipleField
from wtforms.validators import DataRequired, Length

from dci_notify.user.models import User


class SendMessageForm(Form):
    users = SelectMultipleField('Send to', coerce=int,
                                validators=[DataRequired()])
    message = TextAreaField('Message',
                            validators=[DataRequired(), Length(max=160)])

    def __init__(self, *args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        user_tuples = [(user.id, user.full_name)
                       for user in User.query.filter_by(phone_active=True)]
        self.users.choices = user_tuples

    def validate(self):
        initial_validation = super(SendMessageForm, self).validate()
        if not initial_validation:
            return False
        self.users_list = [User.get_by_id(idx) for idx in self.users.data]
        return True
