"""This module contains utilities used by the InstaClient"""
import functools
from functools import wraps
import logging
import time
import random

def get_logger(logger_file_path):
    """
    Creates a logging object and returns it

    Returns:
        logger:logging.Log: Log object
    """

    logger = logging.getLogger('instaclientLogger')
    logger.setLevel(logging.DEBUG)
 
    # log file handler
    fh = logging.FileHandler(logger_file_path)
 
    # log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
 
    logger.addHandler(fh)
    return logger
 
 
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
