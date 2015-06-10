# -*- coding: utf-8 -*-
'''
Public section, including homepage and signup.
'''

from flask import (Blueprint, render_template, send_from_directory)
from dci_notify.extensions import login_manager
from dci_notify.user.models import User

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(userId):
    '''Load a user based on their unique ID.'''
    return User.get_by_id(int(userId))


@blueprint.route("/", methods=["GET"])
def home():
    return render_template("public/home.html")



@blueprint.route("/about/")
def about():
    return render_template("public/about.html")


@blueprint.route("/humans.txt")
def humans():
    return send_from_directory(blueprint.static_folder, "humans.txt")
