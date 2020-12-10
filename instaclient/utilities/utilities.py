"""This module contains utilities used by the InstaClient"""
import functools
from functools import wraps
import logging
import time
import random

""" def get_logger(debug=False):
    Creates a logging object and returns it

    Returns:
        logger:logging.Log: Log object

    loglevel = logging.DEBUG if debug else logging.INFO
    l = logging.getLogger(__name__)
    if not getattr(l, 'handler_set', None):
        l.setLevel(loglevel)
        h = logging.StreamHandler()
        f = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        h.setFormatter(f)
        l.addHandler(h)
        l.setLevel(loglevel)
        l.handler_set = True
    return l   """


def get_url(url, scraperapi_key:str=None):
    if scraperapi_key:
        return f'http://api.scraperapi.com?api_key={scraperapi_key}&url={url}'
    else:
        return url
