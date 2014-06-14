# -*- coding: utf-8 -*-
'''The admin module, containing Flask-Admin.'''
from flask.ext.login import current_user
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from dci_notify.extensions import db
from dci_notify.user.models import Role, User


class MyView(ModelView):
    column_exclude_list = ('password')

    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_admin)

admin = Admin()
admin.add_view(MyView(Role, db.session))
admin.add_view(MyView(User, db.session))
