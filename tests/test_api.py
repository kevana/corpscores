# -*- coding: utf-8 -*-
'''API tests.'''
import json
import pytest

from dci_notify.scraper.scraper import eqIn
from dci_notify.api import send_scores

VALID_EVENT = '''
{
  "api_key": "password",
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


# Helpr functions
class TestHelpers:

    def test_eqIn(self):
        assert eqIn(5, [4, 5])
        assert eqIn(5, set([4, 5]))
        assert eqIn(u'5', ['5'])
        assert eqIn(u'5', [u'4', u'5'])

    def test_not_eqIn(self):
        assert not eqIn(2, [5])
        assert not eqIn('5', ['3'])
        assert not eqIn(u'3', [u'5'])

    def test_send_scores(self, db, app):
        mail = app.extensions['mail']
        event = json.loads(VALID_EVENT)
        with mail.record_messages() as outbox:
            send_scores(event)
            assert len(outbox) != 0
            print(outbox[0].body)


class TestRoutes:

    def test_events_empty_post(self, app, testapp):
        res = testapp.post('/events/', expect_errors=True)
        assert res.status_code == 403

    # Malformed json

    def test_events_missing_key(self, app, testapp):
        pass

    # Working example
