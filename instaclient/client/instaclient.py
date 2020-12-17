"""This module contains the InstaClient class"""

from instaclient.client import *
from instaclient.utilities.utilities import *
from instaclient.instagram import (InstaBaseObject, Profile, Post, Hashtag, Notification)
#Components
from instaclient.client.scraper import Scraper
from instaclient.client.component import Component
from instaclient.client.navigator import Navigator


class InstaClient(Navigator, Scraper):
    CHROMEDRIVER=1
    LOCAHOST=1
    WEB_SERVER=2
    PIXEL_SCROLL=3
    END_PAGE_SCROLL=4
    PAGE_DOWN_SCROLL=5
    
    # INIT
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

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        if init_driver:
            self.__init_driver(func='__init__')


    # INSTACLIENT DECORATOR
    def __manage_driver(init_driver=True, login=True):
        def outer(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                time.sleep(random.randint(1, 2))
                self.logger.debug('INSTACLIENT: Mangage Driver, func: {}'.format(func.__name__))
                if init_driver:
                    if not self.driver:
                        if login and (self.username is None or self.password is None):
                            raise NotLoggedInError()
                        self.__init_driver(login, func=func.__name__)

                error = False
                result = None
                try:
                    result = func(self, *args, **kwargs)
                    time.sleep(1)
                except Exception as exception:
                    error = exception
                
                discard = kwargs.get('discard_driver')
                if discard is not None:
                    if discard:
                        self.discard_driver()
                elif len(args) > 0 and isinstance(args[-1], bool):
                    if args[-1]:
                        self.discard_driver()
                
                time.sleep(random.randint(1, 2))
                if error:
                    raise error
                else:
                    return result
            return wrapper
        return outer
    
    # INSTAGRAM FUNCTIONS
    # LOGIN PROCEDURE
    @__manage_driver(login=False)
    def check_status(self, discard_driver:bool=False):
        """
        Check if account is currently logged in. Returns True if account is logged in. Sets the `instaclient.logged_in` variable accordingly.
        Returns False if the driver is not open yet - even if the Instagram credentials (`username` and `password`) are correct.

        Returns:
            bool: True if client is logged in, False if client is not connected or webdriver is not open.
        """
        self.logger.debug('INSTACLIENT: Check Status')
        if not self.driver:
            return False
        self.logger.debug(self.driver.current_url)
        if ClientUrls.HOME_URL not in self.driver.current_url:
            self.driver.get(ClientUrls.HOME_URL)
        if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
            self.__dismiss_cookies()
        if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN))):
            btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN)))
            self.__press_button(btn)
            self.logger.debug('INSTACLIENT: Dismissed dialogue')

        icon = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.NAV_BAR)), wait_time=4)
        if icon:
            self.logged_in = True
            result = True
        else:
            self.logged_in = False
            result = False
        return result


    @__manage_driver(login=False)
    def login(self, username:str, password:str, check_user:bool=True, discard_driver:bool=False):
        """
        Sign Into Instagram with credentials. Go through 2FA if necessary. Sets the InstaClient variable `InstaClient.logged_in` to True if login was successful.

        Args:
            username (str): The instagram account's username
            password (str): The instagram account's password
            check_user (bool, optional): If False, the username will be considered as valid and will not be checked. If the user is invalid, the login procedure will not be completed. Defaults to True.

        Raises:
            InvalidUserError: Raised if the user is not valid and `check_user` is set to True. Warning: if check_user is set to False and the user is invalid, the login procedure will not be completed.
            InvaildPasswordError: Raised if the password is incorrect.
            SecurityCodeNecessary: Raised if the user's account has 2FA. If this error is raised, you can complete the login procedure with `InstaClient.input_security_code`

        Returns:
            bool: Returns True if login was successful.
        """
        self.username = username
        self.password = password

        # Get Elements
        try:
            # Attempt Login
            self.driver.get(ClientUrls.LOGIN_URL)
            self.logger.debug('INSTACLIENT: Got Login Page')
            # Detect Cookies Dialogue

            if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
                self.__dismiss_cookies()

            # Get Form elements
            username_input = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.USERNAME_INPUT)), url=ClientUrls.LOGIN_URL)
            password_input = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.PASSWORD_INPUT)), url=ClientUrls.LOGIN_URL)
            self.logger.debug('INSTACLIENT: Found elements')
            # Fill out form
            username_input.send_keys(username)
            time.sleep(1)
            password_input.send_keys(password)
            time.sleep(1)
            self.logger.debug('INSTACLIENT: Filled in form')
            login_btn = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.LOGIN_BTN)), url=ClientUrls.LOGIN_URL)# login button xpath changes after text is entered, find first
            self.__press_button(login_btn)
            self.logger.debug('INSTACLIENT: Sent form')
        except ElementClickInterceptedException as error:
            self.password = None
            self.driver.get(ClientUrls.LOGIN_URL)
            raise InvaildPasswordError(password)
        except Exception as error:
            # User already logged in ?
            result = self.check_status()
            if not result:
                raise error
            else:
                self.logger.debug('INSTACLIENT: User already logged in?')
                return self.logged_in
        
        # Detect correct Login
        if check_user:
            usernamealert: WebElement = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.INCORRECT_USERNAME_ALERT)), wait_time=3)
            if usernamealert:
                # Username is invalid
                self.driver.get(ClientUrls.LOGIN_URL)
                self.username = None
                raise InvalidUserError(username)

        passwordalert: WebElement = self.__check_existence(EC.presence_of_element_located((By.XPATH,Paths.INCORRECT_PASSWORD_ALERT)))
        if passwordalert:
            # Password is incorrect
            self.driver.get(ClientUrls.LOGIN_URL)
            self.password = None
            raise InvaildPasswordError(password)

        # Detect Suspicious Login Attempt Dialogue
        send_code = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)))
        if send_code:
            self.logger.warn('INSTACLIENT: Suspicious Login Attempt.')
            send_code = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)), wait_time=4)
            self.__press_button(send_code)
            self.logger.warn('INSTACLIENT: Sent Security Code')
            # Detect Error
            alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ERROR_SENDING_CODE)), wait_time=2)
            if alert:
                # Error in sending code, send via email
                email = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SELECT_EMAIL_BTN)), wait_time=4)
                self.__press_button(email)
                time.sleep(0.5)
                self.__press_button(send_code)
                self.logger.warn('INSTACLIENT: Sending code via email')
                raise SuspisciousLoginAttemptError(mode=SuspisciousLoginAttemptError.EMAIL)
            raise SuspisciousLoginAttemptError(mode=SuspisciousLoginAttemptError.PHONE)

        # Detect 2FS
        scode_input = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.VERIFICATION_CODE)))
        if scode_input:
            # 2F Auth is enabled, request security code
            self.logger.warn('INSTACLIENT: 2FA Required. Check Auth App')
            raise VerificationCodeNecessary()
        else:
            self.logged_in = True

        self.logger.debug('INSTACLIENT: Credentials are Correct')

        # Discard Driver or complete login
        if discard_driver:
            self.discard_driver()
        else:
            # Detect and dismiss save info Dialog
            self.driver.get(ClientUrls.HOME_URL)
            
            # Detect 'Save to Home Screen' Dialogue
            if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.DISMISS_DIALOGUE))):
                self.__dismiss_dialogue()
            
            # Detect 'Turn On Notifications' Box
            if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.DISMISS_DIALOGUE))):
                self.__dismiss_dialogue()
        return self.logged_in


    @__manage_driver(login=False)
    def resend_security_code(self):
        """
        Resend security code if code hasn't been sent successfully. The code is used to verify the login attempt if `instaclient.errors.common.SuspiciousLoginAttemptError` is raised.

        Raises:
            SuspisciousLoginAttemptError: Raised to continue the login procedure. If the `mode` argument of the error is 0, the security code was sent via SMS; if the `mode` argument is 1, then the security code was sent via email.
        Returns:
            bool: True if the code has been sent again successfully. False if an error occured or if the client is no longer on the login page.
        """
        url = self.driver.current_url
        if ClientUrls.SECURITY_CODE_URL in url:
            self.logger.debug('INSTACLIENT: Resending code')
            resend_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.RESEND_CODE_BTN)), wait_time=4)
            self.__press_button(resend_btn)

            alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ERROR_SENDING_CODE)), wait_time=3)
            if alert:
                back_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.BACK_BTN)), wait_time=4)
                self.__press_button(back_btn)
                time.sleep(1)
                email = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SELECT_EMAIL_BTN)), wait_time=4)
                self.__press_button(email)
                time.sleep(0.5)
                send_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)), wait_time=4)
                self.__press_button(send_btn)
                mode = SuspisciousLoginAttemptError.EMAIL
                raise SuspisciousLoginAttemptError(mode)
            raise SuspisciousLoginAttemptError()
        else:
            self.logger.warn('Wrong Url when resending code')
            return False


    @__manage_driver(login=False)
    def input_security_code(self, code:int or str, discard_driver:bool=False):
        """
        Complete login procedure started with `InstaClient.login()` and insert security code required if `instaclient.errors.common.SuspiciousLoginAttemptError` is raised. Sets `InstaClient.logged_in` attribute to True if login was successful.

        Args:
            code (intorstr): The security code sent by Instagram via SMS or email.

        Raises:
            InvalidSecurityCodeError: Error raised if the code is not valid

        Returns:
            bool: True if login was successful.
        """
        code = str(code)
        if len(code) < 6:
            raise InvalidSecurityCodeError()
        elif not code.isdigit():
            raise InvalidSecurityCodeError()

        scode_input:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SECURITY_CODE_INPUT)), wait_time=4)
        scode_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SECURITY_CODE_BTN)), wait_time=4)
        scode_input.send_keys(code)
        time.sleep(0.5)
        self.__press_button(scode_btn)

        # Detect Error
        form_error = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.INVALID_CODE)), wait_time=3)
        if form_error:
            # Invalid Code
            scode_input.clear()
            raise InvalidSecurityCodeError()

        self.logged_in = True
        self.__dismiss_dialogue()
        return self.logged_in


    @__manage_driver(login=False)
    def input_verification_code(self, code:int or str, discard_driver:bool=False):
        """
        Complete login procedure started with `InstaClient.login()` and insert 2FA security code. Sets `instaclient.logged_in` to True if login was successful.

        Args:
            code (int|str): The 2FA security code generated by the Authenticator App or sent via SMS to the user.

        Raises:
            InvalidSecurityCodeError: Raised if the security code is not correct

        Returns:
            bool: Returns True if login was successful
        """
        scode_input: WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.VERIFICATION_CODE)), wait_time=4)
        scode_input.send_keys(code)
        scode_btn: WebElement = self.__find_element(EC.element_to_be_clickable((By.XPATH, Paths.VERIFICATION_CODE_BTN)), wait_time=5)
        time.sleep(1)
        self.__press_button(scode_btn)

        alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ALERT)))
        if alert:
            # Code is Wrong
            # Clear input field
            scode_input.clear()
            raise InvalidVerificationCodeError()
        else:
            # Auth Correct
            self.logged_in = True
            self.__dismiss_dialogue()
            return self.logged_in


    @__manage_driver(login=False)
    def logout(self, discard_driver:bool=False):
        """
        Check if the client is currently connected to Instagram and logs of the current InstaClient session.

        Returns:
            bool: True if the 
        """
        self.logger.debug('INSTACLIENT: LOGOUT')
        result = self.check_status()
        if result:
            if discard_driver:
                self.logger.debug('INSTACLIENT: Logged Out')
                return True
            else:
                self.driver.get(ClientUrls.NAV_USER.format(self.username))
                time.sleep(1)
                settings_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SETTINGS_BTN)), wait_time=4)
                self.__press_button(settings_btn)
                logout_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.LOG_OUT_BTN)), wait_time=4)
                self.__press_button(logout_btn)
                confirm_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.CONFIRM_LOGOUT_BTN)), wait_time=4)
                self.__press_button(confirm_btn)
                self.logger.debug('INSTACLIENT: Logged Out')
            return True
        else:
            return True


    """ def is_valid(user):
        pass

    def is_private(user):
        pass """


    @__manage_driver(login=False)
    def is_valid_user(self, user:str, nav_to_user:bool=True, discard_driver:bool=False):
        """
        is_valid_user Checks if a given username is a valid Instagram user.

        Args:
            user (str): Instagram username to check
            nav_to_user (bool, optional): Whether the driver shouldnavigate to the user page or not. Defaults to True.
            discard_driver (bool, optional): Whether the driver should be closed after the method finishes. Defaults to False.

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account

        Returns:
            bool: True if the user is valid
        """
        self.logger.debug('INSTACLIENT: Checking user vadility')
        if nav_to_user:
            self.driver.get(ClientUrls.NAV_USER.format(user))

        if self.driver.current_url != ClientUrls.NAV_USER.format(user):
            self.driver.get(ClientUrls.NAV_USER.format(user))

        self.logger.debug('INSTACLIENT: Url: {}'.format(self.driver.current_url))
        if self.driver.current_url == ClientUrls.LOGIN_THEN_USER.format(user):
            raise NotLoggedInError()
        elif self.driver.current_url != ClientUrls.NAV_USER.format(user):
            time.sleep(1)
            self.driver.get(ClientUrls.NAV_USER.format(user))
            time.sleep(1)


        if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
            self.__dismiss_cookies()

        element = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)), wait_time=3)
        if element:
            # User does not exist
            self.logger.debug('INSTACLIENT: {} does not exist.'.format(user))
            raise InvalidUserError(username=user)
        else: 
            self.logger.debug('INSTACLIENT: {} is a valid user.'.format(user))
            # Operation Successful
            paccount_alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.PRIVATE_ACCOUNT_ALERT)))
            if paccount_alert:
                # navigate back to home page
                raise PrivateAccountError(user)
            else:
                return True


    # FOLLOW PROCEDURE
    @__manage_driver()
    def follow_user(self, user:str, nav_to_user:bool=True, discard_driver:bool=False):
        """
        follow_user follows the instagram user that matches the username in the `user` attribute.
        If the target account is private, a follow request will be sent to such user and a `PrivateAccountError` will be raised.

        Args:
            user (str): Username of the user to follow.
            discard_driver (bool, optional): If set to True, the driver will be discarded at the end of the method. Defaults to False.

        Raises:
            PrivateAccountError: Raised if the `user` is a private account - A request to follow the user will be sent eitherway.
            InvalidUserError: Raised if the `user` is invalid
        """
        # Navigate to User Page
        if nav_to_user:
            self.nav_user(user, check_user=False)
        
        # Check User Vadility
        try:
            result = self.is_valid_user(user, nav_to_user=False)
            self.logger.debug('INSTACLIENT: User <{}> is valid'.format(user))
            private = False
            
        # User is private
        except PrivateAccountError:
            private = True

        if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.REQUESTED_BTN))):
            # Follow request already sent
            pass
        elif self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.MESSAGE_USER_BTN))):
            # User already followed
            pass
        else:
            follow_button = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOW_BTN)), url=ClientUrls.NAV_USER.format(user))
            self.__press_button(follow_button)

        if private:
            raise FollowRequestSentError(user)

    
    @__manage_driver()
    def unfollow_user(self, user:str, nav_to_user=True, check_user=True, discard_driver:bool=False):
        """
        Unfollows a given user.

        Args:
            user (str): User to unfollow
            nav_to_user (bool, optional): Navigate to user profile page. Defaults to True.
            check_user (bool, optional): Check user vadility. Defaults to True.
            discard_driver (bool, optional): Discard driver when completed. Defaults to False.

        Raises:
            InvalidUserError: raised if the user specified by the `user` argument is invalid.
        """
        if nav_to_user:
            self.nav_user(user, check_user)
        elif check_user:
            try:
                self.is_valid_user(user, nav_to_user=False)
            except PrivateAccountError:
                pass
            self.logger.debug('INSTACLIENT: User <{}> is valid'.format(user))

        if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.UNFOLLOW_BTN))):
            unfollow_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.UNFOLLOW_BTN)))
            self.__press_button(unfollow_btn)
            time.sleep(1)
            confirm_unfollow = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.CONFIRM_UNFOLLOW_BTN)))
            self.__press_button(confirm_unfollow)
            self.logger.debug('INSTACLIENT: Unfollowed user <{}>'.format(user))
        elif self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.REQUESTED_BTN))):
            requested_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.REQUESTED_BTN)))
            self.__press_button(requested_btn)
            self.logger.debug(f'Cancelled Follow Request for user <{user}>')


    # USER DATA PRODECURES
    @__manage_driver()
    def get_user_images(self, user:str, discard_driver:bool=False):
        """
        Get all images from a users profile.

        Args:
            user:str: Username of the user

        Returns:
            img_srcs:list<str>: list of strings (img_src)

        """
    
        self.nav_user(user)

        img_srcs = []
        finished = False
        while not finished:

            finished = self.__infinite_scroll() # scroll down
            
            elements = self.__find_element((EC.presence_of_element_located(By.CLASS_NAME, 'FFVAD')))
            img_srcs.extend([img.get_attribute('src') for img in elements]) # scrape srcs

        img_srcs = list(set(img_srcs)) # clean up duplicates
        return img_srcs

    
    """ @__manage_driver(login=False)
    def scrape_followers(self, user:str, check_user=True, max_wait_time:int=250, callback_frequency:int=20, callback=None, discard_driver=False, **callback_args):
        
        if callback and not callable(callback):
            raise InvalidErrorCallbackError()

        with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix='scrape') as executor:
            scrape_future = executor.submit(self.__scrape_followers, user, check_user, max_wait_time)
            timer_future = executor.submit(self.__scrape_timer, max_wait_time, callback_frequency, callback, **callback_args)
            result = scrape_future.result()
            return result """

    
    """ def __scrape_timer(self, max_wait_time:int, callback_frequency:int, callback=None, **callback_args):
        tic = time.time()
        final_time = tic + max_wait_time
        self.logger.info('Initiating scrape...'.format(callback_frequency))
        while True:
            
            self.logger.info('Scraping followers... waited {} seconds'.format(callback_frequency))
            if callback:
                callback(**callback_args)
            toc = time.time()
            self.logger.debug('TIMER: {} | Difference: {} | Total Difference: {}'.format(toc, (toc - tic), (final_time - toc)))
            if toc > final_time:
                break
            elif (final_time - toc) < 0:
                time.sleep(final_time - toc)
            else:
                tic = toc
                time.sleep(callback_frequency)
        self.logger.debug('Finished Timer')
        return True """

        
    """ def __scrape_followers(self, user:str, check_user=True, max_waiting_time:int=250):
        
        # Set starting time:
        tic = time.time()
        final_time = tic + max_waiting_time
        # Nav to user page
        self.nav_user(user, check_user=check_user)
        self.logger.debug('Navigated to User Page')
        # Find Followers button/link
        self.logger.debug('Found Followers Button')
        followers_btn:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_BTN)), url=ClientUrls.NAV_USER.format(user))
        # Start scraping
        followers = []
        # Click followers btn
        self.__press_button(followers_btn)
        time.sleep(2)
        # Load all followers
        followers = []
        main:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST_MAIN)))
        self.scroll(self.END_PAGE_SCROLL, times=10, interval=0)
        main:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST_MAIN)))
        size = main.size.get('height')
        while True:
            self.logger.debug('INSTACLIENT: Loop')
            main:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST_MAIN)), wait_time=3)
            new_size = main.size.get('height')
            if new_size > size:
                size = new_size
                toc = time.time()
                self.logger.debug('SCRAPER: {} | Difference: {} | Total Difference: {}'.format(toc, (toc - tic), (final_time - toc)))
                if toc > final_time:
                    self.logger.debug('BREAKING LOOP')
                    break
                tic = toc
                for n in range(10):
                    self.scroll(self.END_PAGE_SCROLL, interval=0)
                    toc = time.time()
                    if toc > final_time:
                        self.logger.debug('BREAKING LOOP')
                        break
                continue
            else:
                self.scroll(self.PAGE_DOWN_SCROLL, interval=0)
                main:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST_MAIN)), wait_time=3)
                new_size = main.size.get('height')
                if new_size > size:
                    continue
                else:
                    self.logger.debug('BREAKING LOOP')
                    break
        self.logger.debug('Finished Scrolling. Loading followers div...')
        try:
            followers_list:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST)), wait_time=3)
        except NoSuchElementException:
            self.logger.warn('Followers List not found... Retrying method')
            return self.scrape_followers(user, check_user)

        self.logger.info('Followers loaded. Saving and returing')
        divs = followers_list.find_elements_by_xpath(Paths.FOLLOWER_USER_DIV)
        for div in divs:
            try:
                username = div.text.split('\n')[0]
                if username not in followers and username not in ('Follow',):
                    followers.append(username)
            except:
                pass
        return followers """


    @__manage_driver()
    def get_followers(self, user:str, count:int, check_user=True, discard_driver=False, callback_frequency:int=100, callback=None, **callback_args):
        """
        scrape_followers: Scrape an instagram user's followers and return them as a list of strings.

        Args:
            user (str): User to scrape
            count (int): Number of followers to scrape
            check_user (bool, optional): If set to True, checks if the `user` is a valid instagram username. Defaults to True.
            callback_frequency (int, optional): Number of scraped followers between updates
            callback (function): Function with no parameters that gets called with the frequency set by ``callback_frequency``

        Returns:
            list: List of instagram usernames

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account
            NoSuchElementException: Raised if an element is not found when compiling operation.
        """
        self.nav_user(user, check_user=check_user)
        followers_btn:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_BTN)), url=ClientUrls.NAV_USER.format(user))
        # Click followers btn
        self.__press_button(followers_btn)
        time.sleep(2)
        self.logger.info(f'Got Followers page for <{user}>')

        followers = list()
        failed = list()
        last_callback = 0

        start = time.time() # TODO
        
        try:
            while len(followers) < count:
                finished_warning = False
                

                loop = time.time() # TODO
                self.logger.debug(f'Starting Scrape Loop. Followers: {len(followers)}')
                
                scraped_count = len(followers)
                divs = self.__find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.FOLLOWER_USER_DIV)), wait_time=2)

                got_elements = time.time() # TODO
                self.logger.debug(f'Got Divs in {got_elements - loop}')

                new = 0
                for div in divs:
                    try:
                        username = div.text.split('\n')[0]
                        if username not in followers and username not in('Follow',) and len(followers) < count:
                            followers.append(username)
                            new += 1

                            if (last_callback + new) % callback_frequency == 0:
                                if callable(callback):
                                    self.logger.debug('Called Callback')
                                    callback(**callback_args)

                    except:
                        failed.append(div)
                        pass
                
                if len(followers) >= count:
                    break

                if not finished_warning and len(followers) == scraped_count:
                    self.logger.info('Detected End of Followers Page')
                    finished_warning = True
                    time.sleep(3)
                elif finished_warning:
                    self.logger.info('Finished Followers')
                    break

                self.logger.debug('Scroll')
                self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
        except Exception as error:
            self.logger.error('ERROR IN SCRAPING FOLLOWERS', exc_info=error)
                

        end = time.time() # TODO
        self.logger.debug(f'Finished. Total: {end - start}')
        self.logger.debug(f'Failed: {len(failed)}')
        return followers
        

    # ENGAGEMENT PROCEDURES
    @__manage_driver()
    def scroll(self, mode=PAGE_DOWN_SCROLL, size=500, times=1, interval=3):
        """
        Scrolls to the bottom of a users page to load all of their media

        Returns:
            bool: True if the bottom of the page has been reached, else false

        """
        for n in range(0, times):
            self.__dismiss_dialogue(wait_time=1)
            self.logger.debug('INSTACLIENT: Scrolling')
            if mode == self.PIXEL_SCROLL:
                self.driver.execute_script("window.scrollBy(0, {});".format(size))
            elif mode == self.PAGE_DOWN_SCROLL:
                url = self.driver.current_url
                body = self.__find_element(EC.presence_of_element_located((By.TAG_NAME, 'body')), retry=True, url=url)
                body.send_keys(Keys.PAGE_DOWN)
            elif mode == self.END_PAGE_SCROLL:
                url = self.driver.current_url
                body = self.__find_element(EC.presence_of_element_located((By.TAG_NAME, 'body')), retry=True, url=url)
                body.send_keys(Keys.END)

            time.sleep(interval)
        return False


    @__manage_driver()
    def like_feed_posts(self, count):
        self.logger.debug('INSTACLIENT: like_feed_posts')

    
    @__manage_driver()
    def get_notifications(self, types:list=None, count:int=None, discard_driver=False):
        self.logger.debug('INSTACLIENT: check_notifications')
        self.driver.get(GraphUrls.GRAPH_ACTIVITY)
        element:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.QUERY_ELEMENT)))
        source = element.text        
        notifications = self._scrape_notifications(source, viewer=self.username, types=types, count=count)
        return notifications


    @__manage_driver()
    def like_latest_posts(self, user:str, n_posts:int, like:bool=True, discard_driver:bool=False):
        """
        Likes a number of a users latest posts, specified by n_posts.

        Args:
            user:str: User whose posts to like or unlike
            n_posts:int: Number of most recent posts to like or unlike
            like:bool: If True, likes recent posts, else if False, unlikes recent posts

        TODO: Currently maxes out around 15.
        TODO: Adapt this def
        """

        action = 'Like' if like else 'Unlike'

        self.nav_user(user)

        imgs = []
        elements = self.__find_element(EC.presence_of_all_elements_located((By.CLASS_NAME, '_9AhH0')))
        imgs.extend(elements)

        for img in imgs[:n_posts]:
            img.click() 
            time.sleep(1) 
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                self.logger.error(e)

            self.driver.find_elements_by_class_name('ckWGn')[0].click()


    @__manage_driver()
    def send_dm(self, user:str, message:str, discard_driver:bool=False):
        """
        Send an Instagram Direct Message to a user. 

        Args:
            user (str): Instagram username of the account to send the DM to
            message (str): Message to send to the user via DMs
            discard_driver (bool): Discard driver when operation is done.

        Raises:
            InvalidUserError: if the user is invalid.
        """
        # Navigate to User's dm page
        try:
            self.nav_user_dm(user)
            text_area = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.DM_TEXT_AREA)))
            text_area.send_keys(message)
            time.sleep(1)
            send_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_DM_BTN)))
            self.__press_button(send_btn)
            time.sleep(1)
        except Exception as error: 
            if self.debug:
                self.error_callback(self.driver)
            self.logger.error('INSTACLIENT: An error occured when sending a DM to the user <{}>'.format(user))
            raise error


    @__manage_driver(login=False)
    def get_hashtag(self, tag:str):
        self.logger.debug('INSTACLIENT: check_notifications')
        tag:Hashtag = self._scrape_tag(tag, None)
        return tag
    
    
    #@__manage_driver()
    #def comment_post(self, text):
        #"""
        #Comments on a post that is in modal form
        #"""

        #comment_input = self.driver.find_elements_by_class_name('Ypffh')[0]
        #comment_input.click()
        #comment_input.send_keys(text)
        #comment_input.send_keys(Keys.Return)

        #self.logger.debug('Commentd.')


    """ @__manage_driver() # TODO
    def scrape_dms(self, discard_driver:bool=False):
        if not self.driver:
            self.__init_driver()

        # Navigate to DMs
        if self.username:
            self.nav_user_dm(self.username)
        else:
            raise NotLoggedInError()

        # Infinite Scroll & Loading
        for i in range(1,count+1):
            try:
                div:WebElement = self.driver.find_element_by_xpath(Paths.FOLLOWER_USER_DIV % i)
                time.sleep(1)
                username = div.text.split('\n')[0]
                if  username not in followers:
                    followers.append(username)
                if i%callback_frequency==0:
                    if callback is None:
                        self.logger.debug('Got another {} followers...'.format(callback_frequency))
                    else:
                        callback(*args, **kwargs)
                self.driver.execute_script("arguments[0].scrollIntoView();", div)
                # TODO OPTIMIZE ALGORITHM (scroll by more than one account only)
            except Exception as error:
                raise error

        
        if discard_driver:
            self.discard_driver() """
    


    def discard_driver(self):
        self.logger.debug('INSTACLIENT: Discarding driver...')
        if self.driver:
            self.driver.quit()
            self.logged_in = False
            self.driver = None
        self.logger.debug('INSTACLIENT: Driver Discarded')


    def __init_driver(self, login=False, retries=0, func=None):
        self.logger.debug('INSTACLIENT: Initiating Driver | attempt {} | func: {}'.format(retries, func))
        try:
            if self.driver_type == self.CHROMEDRIVER:
                if self.host_type == self.WEB_SERVER:
                    # Running on web server
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                    mobile_emulation = { "deviceName": "Nexus 5" }
                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    chrome_options.add_argument("--window-size=414,896")
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--no-sandbox")
                    chrome_options.add_argument("--disable-setuid-sandbox") 
                    chrome_options.add_argument("--remote-debugging-port=9222")
                    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    chrome_options.add_experimental_option('useAutomationExtension', False)
                    if self.proxy:
                        chrome_options.add_argument('--proxy-server=%s' % self.proxy)
                    self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                elif self.host_type == self.LOCAHOST:
                    # Running locally
                    chrome_options = webdriver.ChromeOptions()
                    mobile_emulation = { "deviceName": "Nexus 5" }
                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    chrome_options.add_argument("--headless") if self.localhost_headless else None
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--no-sandbox")
                    self.logger.debug('Path: {}'.format(self.driver_path))
                    if self.proxy:
                        chrome_options.add_argument('--proxy-server=%s' % self.proxy)
                    
                    self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)
                else:
                    raise InvaildHostError(self.host_type)
            else:
                raise InvaildDriverError(self.driver_type)
        except WebDriverException as error:
            if retries < 2:
                self.logger.debug('INSTACLIENT: Error when initiating driver... Trying again')
                self.__init_driver(login=login, retries=retries+1, func='__init_driver')
            else:
                raise error

        if login:
            try:
                self.login(self.username, self.password)
            except:
                raise InstaClientError(message='Tried logging in when initiating driver, but username and password are not defined.')
