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


def insta_method(func):
    """
    Instagram method decorator. Sleeps for around 2 seconds before and after calling any methods that interact with Instagram.

    Args:
        func:function: Function to wrap

    Returns:
        wrapper:function: Wrapper function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Call function
        time.sleep(random.randint(1, 2))
        output = func(*args, **kwargs)
        # Post Processing
        time.sleep(random.randint(1, 2))
        return output
    return wrapper


def manage_driver(func):
    @wraps(func)
    def wrapper(self, login=False, *args, **kwargs):
        if not self.driver:
            print('INSTACLIENT: Initiating Driver...')
            self.__init_driver(login)
            print('INSTACLIENT: Driver initiated.')
        
        error = False
        result = None
        try:
            result = func(*args, *kwargs)
        except Exception as exception:
            error = exception

        discard = kwargs.get('discard_driver')
        if discard:
            print('INSTACLIENT: Discarding driver...')
            self.__discard_driver()
            print('INSTACLIENT: Driver discarded.')
        if error:
            raise error
        else:
            return result
    return wrapper

