# -*- coding: utf-8 -*-
'''
API tests.
'''

import json
import pytest

from dci_notify.api import send_scores
from dci_notify.scraper.scraper import eqIn
from .factories import UserFactory


VALID_EVENT = '''
{
  "api_key": "API_KEY",
  "city": "Mesa",
  "date": "2014-06-26T00:00:00",
  "name": "Southwest Corps Connection ",
  "results": [
    {
      "corps": "Santa Clara Vanguard",
      "place": "1",
      "score": "74.200"
    },
    {
      "corps": "Blue Knights",
      "place": "2",
      "score": "70.000"
    },
    {
      "corps": "Crossmen",
      "place": "3",
      "score": "66.600"
    },
    {
      "corps": "The Academy",
      "place": "4",
      "score": "63.800"
    }
  ],
  "state": "AZ"
}
'''


class TestHelpers:
    '''Tests for helper methods.'''
    def test_eqIn(self):
        assert eqIn(5, [4, 5])
        assert eqIn(5, set([4, 5]))
        assert eqIn(u'5', ['5'])
        assert eqIn(u'5', [u'4', u'5'])

    def test_not_eqIn(self):
        assert not eqIn(2, [5])
        assert not eqIn('5', ['3'])
        assert not eqIn(u'3', [u'5'])

    @pytest.mark.xfail  # TODO: Failing due to DB mocking problem
    def test_send_scores(self, user, db, app):
        mail = app.extensions['mail']
        event = json.loads(VALID_EVENT)
        with mail.record_messages() as outbox:
            send_scores(event)
            assert len(outbox) != 0


class TestRoutes:
    @pytest.mark.xfail
    def test_events_empty_post(self, app, testapp):
        res = testapp.post('/events/', expect_errors=True)
        assert res.status_code == 403

    # Malformed json
    @pytest.mark.xfail
    def test_events_missing_key(self, app, testapp):
        pass

    # Working example
    @pytest.mark.xfail
    def test_events_success(self, app, db, testapp, user):
        mail = app.extensions['mail']
        user.save() # Commit to test db
        user_two = UserFactory()
        print(user)
        url = '/events/'
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        with mail.record_messages() as outbox:
            r = testapp.post(url, VALID_EVENT, headers=headers)
            assert r.status_code == 200
            # assert len(outbox) == 3
