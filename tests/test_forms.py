# -*- coding: utf-8 -*-
'''
Form tests.
'''

from dci_notify.admin.forms import SendMessageForm
from dci_notify.public.forms import LoginForm
from dci_notify.user.forms import RegisterForm


class TestRegisterForm:

    def test_validate_user_already_registered(self, user):
        # Enters username that is already registered
        form = RegisterForm(username=user.username, email='foo@bar.com',
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example')

        assert form.validate() is False
        assert 'Username already registered' in form.username.errors

    def test_validate_email_already_registered(self, user):
        # enters email that is already registered
        form = RegisterForm(username='unique', email=user.email,
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example')

        assert form.validate() is False
        assert 'Email already registered' in form.email.errors

    def test_validate_phone_already_registered(self, user):
        # Enters phone number that is already registered
        form = RegisterForm(username='unique', email='foo@bar.com',
                            carrier='at&t', phone_num=user.phone_num,
                            password='example', confirm='example')

        assert form.validate() is False
        assert 'Phone number already registered' in form.phone_num.errors

    def test_validate_strings_too_long(self, user):
        # Username
        form = RegisterForm(username='u'*81, email='foo@bar.com',
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example')
        assert form.validate() is False
        assert 'Field must be between 3 and 25 characters long.' in form.username.errors
        # Email
        form = RegisterForm(username='unique', email='foo@'+'bar'*25+'.com',
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example')
        assert form.validate() is False
        assert 'Field must be between 6 and 40 characters long.' in form.email.errors
        # First Name
        form = RegisterForm(username='unique', email='foo@bar.com',
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example',
                            first_name='a'*100)
        assert form.validate() is False
        assert 'Field cannot be longer than 30 characters.' in form.first_name.errors
        # Last Name
        form = RegisterForm(username='unique', email='foo@bar.com',
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example',
                            last_name='a'*100)
        assert form.validate() is False
        assert 'Field cannot be longer than 30 characters.' in form.last_name.errors
        # Corps
        form = RegisterForm(username='unique', email='foo@bar.com',
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example',
                            corps='a'*100)
        assert form.validate() is False
        assert 'Field cannot be longer than 80 characters.' in form.corps.errors
        # Phone number
        form = RegisterForm(username='unique', email='foo@bar.com',
                            carrier='at&t', phone_num='55512345671111111',
                            password='example', confirm='example',
                            first_name='a'*100)
        assert form.validate() is False
        assert 'Field must be between 10 and 10 characters long.' in form.phone_num.errors

    def test_validate_success_no_names(self, db):
        form = RegisterForm(username='newusername', email='new@test.test',
                            carrier='at&t', phone_num='5551234567',
                            password='example', confirm='example')
        assert form.validate() is True

    def test_validate_success_with_names(self, db):
        form = RegisterForm(username='newusername', email='new@test.test',
                            carrier='at&t', phone_num='5551234567',
                            first_name='John', last_name='Smith',
                            password='example', confirm='example',
                            corps='Bluecoats')
        assert form.validate() is True


class TestLoginForm:

    def test_validate_success(self, user):
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is True
        assert form.user == user

    def test_validate_unknown_username(self, db):
        form = LoginForm(username='unknown', password='example')
        assert form.validate() is False
        assert 'Unknown username' in form.username.errors
        assert form.user is None

    def test_validate_invalid_password(self, user):
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='wrongpassword')
        assert form.validate() is False
        assert 'Invalid password' in form.password.errors

    def test_validate_inactive_user(self, user):
        user.active = False
        user.set_password('example')
        user.save()
        # Correct username and password, but user is not activated
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is False
        assert 'User not activated' in form.username.errors


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
