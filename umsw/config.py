# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~~~

    Default configuration

    :copyright: (c) 2013 ParsPooyesh Co
"""

class DefaultConfig(object):
    """
    Default configuration for a newsmeme application.
    """

    DEBUG = True

    # change this in your production settings !!!

    SECRET_KEY = "secret"

    ADMINS = ()

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'

    ACCEPT_LANGUAGES = ['en', 'fa']
