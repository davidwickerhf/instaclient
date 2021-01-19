"""InstaClient class"""

# IMPORT UTILITIES, DEPENDENCIES & MODELS
from instaclient.instagram.comment import Comment
from instaclient.client import *

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
        if error_callback:
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
            self.connect(func='__init__')

    # CLIENT PROPERTIES
    @property
    def logged_in(self) -> bool:
        """Checks whether the client is currently logged in to Instagram.

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
        """gets all the threads created and controlled by the client. All such threads include `instaclient` in their names.

        Returns:
            Optional[list]: A list of all sub-threads created and controlled by the client. Returns `None` if no thread is found.
        """
        running = list()
        for thread in threading.enumerate(): 
            if thread is not threading.main_thread() and 'instaclient' in thread.getName():
                running.append(thread)
        
        if len(running) < 1:
            return None
        else:
            return running

    @property
    def logger(self) -> Optional[logging.Logger]:
        return LOGGER

    def set_logger(self, logger:logging.Logger):
        global LOGGER
        LOGGER = logger



    # DRIVER METHODS
    # connect()
    # disconnect()


    # AUTH
    # login()
    # resend_security_code()
    # input_security_code()
    # input_verification_code()
    # logout()


    # CHECKERS
    # check_status()
    # is_valid_user()

   
    # SCRAPING
    # get_notifications()
    # get_profile()
    # get_followers()
    # get_post()
    # get_user_posts()
    # get_hashtag()
    

    # INTERACTIONS
    # follow_user()
    # unfollow_user()
    # send_dm()
    # comment_post()
    # like_post()
    # unlike_post()
    # like_user_posts()
    # like_feed_posts()
    # scroll()
    
