# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Module, request, url_for, \
    render_template


index = Module(__name__)

@index.route('/')
def index_page():
    return render_template('index.html')
