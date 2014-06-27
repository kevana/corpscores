# -*- coding: utf-8 -*-
'''API tests.'''
import pytest

from dci_notify.scraper.scraper import eqIn


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


class TestRoutes:

    def test_events_empty_post(self, app, testapp):
        res = testapp.post('/events/', expect_errors=True)
        assert res.status_code == 403

    # Malformed json
    
    def test_events_missing_key(self, app, testapp):
        pass

    # Working example
