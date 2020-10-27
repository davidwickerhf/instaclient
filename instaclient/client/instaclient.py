"""This module contains the InstaClient class"""
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
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
    def __init__(self, driver_type: int=CHROMEDRIVER, host=LOCAHOST):
        """
        Creates an instance of instaclient class.

        Args:
            driver_type:int: 
                InstaClient.CHROMEDRIVER for a Chrome instance
            host:int: 
                InstaClient.LOCALHOST for testing / running locally
                InstaClient.WEB_SERVER for production / running on a web server

        Attributes:
            driver: Instance of the Selenium Webdriver (defaults to Chrome) 
            logged_in:bool: Boolean whether current user is logged in or not. Defaults to False
        """
        try:
            if driver_type == self.CHROMEDRIVER:
                if host == self.WEB_SERVER:
                    # Running on web server
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                    chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
                    chrome_options.add_argument("window-size=525,950")
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--no-sandbox")
                    self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                elif host == self.LOCAHOST:
                    # Running locally
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
                    chrome_options.add_argument("window-size=525,950")
                    self.driver = webdriver.Chrome(executable_path='instaclient/drivers/chromedriver.exe', chrome_options=chrome_options)
                else:
                    raise InvaildHostError(host)
            else:
                raise InvaildDriverError(driver_type)
        except Exception as error:
            raise error
        self.logged_in = False


    @insta_method
    def check_status(self):
        """
        Check if account is currently logged in. Returns True if account is logged in. Sets the instaclient.logged_in variable accordingly.

        :return: True if account is logged in, False if account is NOT logged in.
        :rtype: boolean
        """
        icon = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.NAV_BAR)), wait_time=4)
        if icon:
            self.logged_in = True
            return True
        else:
            self.logged_in = False
            return False


    @insta_method
    def login(self, username:str, password:str):
        """
        Logs a user into Instagram via the web portal
        """
        self.username = username
        self.password = password
        # Get Elements
        try:
            # Attempt Login
            self.driver.get(ClientUrls.LOGIN_URL)
            # Detect Cookies Dialogue
            try:
                alert = self.__find_element(EC.element_to_be_clickable((By.XPATH, Paths.ACCEPT_COOKIES)), wait_time=3)
                alert.click()
            except:
                print('No alert')
                pass
            # Get Form elements
            username_input = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.USERNAME_INPUT)))
            password_input = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.PASSWORD_INPUT)))
            login_btn = self.__find_element(EC.presence_of_element_located((By.XPATH,Paths.LOGIN_BTN)))# login button xpath changes after text is entered, find first
            # Fill out form
            username_input.send_keys(username)
            time.sleep(1)
            password_input.send_keys(password)
            time.sleep(1)
            login_btn.click()
        except:
            # User already logged in ?
            print('User already logged in?')
            return self.logged_in
        
        # Detect correct Login
        usernamealert: WebElement = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.INCORRECT_USERNAME_ALERT)), wait_time=3)
        if usernamealert:
            # Username is invalid
            self.driver.get(ClientUrls.LOGIN_URL)
            self.username = None
            raise InvalidUserError(username)

        passwordalert: WebElement = self.__check_existence(EC.presence_of_element_located((By.XPATH,Paths.INCORRECT_PASSWORD_ALERT)), wait_time=3)
        if passwordalert:
            # Password is incorrect
            self.driver.get(ClientUrls.LOGIN_URL)
            self.password = None
            raise InvaildPasswordError(password)

        # Detect 2FS
        scode_input = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.SECURITY_CODE)), wait_time=3)
        if scode_input:
            # 2F Auth is enabled, request security code
            raise SecurityCodeNecessary()
        else:
            self.logged_in = True

        # Detect and dismiss save info Dialog
        self.driver.get(ClientUrls.HOME_URL)

        # Detect 'Turn On Notifications' Box
        try:
            no_notifications_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.NO_NOTIFICATIONS_BTN)), wait_time=3)
            no_notifications_btn.click()
        except:
            pass
        self.dismiss_dialogue()
        return self.logged_in

    
    @insta_method
    def input_security_code(self, code):
        """
        Use when authenticating and the 2FA security code is required.

        Args:
            code:int: Security code sent by instagram to the user's phone number or Authenticator App.

        Returns:
            True if login is successful

        Raises:
            InvalidSecurityCodeError() if the security code is incorrect
        """
        scode_input: WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SECURITY_CODE)), wait_time=4)
        scode_input.send_keys(code)
        scode_btn: WebElement = self.__find_element(EC.element_to_be_clickable((By.XPATH, Paths.SECURITY_CODE_BTN)), wait_time=5)
        time.sleep(1)
        scode_btn.click()

        alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ALERT)))
        if alert:
            # Code is Wrong
            # Clear input field
            scode_input.clear()
            raise InvalidSecurityCodeError()
        else:
            # Auth Correct
            self.logged_in = True
            self.dismiss_dialogue()
            return self.logged_in


    @insta_method
    def follow_user(self, user:str):
        """
        Follows user(s)

        Args:
            user:str: Username of the user to follow
        """

        self.nav_user(user)

        follow_buttons = self.__find_buttons('Follow')

        for btn in follow_buttons:
            btn.click()

    
    @insta_method
    def unfollow_user(self, user:str):
        """
        Unfollows user(s)

        Args:
            user:str: Username of user to unfollow
        """

        self.nav_user(user)

        unfollow_btns = self.__find_buttons('Following')

        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation = self.__find_buttons('Unfollow')[0]
                unfollow_confirmation.click()
        else:
            print('No {} buttons were found.'.format('Following'))
    

    @insta_method
    def get_user_images(self, user:str):
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

            finished = self._infinite_scroll() # scroll down
            
            elements = self.__find_element((EC.presence_of_element_located(By.CLASS_NAME, 'FFVAD')))
            img_srcs.extend([img.get_attribute('src') for img in elements]) # scrape srcs

        img_srcs = list(set(img_srcs)) # clean up duplicates
        return img_srcs
    

    @insta_method
    def like_latest_posts(self, user:str, n_posts:int, like:bool=True):
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
    def send_dm(self, user:str, message:str, check_user=True):
        """
        Send a DM to the specified user.

        Args:
            user:str: User to send the DM to
            message:str: Message to send to the user
        """
        # Navigate to User's dm page
        self.nav_user_dm(user, check_user=check_user)
        text_area = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.DM_TEXT_AREA)))
        print(text_area)
        text_area.send_keys(message)
        send_btn = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_DM_BTN)))
        send_btn.click()


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
    def scrape_followers(self, user:str, check_user=True, *args, **kwargs):
        """
        Gets all followers of a certain user

        Args:
            user:str: Username of the user for followers look-up
            count:int: Number of followers to get. Note that high follower counts will take longer and longer exponentially (even hours)
            
        Returns:
            followers:list<str>: List of usernames (str)

        Raises:
            InvalidUserError if user does not exist
            PrivateAccountError if account is private
        """
        # Nav to user page
        self.nav_user(user, check_user=check_user)
        # Find Followers button/link
        followers_btn:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_BTN)), wait_time=4)
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
        followers_list:WebElement = self.__find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_LIST)), wait_time=3)
        divs = followers_list.find_elements_by_xpath(Paths.FOLLOWER_USER_DIV)
        for div in divs:
            username = div.text.split('\n')[0]
            if username not in followers and username not in ('Follow',):
                followers.append(username)
        return followers

                
    # IG UTILITY METHODS
    @insta_method
    def dismiss_dialogue(self):
        try:
            dialogue = self.__find_buttons(button_text='Not Now') # add this to 'Translation' doc
            dialogue.click()
        except:
            pass
    

    @insta_method
    def search_tag(self, tag:str):
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
            return self.is_valid_user(user=user)
        


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
        message_btn = self.__find_buttons('Message')
        # Open User DM Page
        message_btn.click()
        return True
        

    def is_valid_user(self, user):
        element = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)), wait_time=3)
        if element:
            # User does not exist
            self.driver.get(ClientUrls.HOME_URL)
            print('Returned Home')
            raise InvalidUserError(username=user)
        else: 
            # Operation Successful
            print('Sucessfully Navigated to user')
            paccount_alert = self.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.PRIVATE_ACCOUNT_ALERT)), wait_time=3)
            if paccount_alert:
                # navigate back to home page
                raise PrivateAccountError(user)
            else:
                return True


    # IG PRIVATE UTILITIES
    def _infinite_scroll(self):
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


    def __find_element(self, expectation, wait_time:int=10):
        """
        Finds widget (element) based on the field's value
        Args:
            expectation: EC.class 
            wait_time:int: (Seconds) retry window before throwing Exception
        """
        wait = WebDriverWait(self.driver, wait_time)
        widgets = wait.until(expectation)
        return widgets


    def __check_existence(self, expectation, wait_time:int=10):
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
        