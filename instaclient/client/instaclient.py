"""This module contains the InstaClient class"""

# IMPORT UTILITIES, DEPENDENCIES & MODELS
from instaclient.instagram.comment import Comment
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
    def __init__(self, driver_type: int=CHROMEDRIVER, host_type:int=LOCAHOST, driver_path=None, connect=False, logger:logging.Logger=None, debug=False, error_callback=None, localhost_headless=False, proxy=None):
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
        self.driver = None
        self.username = None
        self.password = None

        global LOGGER
        if logger:
            LOGGER = logger

        if debug and not logger:
           LOGGER.setLevel(logging.DEBUG)

        if connect:
            self._connect(func='__init__')

    # CLIENT PROPERTIES
    @property
    def logged_in(self) -> bool:
        """
        logged_in: Checks whether the client is currently logged in to Instagram.

        Returns:
            bool: True if `driver` is open and user is logged into Instagram.
        """
        if self.driver:
            if self.username and self.password:
                url = self.driver.current_url
                if 'https://www.instagram.com/' in url and ClientUrls.LOGIN_URL not in url:
                    return True
        return False

    @property
    def threads(self) -> Optional[list]:
        """
        threads: gets all the threads created and controlled by the client. All such threads include `instaclient` in their names.

        Returns:
            Optional[list]: A list of all sub-threads created and controlled by the client. Returns `None` if no thread is found.
        """
        running = list()
        for thread in threading.enumerate(): 
            if thread is not threading.main_thread():
                running.append(thread)
        
        if len(running) < 1:
            return None
        else:
            return running



    # DRIVER METHODS
    def connect(self: 'InstaClient', login=False, retries=0, func=None):
        return super()._connect(login=login, retries=retries, func=func)

    def disconnect(self: 'InstaClient'):
        return super()._disconnect()



    # AUTH
    def login(self: 'InstaClient', username: str, password: str, check_user: bool=True):
        return super()._login(username, password, check_user=check_user)


    def resend_security_code(self):
        return super()._resend_security_code()


    def input_security_code(self, code: int):
        return super()._input_security_code(code)


    def input_verification_code(self, code: int):
        return super()._input_verification_code(code)


    def logout(self: 'InstaClient', disconnect:bool=True):
        return super()._logout(disconnect=disconnect)
    


    # CHECKERS
    def check_status(self: 'InstaClient') -> bool:
        return super()._check_status()
    

    def is_valid_user(self: 'InstaClient', user: str) -> bool:
        return super()._is_valid_user(user)


   
    # SCRAPING
    def get_notifications(self: 'InstaClient', types: Optional[list]=None, count: Optional[int]=None) -> Optional[list]:
        return super()._scrape_notifications(types=types, count=count)


    def get_profile(self: 'InstaClient', username: str, context: bool=True) -> Optional[Profile]:
        return super()._scrape_profile(username, context=context)


    def get_followers(self, user: str, count: int, check_user:bool=True, callback_frequency: int=100, callback=None, **callback_args) -> Optional[list]:
        return super()._scrape_followers(user, count, check_user=check_user, callback_frequency=callback_frequency, callback=callback, **callback_args)

    
    def get_post(self, shortcode:int, context:Optional[bool]=True) -> Optional[Post]:
        return super()._scrape_post(shortcode=shortcode, context=context)

    
    def get_user_posts(self: 'InstaClient', username: str, count: Optional[int]=30, deep_scrape: Optional[bool]=True, callback_frequency: int=100, callback=None, **callback_args) -> Union[List[str], List[Post]]:
        return super()._scrape_user_posts(username, count, deep_scrape=deep_scrape, callback_frequency=callback_frequency, callback=callback, **callback_args)


    def get_hashtag(self: 'InstaClient', tag: str) -> Optional[Hashtag]:
        return super()._scrape_tag(tag=tag, viewer=self.username)

    

    # INTERACTIONS
    def follow(self, user: str, nav_to_user: bool=True):
        return super()._follow_user(user, nav_to_user=nav_to_user)


    def unfollow(self, user: str, nav_to_user:bool=True, check_user:bool=True):
        return super()._unfollow_user(user, nav_to_user=nav_to_user, check_user=check_user)


    def send_dm(self, user: str, message: str):
        return super()._send_dm(user, message)


    def comment_post(self, shortcode: str, text: str) -> Optional[Comment]:
        result = super()._comment_on_post(shortcode, text)
        # Return Comment Object
        return self._find_comment(shortcode, self.username, text)


    def like_post(self, shortcode: str) -> Optional[Post]:
        return super()._like_post(shortcode=shortcode)

    
    def unlike_post(self, shortocde: str) -> Optional[Post]:
        return super()._unlike_post(shortcode=shortocde)


    def like_user_posts(self, user: str, n_posts: int, like: bool=True):
        return super()._like_latest_posts(user, n_posts, like=like)


    def like_feed_posts(self, count:int):
        return super()._like_feed_posts(count)


    def scroll(self, mode:int=Interactions.PAGE_DOWN_SCROLL, size:int=500, times:int=1, interval:int=3):
        return super()._scroll(mode=mode, size=size, times=times, interval=interval)

    
