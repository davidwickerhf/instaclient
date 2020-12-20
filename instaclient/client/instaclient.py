"""This module contains the InstaClient class"""

# IMPORT UTILITIES, DEPENDENCIES & MODELS
from instaclient.client import *
from instaclient.utilities.utilities import *

# IMPORT CLIENT COMPONENTS
from instaclient.client.scraper import Scraper
from instaclient.client.auth import Auth
from instaclient.client.interactions import Interactions


class InstaClient(Auth, Interactions, Scraper):
    # INIT
    CHROMEDRIVER=1
    LOCAHOST=1
    WEB_SERVER=2
    def __init__(self, driver_type: int=CHROMEDRIVER, host_type:int=LOCAHOST, driver_path=None, init_driver=False, logger:logging.Logger=None, debug=False, error_callback=None, localhost_headless=False, proxy=None, scraperapi_key=None):
        """
        Create an `InstaClient` object to access the instagram website.

        Args:
            
            driver_type (int, optional): The type of browser driver to run instagram on. Defaults to CHROMEDRIVER.
            host_type (int, optional): Whether the code is run locally or on a server. Defaults to LOCAHOST.
            driver_path (str): The path where you saved the c`hromedriver.exe` file. This is required if you are running the client locally. Defaults to None
            debug (bool): If set to True, the `error_callback` will be called multiple times for debugging or when an error occures. Defaults to Falses
            error_callback (callback): A callback method to be called when an error occures within the InstaClient. Your custom error_callbak must require only one argument named `driver`: a driver like object (The InstaClient will pass itself to the method as `driver` argument)
            localhost_headless (bool): If set to True, the localhost chromedriver will be set to --headless, meaning it will run without showing the Chrome window. Defaults to true.

        Raises:
            InvaildHostError: Raised if host int does not correspond to any host type
            InvaildDriverError: Raised if driver int does not correspond to any driver type.
            error: Normal Exception, raised if anything fails when creating the client.
            InvalidErrorCallbackError: Raised if the `error_callback` is not callable
        """
        self.driver_type = driver_type
        self.host_type = host_type
        if host_type == self.LOCAHOST and driver_path is None:
            raise InvalidDriverPathError(driver_path)
        self.driver_path = driver_path
        self.debug = debug
        if error_callback or debug:
            if not callable(error_callback):
                raise InvalidErrorCallbackError()
        self.error_callback = error_callback
        self.localhost_headless = localhost_headless
        self.proxy = proxy
        self.scraperapi_key = scraperapi_key
        self.logged_in = False
        self.driver = None
        self.username = None
        self.password = None
        self.threads = []

        global LOGGER
        if logger:
            LOGGER = logger

        if debug and not logger:
           LOGGER.setLevel(logging.DEBUG)

        if init_driver:
            self._init_driver(func='__init__')

    # AUTH


    # CHECKERS

   
   # SCRAPING


   # INTERACTIONS
    
