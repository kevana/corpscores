# -*- coding: utf-8 -*-
'''
Form tests.
'''

from dci_notify.admin.forms import SendMessageForm


class TestSendMessageForm:

    def test_validate_no_recipients_selected(self, user):
        pass
        form = SendMessageForm(message='Test Message')
        assert form.validate() is False
        assert 'This field is required.' in form.users.errors

    def test_validate_empty_message(self, user):
        form = SendMessageForm(users=[user.id])
        assert form.validate() is False
        assert 'This field is required.' in form.message.errors

    def test_validate_success(self, user):
        form = SendMessageForm(users=[user.id], message='Test')
        form.users.choices = [(user.id, user.full_name)]
        assert form.validate() is True
        assert user in form.users_list
