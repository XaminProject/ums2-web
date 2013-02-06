# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Module, request, url_for, \
    render_template
from redis import *
from umsw.defaults import pool, REDIS_PREFIX, ADDED_LIST, \
    DL_LIST, ADDED_POSTFIX, BUILD_LIST, SLAVE_PREFIX
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


@index.route('/added')
@index.route('/added/<int:page>')
def show_added(page=1):

    r = Redis(connection_pool=pool)
    all_data = r.smembers(ADDED_LIST)

    count = 0;
    added = {}
    for pkg in all_data:
        added[pkg] = r.hgetall(pkg)
    return render_template('added.html', data=added)

@index.route('/list-dl')
def download_list():

    r = Redis(connection_pool=pool)
    all_data = r.lrange(DL_LIST, 0, r.llen(DL_LIST) + 1)
    count = 0;
    added = {}
    for pkg in all_data:
        x = -len(ADDED_POSTFIX)
        pkg = pkg[:x]
        added[pkg] = r.hgetall(pkg)
    return render_template('listdl.html', data=added)


@index.route('/list-build')
def build_list():

    r = Redis(connection_pool=pool)
    all_data = r.lrange(BUILD_LIST, 0, r.llen(BUILD_LIST) + 1)
    added = {}
    x = -len(ADDED_POSTFIX)
    for pkg in all_data:
        pkg = pkg[:x]
        added[pkg] = r.hgetall(pkg)
    return render_template('listbuild.html', data=added)


@index.route('/slaves')
def slave_list():

    r = Redis(connection_pool=pool)
    all_data = r.keys(SLAVE_PREFIX + '*')

    added = {}
    x = -len(ADDED_POSTFIX)
    for key in all_data:
        pkg = r.get(key)
        pkg = pkg[:x]
        key = key[len(SLAVE_PREFIX):]
        added[key] = r.hgetall(pkg)
    return render_template('slaves.html', data=added)
