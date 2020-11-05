"""This module contains the InstaClient class"""
from logging import log
from os import waitpid
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException        
import time, os

from instaclient.utilities.utilities import *
from instaclient.errors import *
from instaclient.client.paths import Paths
from instaclient.client.urls import ClientUrls


class InstaClient:
    CHROMEDRIVER=1
    LOCAHOST=1
    WEB_SERVER=2
    def __init__(self, driver_type: int=CHROMEDRIVER, host_type:int=LOCAHOST):
        """
        Create an `InstaClient` object to access the instagram website.

        Args:
            driver_type (int, optional): The type of browser driver to run instagram on. Defaults to CHROMEDRIVER.
            host (int, optional): Whether the code is run locally or on a server. Defaults to LOCAHOST.

        Raises:
            InvaildHostError: Raised if host int does not correspond to any host type
            InvaildDriverError: Raised if driver int does not correspond to any driver type.
            error: Normal Exception, raised if anything fails when creating the client.
        """
        self.driver_type = driver_type
        self.host_type = host_type
        self.logged_in = False
        self.driver = None
        self.username = None
        self.password = None
        self.__init_driver()


    @insta_method
    def check_status(self, discard_driver:bool=False):
        """
        Check if account is currently logged in. Returns True if account is logged in. Sets the `instaclient.logged_in` variable accordingly.
        Returns False if the driver is not open yet - even if the Instagram credentials (`username` and `password`) are correct.

        Returns:
            bool: True if client is logged in, False if client is not connected or webdriver is not open.
        """
        if not self.driver:
            return False
        self.driver.get(ClientUrls.HOME_URL)
        icon = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.NAV_BAR)), wait_time=4)
        if icon:
            self.logged_in = True
            result = True
        else:
            self.logged_in = False
            result = False
        if discard_driver:
            self.__discard_driver()
        return result


    @insta_method
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
        
        # Initiate Driver
        if not self.driver:
            self.__init_driver()

        # Get Elements
        try:
            # Attempt Login
            self.driver.get(ClientUrls.LOGIN_URL)
            print('INSTACLIENT: Got Login Page')
            # Detect Cookies Dialogue

            if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
                print('INSTACLIENT: Found Cookies Request')
                alert = self.__find_element(EC.element_to_be_clickable((By.XPATH, Paths.ACCEPT_COOKIES)), url=ClientUrls.LOGIN_URL)
                alert.click()

            # Get Form elements
            username_input = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.USERNAME_INPUT)), url=ClientUrls.LOGIN_URL)
            password_input = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.PASSWORD_INPUT)), url=ClientUrls.LOGIN_URL)
            login_btn = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.LOGIN_BTN)), url=ClientUrls.LOGIN_URL)# login button xpath changes after text is entered, find first
            print('INSTACLIENT: Found elements')
            # Fill out form
            username_input.send_keys(username)
            time.sleep(1)
            password_input.send_keys(password)
            time.sleep(1)
            print('INSTACLIENT: Filled in form')
            login_btn.click()
            print('INSTACLIENT: Sent form')
        except Exception as error:
            # User already logged in ?
            result = self.check_status()
            if discard_driver:
                self.__discard_driver()
            if not result:
                raise error
            else:
                print('INSTACLIENT: User already logged in?')
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
            print('INSTACLIENT: Suspicious Login Attempt.')
            send_code = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)), wait_time=4)
            send_code.click()
            print('INSTACLIENT: Sent Security Code')
            # Detect Error
            alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ERROR_SENDING_CODE)), wait_time=4)
            if alert:
                # Error in sending code, send via email
                email = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SELECT_EMAIL_BTN)), wait_time=4)
                email.click()
                time.sleep(0.5)
                send_code.click()
                print('INSTACLIENT: Sending code via email')
                raise SuspisciousLoginAttemptError(mode=SuspisciousLoginAttemptError.EMAIL)
            raise SuspisciousLoginAttemptError(mode=SuspisciousLoginAttemptError.PHONE)

        # Detect 2FS
        scode_input = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.VERIFICATION_CODE)))
        if scode_input:
            # 2F Auth is enabled, request security code
            print('INSTACLIENT: 2FA Required. Check Auth App')
            raise VerificationCodeNecessary()
        else:
            self.logged_in = True

        # Discard Driver or complete login
        if discard_driver:
            self.__discard_driver()
        else:
            # Detect and dismiss save info Dialog
            self.driver.get(ClientUrls.HOME_URL)

            # Detect 'Turn On Notifications' Box
            try:
                no_notifications_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.NO_NOTIFICATIONS_BTN)), wait_time=3, url=ClientUrls.HOME_URL)
                no_notifications_btn.click()
            except:
                pass
            self.dismiss_dialogue()
        return self.logged_in


    @insta_method
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
            print('INSTACLIENT: Resending code')
            resend_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.RESEND_CODE_BTN)), wait_time=4)
            resend_btn.click()

            alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ERROR_SENDING_CODE)), wait_time=3)
            if alert:
                back_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.BACK_BTN)), wait_time=4)
                back_btn.click()
                time.sleep(1)
                email = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SELECT_EMAIL_BTN)), wait_time=4)
                email.click()
                time.sleep(0.5)
                send_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)), wait_time=4)
                send_btn.click()
                mode = SuspisciousLoginAttemptError.EMAIL
                raise SuspisciousLoginAttemptError(mode)
            raise SuspisciousLoginAttemptError()
        else:
            print('Wrong Url when resending code')
            return False


    @insta_method
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
        scode_btn.click()

        # Detect Error
        form_error = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.INVALID_CODE)), wait_time=3)
        if form_error:
            # Invalid Code
            scode_input.clear()
            raise InvalidSecurityCodeError()

        self.logged_in = True
        if discard_driver:
            self.__discard_driver()
        else:
            self.dismiss_dialogue()
        return self.logged_in


    @insta_method
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
        scode_btn.click()

        alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ALERT)))
        if alert:
            # Code is Wrong
            # Clear input field
            scode_input.clear()
            raise InvalidVerificationCodeError()
        else:
            # Auth Correct
            self.logged_in = True
            self.dismiss_dialogue()
            if discard_driver:
                self.__discard_driver()
            return self.logged_in


    @insta_method
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
        if not self.driver:
            self.__init_driver(login=True)
        
        # Navigate to User Page
        if nav_to_user:
            self.nav_user(user, check_user=False)
        
        # Check User Vadility
        try:
            result = self.is_valid_user(user, nav_to_user=False)
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
            follow_button.click()

        if discard_driver:
            self.__discard_driver()

        if private:
            raise FollowRequestSentError(user)

    
    @insta_method
    def unfollow_user(self, user:str, discard_driver:bool=False):
        """
        Unfollows user(s)

        Args:
            user:str: Username of user to unfollow
        """
        if not self.driver:
            self.__init_driver(login=True)
        self.nav_user(user)

        unfollow_btns = self.__find_buttons('Following')

        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation = self.__find_buttons('Unfollow')[0]
                unfollow_confirmation.click()
        else:
            print('INSTACLIENT: No {} buttons were found.'.format('Following'))
        if discard_driver:
            self.__discard_driver()
    

    @insta_method
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
    

    @insta_method
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
                print(e)

            self.driver.find_elements_by_class_name('ckWGn')[0].click()


    @insta_method
    def send_dm(self, user:str, message:str, discard_driver:bool=False):
        """
        Send an Instagram Direct Message to a user. if `check_user` is set to True, the `user` argument will be checked to validate whether it is a real instagram username.

        Args:
            user (str): Instagram username of the account to send the DM to
            message (str): Message to send to the user via DMs
            check_user (bool, optional): If set to False, the `InstaClient` will assume that `user` is a valid instagram username. Defaults to True.
        """
        if not self.driver:
            self.__init_driver(login=True)
        # Navigate to User's dm page
        try:
            self.nav_user_dm(user)
            text_area = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.DM_TEXT_AREA)))
            text_area.send_keys(message)
            send_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_DM_BTN)))
            send_btn.click()
        except Exception as error: 
            if discard_driver:
                self.__discard_driver()
            raise error


    #@insta_method
    #def comment_post(self, text):
        #"""
        #Comments on a post that is in modal form
        #"""

        #comment_input = self.driver.find_elements_by_class_name('Ypffh')[0]
        #comment_input.click()
        #comment_input.send_keys(text)
        #comment_input.send_keys(Keys.Return)

        #print('Commentd.')


    @insta_method
    def scrape_followers(self, user:str, check_user=True, discard_driver:bool=False):
        """
        scrape_followers Scrape an instagram user's followers and return them as a list of strings.

        Args:
            user (str): User to scrape
            check_user (bool, optional): If set to True, checks if the `user` is a valid instagram username. Defaults to True.
            discard_driver (bool, optional): If set to True, the `driver` will be discarded at the end of the method. Defaults to False.

        Returns:
            list: List of instagram usernames
        """
        
        if not self.driver:
            self.__init_driver(login=True)
        # Nav to user page
        self.nav_user(user, check_user=check_user)
        # Find Followers button/link
        followers_btn:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_BTN)), url=ClientUrls.NAV_USER.format(user))
        # Start scraping
        followers = []
        # Click followers btn
        followers_btn.click()
        time.sleep(2)
        # Load all followers
        followers = []
        main:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST_MAIN)))
        size = main.size.get('height')
        time.sleep(15)
        while True:
            main:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST_MAIN)), wait_time=3)
            new_size = main.size.get('height')
            if new_size > 60000:
                break
            if new_size > size:
                size = new_size
                time.sleep(15)
                continue
            else:
                break
        try:
            followers_list:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST)), wait_time=3)
        except NoSuchElementException:
            return self.scrape_followers(user, check_user, discard_driver)

        divs = followers_list.find_elements_by_xpath(Paths.FOLLOWER_USER_DIV)
        for div in divs:
            try:
                username = div.text.split('\n')[0]
                if username not in followers and username not in ('Follow',):
                    followers.append(username)
            except:
                pass
        if discard_driver:
            self.__discard_driver()
        return followers

                
    # IG UTILITY METHODS
    @insta_method
    def dismiss_dialogue(self):
        """
        Dismiss an eventual Instagram dialogue with button text containing either 'Cancel' or 'Not Now'.
        """
        try:
            dialogue = self.__find_buttons(button_text='Not Now') # TODO add this to 'Translation' doc
            dialogue.click()
        except:
            try:
                dialogue = self.__find_buttons(button_text='Cancel') # TODO add this to translation docs
                dialogue.click()
            except:
                pass
    

    @insta_method
    def search_tag(self, tag:str, discard_driver:bool=False):
        """
        Naviagtes to a search for posts with a specific tag on IG.

        Args:
            tag:str: Tag to search for
        """

        self.driver.get(ClientUrls.SEARCH_TAGS.format(tag))
        alert: WebElement = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)))
        if alert:
            # Tag does not exist
            raise InvaildTagError(tag=tag)
        else: 
            # Operation Successful
            return True


    @insta_method
    def logout(self, discard_driver:bool=False):
        """
        Check if the client is currently connected to Instagram and logs of the current InstaClient session.

        Returns:
            bool: True if the 
        """
        result = self.check_status()
        if result:
            if discard_driver:
                self.__discard_driver()
            else:
                settings_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SETTINGS_BTN)), wait_time=4)
                settings_btn.click()
                logout_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.LOG_OUT_BTN)), wait_time=4)
                logout_btn.click()
                confirm_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.CONFIRM_LOGOUT_BTN)), wait_time=4)
                confirm_btn.click()
            return True
        else:
            return True


    @insta_method
    def nav_user(self, user:str, check_user:bool=True):
        """
        Navigates to a users profile page

        Args:
            user:str: Username of the user to navigate to the profile page of
            check_user:bool: Condition whether to check if a user is valid or not

        Returns:
            True if operation is successful

        Raises:
            InvaildUserError if user does not exist
        """
        self.driver.get(ClientUrls.NAV_USER.format(user))
        if check_user:
            return self.is_valid_user(user=user, nav_to_user=False)
        

    @insta_method
    def nav_user_dm(self, user:str, check_user:bool=True):
        """
        Open DM page with a specific user
        
        Args:
            user:str: Username of the user to send the dm to

        Raises:
            InvalidUserError if user does not exist

        Returns:
            True if operation was successful
        """
        self.nav_user(user, check_user=check_user)
        if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.FOLLOW_BTN))):
            self.follow_user(user, nav_to_user=False)
        if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.REQUESTED_BTN))):
            raise FollowRequestSentError(user)
        else:
            message_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.MESSAGE_USER_BTN)))
            # Open User DM Page
            message_btn.click()
            return True
        

    @insta_method
    def is_valid_user(self, user, nav_to_user=True, discard_driver:bool=False):
        if not self.driver:
            self.__init_driver(login=True)
            nav_to_user = True
        if nav_to_user:
            self.driver.get(ClientUrls.NAV_USER.format(user))
        element = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)), wait_time=8)
        if element:
            # User does not exist
            self.driver.get(ClientUrls.HOME_URL)
            if discard_driver:
                self.__discard_driver()
            raise InvalidUserError(username=user)
        else: 
            # Operation Successful
            paccount_alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.PRIVATE_ACCOUNT_ALERT)), wait_time=3)
            if paccount_alert:
                # navigate back to home page
                if discard_driver:
                    self.__discard_driver()
                raise PrivateAccountError(user)
            else:
                if discard_driver:
                    self.__discard_driver()
                return True


    # IG PRIVATE UTILITIES
    def __infinite_scroll(self):
        """
        Scrolls to the bottom of a users page to load all of their media

        Returns:
            bool: True if the bottom of the page has been reached, else false

        """

        SCROLL_PAUSE_TIME = 1

        self.last_height = self.driver.execute_script("return document.body.scrollHeight")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        self.new_height = self.driver.execute_script("return document.body.scrollHeight")


        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False


    def __find_buttons(self, button_text:str):
        """
        Finds buttons for following and unfollowing users by filtering follow elements for buttons. Defaults to finding follow buttons.

        Args:
            button_text: Text that the desired button(s) has 
        """
        buttons = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.BUTTON.format(button_text))), wait_time=4)
        return buttons


    def __find_element(self, expectation, url:str=None, wait_time:int=8, attempt=0):
        """
        __find_element finds and returns the `WebElement`(s) that match the expectation's XPATH.

        If a TimeoutException is raised by the driver, this method will take care of finding the reason of the exception and it will call itself another time. If the second attemt fails as well, then the `NoSuchElementException` will be raised.

        Args:
            expectation (expected_conditions class): Any class defined in ``selenium.webdriver.support.expected_conditions``
            url (str): The url where the element is expected to be present
            wait_time (int, optional): Time to wait to find the element. Defaults to 15.
            attempt (int, optional): Number of attempts. IMPORTANT: don't change this attribute's value. Defaults to 0.

        Raises:
            NoSuchElementException: Raised if the element is not found after two attempts.

        Returns:
            WebElement: web element that matches the `expectation` xpath
        """
        try:
            wait = WebDriverWait(self.driver, wait_time)
            widgets = wait.until(expectation)
            return widgets
        except TimeoutException:
            # Element was not found in time
            if attempt < 1:
                if self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
                    accept_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.ACCEPT_COOKIES)))
                    accept_btn.click()
                if not self.check_status():
                    # Not Logged In!
                    raise NotLoggedInError()
                else:
                    if attempt < 1 and url is not None:
                        self.driver.get(url)
                        self.__find_element(self, expectation, url, wait_time, attempt+1)
                    else:
                        raise NoSuchElementException()
            else:
                raise NoSuchElementException()


    def __check_existence(self, expectation, wait_time:int=2.5):
        """
        Checks if an element exists.
        Args:
            expectation: EC.class
            wait_time:int: (Seconds) retry window before throwing Exception
        """
        try: 
            wait = WebDriverWait(self.driver, wait_time)
            widgets = wait.until(expectation)
            return True
        except:
            return False


    def __discard_driver(self):
        if self.driver:
            self.driver.quit()
            self.logged_in = False
            self.driver = None


    def __init_driver(self, login=False):
        try:
            if self.driver_type == self.CHROMEDRIVER:
                if self.host_type == self.WEB_SERVER:
                    # Running on web server
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                    chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
                    chrome_options.add_argument("--window-size=343,915")
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--no-sandbox")
                    self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                elif self.host_type == self.LOCAHOST:
                    # Running locally
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
                    chrome_options.add_argument("--window-size=343,915")
                    #chrome_options.add_argument("--headless")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--no-sandbox")
                    self.driver = webdriver.Chrome(executable_path='instaclient/drivers/chromedriver.exe', chrome_options=chrome_options)
                else:
                    raise InvaildHostError(self.host_type)
            else:
                raise InvaildDriverError(self.driver_type)
        except Exception as error:
            raise error

        if login:
            try:
                self.login(self.username, self.password)
            except:
                raise InstaClientError(message='Tried logging in when initiating driver, but username and password are not defined.')

        