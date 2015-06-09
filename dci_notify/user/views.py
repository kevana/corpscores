# -*- coding: utf-8 -*-
'''
Views for the user module of CorpScores.
'''

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required
from dci_notify.user.forms import PhoneNotificationForm
from dci_notify.utils import flash_errors
from flask.ext.login import current_user

blueprint = Blueprint('user', __name__, url_prefix='/users',
                      static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def members():
    form = PhoneNotificationForm(request.form)
    if form.validate_on_submit():
        current_user.phone_active = form.phoneEnabled.data
        current_user.save()
        status = 'enabled' if form.phoneEnabled.data else 'disabled'
        flash('Phone notifications have been {}.'.format(status), 'success')
    else:
        flash_errors(form)
        # Set current state of form
        form.phoneEnabled.data = current_user.phone_active

    return render_template('users/members.html', form=form)
