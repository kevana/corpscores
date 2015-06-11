"""
Views for the API
"""

from flask import request

from flask.ext.restless import ProcessingException

from dci_notify.extensions import api_manager
from dci_notify.user.models import CompetitionEvent
from dci_notify.api.funcs import send_scores


def auth_func(*args, **kwargs):
    api_key = api_manager.app.config.get('API_KEY', 'API_KEY')
    data = request.get_json()
    # TODO: Clean up logic, separate 401 and 403 responses.
    if request.headers.get('API_KEY') == api_key:
        return
    if data is None or data['api_key'] != api_key:
        raise ProcessingException(description='Not authenticated!', code=401)
    return True


def post_postprocessor(result=None, **kw):
    """Send scores after a new event has been posted."""
    send_scores(result)


def init_api():
    """
    Flask-Restless is unable to create blueprints (create_api_blueprint)
    before the extension is initialized with an app. Added kludge function to
    defer creation in app.py Remove as soon as this is fixed

    Ref: https://github.com/jfinkels/flask-restless/issues/397
    """
    api_manager.create_api(CompetitionEvent,
                       collection_name='events',
                       methods=['GET', 'POST'],
                       preprocessors={
                           'GET_SINGLE': [auth_func],
                           'GET_MANY': [auth_func],
                           'POST': [auth_func]
                       },
                       postprocessors={
                           'POST': [post_postprocessor]
                       })
