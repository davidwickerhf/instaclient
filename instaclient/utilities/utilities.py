"""This module contains utilities used by the InstaClient"""
import functools
from functools import wraps
import logging
import time
import random

def get_logger():
    """
    Creates a logging object and returns it

    Returns:
        logger:logging.Log: Log object
    """

    loglevel = logging.INFO
    l = logging.getLogger(__name__)
    if not getattr(l, 'handler_set', None):
        l.setLevel(loglevel)
        h = logging.StreamHandler()
        f = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        h.setFormatter(f)
        l.addHandler(h)
        l.setLevel(loglevel)
        l.handler_set = True
    return l  
 
 
def exception(func):
    """
    Exception logging decorator

    Args:
        func:function: Function to wrap

    Returns:
        wrapper:function: Wrapper function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            # log the exception
            msg = "Exception in method {}".format(func.__name__)
            logger = get_logger('debug.log')
            logger.exception(msg)
 
    return wrapper
