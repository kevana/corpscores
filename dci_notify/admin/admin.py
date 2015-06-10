# -*- coding: utf-8 -*-
'''
The admin module, containing Flask-Admin.
'''

from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from dci_notify.admin.forms import SendMessageForm
from dci_notify.extensions import db
from dci_notify.sms import send_sms
from dci_notify.user.models import Role, User, CompetitionEvent
from dci_notify.utils import flash_errors


def send_messages(users, message):
    '''Send a message to specified users.'''
    for user in users:
        send_sms(user.carrier, user.phone_num, message)


class MyView(ModelView):
    '''Authenticated-required view for database models.'''
    column_exclude_list = ('password')

    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_admin)


class MyBaseView(BaseView):
    '''Admin view for sending SMS messages to users.'''
    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_admin)

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = SendMessageForm()
        if form.validate_on_submit():
            send_messages(form.users_list, form.message.data)
        else:
            flash_errors(form)
        return self.render('admin/message.html', form=form)


admin = Admin()
admin.add_view(MyBaseView(name='Message', endpoint='message'))
admin.add_view(MyView(Role, db.session))
admin.add_view(MyView(User, db.session))
admin.add_view(MyView(CompetitionEvent, db.session))
