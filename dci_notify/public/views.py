# -*- coding: utf-8 -*-
'''
Public section, including homepage and signup.
'''

from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, send_from_directory)
from flask.ext.login import login_user, login_required, logout_user

from dci_notify.extensions import login_manager
from dci_notify.user.models import User
from dci_notify.public.forms import LoginForm
from dci_notify.user.forms import RegisterForm
from dci_notify.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(userId):
    '''Load a user based on their unique ID.'''
    return User.get_by_id(int(userId))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    corps=form.corps.data,
                    password=form.password.data,
                    carrier=form.carrier.data,
                    phone_num=form.phone_num.data,
                    phone_active=True,
                    active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route("/humans.txt")
def humans():
    return send_from_directory(blueprint.static_folder, "humans.txt")
