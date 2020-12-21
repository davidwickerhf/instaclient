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
    def login(self: 'InstaClient', username: str, password: str, check_user: bool=True, _discard_driver: bool=False):
        return super()._login(username, password, check_user=check_user, _discard_driver=_discard_driver)

    def resend_security_code(self):
        return super()._resend_security_code()

    def input_security_code(self, code: int, _discard_driver: bool=False):
        return super()._input_security_code(code, _discard_driver=_discard_driver)

    def input_verification_code(self, code: int, _discard_driver: bool=False):
        return super()._input_verification_code(code, _discard_driver=_discard_driver)

    def logout(self: 'InstaClient', _discard_driver: bool=False):
        return super()._logout(_discard_driver=_discard_driver)
    


    # CHECKERS
    def check_status(self: 'InstaClient', _discard_driver: bool=False) -> bool:
        return super()._check_status(_discard_driver=_discard_driver)
    
    def is_valid_user(self: 'InstaClient', user: str, nav_to_user: bool=True, _discard_driver: bool=False) -> bool:
        return super()._is_valid_user(user, nav_to_user=nav_to_user, _discard_driver=_discard_driver)

   
    # SCRAPING
    def get_notifications(self: 'InstaClient', types: Optional[list]=None, count: Optional[int]=None) -> Optional[list]:
        return super()._scrape_notifications(types=types, count=count)

    def get_profile(self: 'InstaClient', username: str, context: bool=True) -> Optional[Profile]:
        return super()._scrape_profile(username, context=context)

    def get_user_images(self, user: str, _discard_driver: bool=False):
        return super()._scrape_user_images(user, _discard_driver=_discard_driver)

    def get_followers(self, user: str, count: int, check_user:bool=True, _discard_driver:bool=False, callback_frequency: int=100, callback=None, **callback_args) -> Optional[list]:
        return super()._scrape_followers(user, count, check_user=check_user, _discard_driver=_discard_driver, callback_frequency=callback_frequency, callback=callback, **callback_args)

    def get_hashtag(self: 'InstaClient', tag: str) -> Optional[Hashtag]:
        return super()._scrape_tag(tag, self.username)

    

    # INTERACTIONS
    def follow(self, user: str, nav_to_user: bool=True, _discard_driver: bool=False):
        return super()._follow_user(user, nav_to_user=nav_to_user, _discard_driver=_discard_driver)

    def unfollow(self, user: str, nav_to_user:bool=True, check_user:bool=True, _discard_driver: bool=False):
        return super()._unfollow_user(user, nav_to_user=nav_to_user, check_user=check_user, _discard_driver=_discard_driver)

    def send_dm(self, user: str, message: str, _discard_driver: bool=False):
        return super()._send_dm(user, message, _discard_driver=_discard_driver)

    def like_user_posts(self, user: str, n_posts: int, like: bool=True, _discard_driver: bool=False):
        return super()._like_latest_posts(user, n_posts, like=like, _discard_driver=_discard_driver)

    def like_feed_posts(self, count:int):
        return super()._like_feed_posts(count)

    def scroll(self, mode:int=Interactions.PAGE_DOWN_SCROLL, size:int=500, times:int=1, interval:int=3):
        return super()._scroll(mode=mode, size=size, times=times, interval=interval)

    
