# -*- coding: utf-8 -*-
'''SMS tests'''
import pytest


from dci_notify.extensions import mail
from dci_notify.sms import split_msg, send_sms


class TestSplitMessage:

    def test_split_msg_one_chunk(self):
        short_msg = 'a' * 150
        chunks = split_msg(short_msg)
        assert len(chunks) is 1

    def test_split_msg_multi_chunk(self):
        short_msg = 'a' * 500
        chunks = split_msg(short_msg)
        assert len(chunks) is 4


class TestSendMessage:

    def test_send_sms_single_message(self, app):
        with mail.record_messages() as outbox:
            send_sms(carrier='verizon',
                     number=5551112222,
                     message='message',
                     subject='subject')
            assert len(outbox) is 1
            assert outbox[0].subject == 'subject'
            assert outbox[0].body == 'message'

    def test_send_sms_multiple_messages(self, app):
        with mail.record_messages() as outbox:
            send_sms(carrier='verizon',
                     number=5551112222,
                     message='m' * 300,
                     subject='subject')
            assert len(outbox) is 2
            assert outbox[0].subject == 'subject'
            assert outbox[0].body == 'm' * 159

    def test_send_sms_with_conn(self, app):
        with mail.record_messages() as outbox:
            with mail.connect() as conn:
                send_sms(carrier='verizon',
                         number=5551112222,
                         message='m' * 300,
                         subject='subject',
                         conn=conn)
            assert len(outbox) is 2
