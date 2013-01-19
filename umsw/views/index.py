# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Module, request, url_for, \
    render_template
from redis import *
from umsw.defaults import pool, REDIS_PREFIX
from json import dumps, loads

index = Module(__name__)


@index.route('/')
def index_page():
    return render_template('index.html')


@index.route('/sources')
def show_sources():

    r = Redis(connection_pool=pool)
    all_data = r.get(REDIS_PREFIX + 'sources')
    if not all_data:
        all_data = {}
    else:
        all_data = loads(all_data)

    return render_template('sources.html', data=all_data)
