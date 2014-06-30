# -*- coding: utf-8 -*-
'''API Module for CorpScores.'''

from flask import (abort, Blueprint, request, render_template, flash,
                   make_response, url_for, redirect, session, jsonify,
                   render_template_string)
from flask.ext.login import current_user
from flask.ext.mail import Message
from sqlalchemy.dialects.postgresql import JSON
# Imports for profiling
import time
from dci_notify.extensions import mail

from datetime import datetime
from dci_notify.async import async
from dci_notify.database import SurrogatePK
from dci_notify.extensions import db
from dci_notify.database import (
    Column,
    db,
    Model,
    SurrogatePK
)
from dci_notify.user.models import User
from pprint import pprint
from dci_notify.sms import send_sms

api_key = '1F4F320E-66A0-4F14-BA09-CBA22F1F9CE9'

score_template = '''{{event.name}} - {{event.date.strftime('%b %d')}}, {{event.city}} {{event.state}}
{% for corp in event.results -%}
{{corp.place}}. {{corp.score}}-{{corp.corps}}
{% endfor %}'''

@async
def async_send_scores(message):
    # Super simple profiling
    start_time = time.time()

    with mail.app.app_context():
        with mail.connect() as conn:
            for user in User.query.filter_by(phone_active=True):
                send_sms(user.carrier, user.phone_num, message, conn=conn)
        num_users = len(User.query.filter_by(phone_active=True).all())

    elapsed_time = time.time() - start_time
    admin_msg = Message('CorpScores Event Stats',
                        sender=mail.app.config['SMS_DEFAULT_SENDER'],
                        recipients=['ahlqu039@umn.edu'])
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
    date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
    data['date'] = date
    msg = render_template_string(score_template, event=data)

    async_send_scores(message=msg)


#class Event(SurrogatePK, Model):
#    __tablename__ = 'events'
#    '''Model for storing DCI Event results.'''
#    blob = Column(JSON, nullable=False)
#    blob = Column()
#
#    def __init__(self, blob, **kwargs):
#        db.Model.__init__(self, blob=blob, **kwargs)
#

blueprint = Blueprint('api', __name__, static_folder="../api")


@blueprint.errorhandler(400)
def bad_request(e):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@blueprint.errorhandler(404)
def unauthorized(e):
    return make_response(jsonify({'error': 'Unauthorized'}), 403)


@blueprint.before_request
def check_api_key():
    data = request.get_json()
    if data is None or data['api_key'] != api_key:
        abort(403)


@blueprint.route('/events/', methods=['GET'])
def get_events():
    return 'unimplemented'  # return jsonify(Event.query.all()), 200


@blueprint.route('/events/', methods=['POST'])
def post_event():
    data = request.get_json()
    if not request.json or not all(x in data for x in ('city', 'state', 'date',
                                                       'name', 'results')):
        abort(400)
    send_scores(data)
    return make_response(jsonify({'status': 'OK'}), 200)


@blueprint.route('/events/<id>', methods=['GET'])
def get_event(id):
    pass


@blueprint.route('/events/<id>', methods=['PUT'])
def put_event(id):
    pass


@blueprint.route('/events/<id>', methods=['DELETE'])
def del_event(id):
    pass
