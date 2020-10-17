"""This module contains the InstaClient class"""
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException        
import time

from instaclient.utilities.utilities import *
from instaclient.errors.common import *
from instaclient.client.paths import Paths
from instaclient.client.urls import ClientUrls


class InstaClient:
    CHROMEDRIVER=1
    def __init__(self, username: str, password: str, driver: int=CHROMEDRIVER):
        """
        Creates an instance of instaclient class.

        Args:
            username:str: The username of the user
            password:str: The password of the user
            driver_location:str: Path of the driver file (must be in the root folder of your project)
            wait_time:int: (Seconds) time to wait before raising driver exception

        Attributes:
            driver: Instance of the Selenium Webdriver (defaults to Chrome) 
            logged_in:bool: Boolean whether current user is logged in or not. Defaults to False
        """

        self.username = username
        self.password = password

        try:
            if driver == self.CHROMEDRIVER:
                self.driver = webdriver.Chrome('drivers/chromedriver.exe')
            else:
                raise InexistingDriverError(driver)
            self.driver.maximize_window()
        except Exception as error:
            raise error
        self.logged_in = False


    @insta_method
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """
        # Get Elements
        try:
            # Attempt Login
            self.driver.get(ClientUrls.LOGIN_URL)
            username_input = self._find_element(EC.presence_of_element_located((By.XPATH,Paths.USERNAME_INPUT)))
            password_input = self._find_element(EC.presence_of_element_located((By.XPATH,Paths.PASSWORD_INPUT)))
            login_btn = self._find_element(EC.presence_of_element_located((By.XPATH,Paths.LOGIN_BTN)))# login button xpath changes after text is entered, find first
            # Fill out form
            print('Button: ', type(login_btn), ' ', str(login_btn))
            username_input.send_keys(self.username)
            time.sleep(1)
            password_input.send_keys(self.password)
            time.sleep(1)
            login_btn.click()
        except:
            # User already logged in ?
            print('User already logged in?')
            return self.logged_in
        # Detect correct Login
        try:
            # Credentials Incorrect
            alert: WebElement = self._find_element(EC.presence_of_element_located((By.XPATH,Paths.ALERT)))
            if 'username' in alert.text:
                self.driver.get(ClientUrls.LOGIN_URL)
                raise IncorrectUsernameError(self.username)
            elif 'password' in alert.text:
                self.driver.get(ClientUrls.LOGIN_URL)
                raise IncorrectPasswordError(self.password)
        except (TimeoutException, NoSuchElementException):
            self.logged_in = True
        # Detect save info Dialog
        try:
            save_info_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SAVE_INFO_BTN)))
            save_info_btn.click()
        except:
            pass
        # Detect 'Turn On Notifications' Box
        try:
            no_notifications_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NO_NOTIFICATIONS_BTN)))
            no_notifications_btn.click()
        except:
            pass
        return self.logged_in


    @insta_method
    def follow_user(self, user:str):
        """
        Follows user(s)

        Args:
            user:str: Username of the user to follow
        """

        self.nav_user(user)

        follow_buttons = self._find_buttons('Follow')

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

        unfollow_btns = self._find_buttons('Following')

        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation = self._find_buttons('Unfollow')[0]
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
            
            elements = self._find_element((EC.presence_of_element_located(By.CLASS_NAME, 'FFVAD')))
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
        """

        action = 'Like' if like else 'Unlike'

        self.nav_user(user)

        imgs = []
        elements = self._find_element(EC.presence_of_all_elements_located((By.CLASS_NAME, '_9AhH0')))
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
    def send_dm(self, user:str, message:str):
        """
        Send a DM to the specified user.

        Args:
            user:str: User to send the DM to
            message:str: Message to send to the user
        """
        # Navigate to User's dm page
        self.nav_user_dm(user)
        text_area = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.DM_TEXT_AREA)))
        print(text_area)
        text_area.send_keys(message)
        send_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_DM_BTN)))
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
    def get_followers(self, user:str):
        """
        Gets all followers of a certain user

        Args:
            user:str: Username of the user for followers look-up
        
        Returns:
            followers:list<str>: List of usernames (str)
        """
        
        self.nav_user_followers(user) # Open followers page
        # Scroll list and save usernames
        followers = []
        finished = False
        while not finished:

            finished = self._infinite_scroll() # scroll down

            followers.extend([follower.get_attribute('title') for follower in self.driver.find_elements_by_class_name('FPmhX notranslate  _0imsa')]) # scrape srcs

        followers = list(set(followers)) # clean up duplicates
        return followers


    # IG UTILITY METHODS
    @insta_method
    def search_tag(self, tag:str):
        """
        Naviagtes to a search for posts with a specific tag on IG.

        Args:
            tag:str: Tag to search for
        """

        self.driver.get(ClientUrls.SEARCH_TAGS.format(tag))
        alert: WebElement = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)))
        if alert:
            # Tag does not exist
            self.driver.get(ClientUrls.HOME_URL)
            print('Returned Home')
            raise InexistingTagError(tag=tag)
        else: 
            # Operation Successful
            print('Sucessfully Navigated to tag page')
            return True


    @insta_method
    def nav_user(self, user:str):
        """
        Navigates to a users profile page

        Args:
            user:str: Username of the user to navigate to the profile page of

        Returns:
            True if operation is successful

        Raises:
            InexistinUserError if user does not exist
        """
        self.driver.get(ClientUrls.NAV_USER.format(user))
        element = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)))
        if element:
            # User does not exist
            self.driver.get(ClientUrls.HOME_URL)
            print('Returned Home')
            raise InexistingUserError(user=user)
        else: 
            # Operation Successful
            print('Sucessfully Navigated to user')
            return True


    @insta_method
    def nav_user_dm(self, user:str):
        """
        Open DM page with a specific user
        
        Args:
            user:str: Username of the user to send the dm to
        """
        self.nav_user(user)

        message_btn = self._find_buttons('Message')
        # Open User DM Page
        message_btn.click()

    
    @insta_method
    def nav_user_followers(self, user:str):
        """
        Navigates to the user's followers page

        Args:
            user:str: Username of the user
        """
        self.driver.get(ClientUrls.FOLLOWERS_URL.format(user))


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


    def _find_buttons(self, button_text:str):
        """
        Finds buttons for following and unfollowing users by filtering follow elements for buttons. Defaults to finding follow buttons.

        Args:
            button_text: Text that the desired button(s) has 
        """
        buttons = self._find_element(EC.presence_of_element_located((By.XPATH, "//*[text()='{}']".format(button_text))))
        return buttons


    def _find_element(self, expectation, wait_time=10):
        """
        Finds widget (element) based on the field's value
        Args:
            expectation: EC.class 
            wait_time:int: (Seconds) retry window before throwing Exception
        """
        wait = WebDriverWait(self.driver, wait_time)
        widgets = wait.until(expectation)
        return widgets


    def _check_existence(self, expectation, wait_time=10):
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
        