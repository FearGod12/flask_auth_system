#!/usr/bin/python3
"""API blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/')

# import all relavant routes defined within api.v1.views
from api.views.books import *  # noqa
from api.views.users import *  # noqa

