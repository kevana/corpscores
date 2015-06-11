# -*- coding: utf-8 -*-
"""
API functions for CorpScores.
"""

from datetime import datetime
import time

from flask import (render_template_string)
from flask.ext.mail import Message

from dci_notify.async import async
from dci_notify.extensions import mail
from dci_notify.sms import send_sms
from dci_notify.user.models import User

score_template = '''{{event.name}} - {{event.date.strftime('%b %d')}}, {{event.city}} {{event.state}}
{% for corp in event.results -%}
{{corp.place}}. {{corp.score}}-{{corp.corps}}
{% endfor %}'''


@async
def async_send_scores(message):
    """Send message to all users with active phones and a summary to """
    # Super simple profiling
    start_time = time.time()

    with mail.app.app_context():
        with mail.connect() as conn:
            for user in User.query.filter_by(phone_active=True):
                send_sms(user.carrier, user.phone_num, message, conn=conn)
        num_users = len(User.query.filter_by(phone_active=True).all())

    elapsed_time = time.time() - start_time
    admin_msg = Message('CorpScores Event Stats',
                        sender=mail.app.config.get('SMS_DEFAULT_SENDER'),
                        recipients=mail.app.config.get('ADMINS'))
    admin_msg.body = '''
    Total Users: %d
    Message Length: %d
    Message: %s
    Elapsed time: %f''' % (num_users,
                           len(message),
                           message,
                           elapsed_time)
    with mail.app.app_context():
        mail.send(admin_msg)


def send_scores(data):
    """Create a message from the given data and send it asynchronously."""
    date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
    data['date'] = date
    msg = render_template_string(score_template, event=data)

    async_send_scores(message=msg)
