#!/usr/bin/env python
#
# Unofficial Instagram Python client. Built with the use of the selenium,
# and requests modules.
# Copyright (C) 2015-2021
# David Henry Francis Wicker <wickerdevs@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
from instaclient.client import *
from instaclient.instagram import profile

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.client.checker import Checker


class Navigator(Checker):

    # NAVIGATION PROCEDURES
    def _show_nav_bar(self:'InstaClient'):
        if self.driver.current_url != ClientUrls.HOME_URL:
            self._nav_home()
        self._dismiss_dialogue()
        self._dismiss_useapp_bar()
        

    def _nav_home(self:'InstaClient', manual=False):
        """Navigates to IG home page
        """
        if not manual:
            if self.driver.current_url != ClientUrls.HOME_URL:
                self.driver.get(ClientUrls.HOME_URL)
                self._dismiss_dialogue()
        else:
            self._show_nav_bar()
            home_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.HOME_BTN)))
            self._press_button(home_btn)


    def _nav_user(self:'InstaClient', user:str, check_user:bool=True):
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
        if check_user:
            result, profile = self.is_valid_user(user=user)
            if not result:
                raise InvalidUserError(user)
        if self.driver.current_url != ClientUrls.NAV_USER.format(user):
            self.driver.get(ClientUrls.NAV_USER.format(user))
            self._dismiss_useapp_bar()

    
    def _nav_user_dm(self:'InstaClient', user:str):
        """
        Open DM page with a specific user
        
        Args:
            user:str: Username of the user to send the dm to

        Raises:
            InvalidUserError if user does not exist

        Returns:
            True if operation was successful
        """
        result, profile = self.is_valid_user(user)
        if not result:
            raise InvalidUserError(user)
        LOGGER.debug(f'INSTACLIENT: User <{user}> is valid and public (or followed)'.format(user))
        

        # TODO NEW VERSION: Opens DM page and creates new DM
        try:
            # LOAD INBOX PAGE
            LOGGER.debug('LOADING PAGE')
            self.driver.get(ClientUrls.INBOX)

            self._dismiss_dialogue(2)

            # GET NEW MESSAGE ELEMENT
            new_msg_btn:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NEW_MSG_BTN)), wait_time=10)
            self._press_button(new_msg_btn)


            # LOAD NEW PAGE
            user_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USER_DIV)), wait_time=10)
            LOGGER.debug('Page Loaded')

            # INPUT USERNAME 
            input_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEARCH_USER_INPUT)), wait_time=15)
            LOGGER.debug(f'INPUT: {input_div}')
            input_div.send_keys(user)
            LOGGER.debug('Sent Username to Search Field')
            time.sleep(1)

            # FIND CORRECT USER DIV
            user_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USER_DIV)))
            username_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USER_DIV_USERNAME)))
            LOGGER.debug('Found user div')

            self._press_button(user_div)
            LOGGER.debug('Selected user div')
            time.sleep(1)
            next = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NEXT_BUTTON)))
            self._press_button(next)
            LOGGER.debug('Next pressed')
            return True
        except Exception as error:
            LOGGER.error('There was error navigating to the user page: ', exc_info=error)
            raise InstaClientError('There was an error when navigating to <{}>\'s DMs'.format(user))
            
    
    def _nav_post(self:'InstaClient', shortcode:str):
        url = ClientUrls.POST_URL.format(shortcode)
        if self.driver.current_url is not url:
            self.driver.get(url)

        result = self._is_valid_page(url)
        if not result:
            raise InvalidShortCodeError(shortcode)

        self._dismiss_useapp_bar()
        LOGGER.debug('Got Post\'s Page')
        return True


    def _nav_post_comments(self:'InstaClient', shortcode:str):
        url = ClientUrls.COMMENTS_URL.format(shortcode)
        if self.driver.current_url is not url:
            if self.driver.current_url == ClientUrls.POST_URL.format(shortcode):
                # Press Comment Button
                btn = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.COMMENT_BTN)))
                if btn:
                    btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.COMMENT_BTN)))
                    self._press_button(btn)
                else:
                    pass
            if self.driver.current_url != url:
                self.driver.get(url)

        result = self._is_valid_page(url)
        if not result:
            raise InvalidShortCodeError(shortcode)
        LOGGER.debug('Got Post\'s Comments Page')
        return True
        
     
    def _nav_tag(self:'InstaClient', tag:str):
        """Navigates to a search for posts with a specific tag on IG.

        Args:
            tag:str: Tag to search for
        """

        self.driver.get(ClientUrls.SEARCH_TAGS.format(tag))
        if self._is_valid_page(ClientUrls.SEARCH_TAGS.format(tag)):
            return True
        else:
            raise InvaildTagError(tag)

    
    def _nav_location(self:'InstaClient', id:str, slug:str):
        """Navigates to the page of the location specified by
        the `id` and `slug`.

        Args:
            id (str): ID of the location to navigate to.
            slug (str): Slug of the location to navigate to.
        """

        self.driver.get(ClientUrls.LOCATION_PAGE.format(id, slug))
        if self._is_valid_page(ClientUrls.LOCATION_PAGE.format(id, slug)):
            return True
        else:
            raise InvaildLocationError(id, slug)


    def _nav_explore(self:'InstaClient', manual=False):
        """Navigates to the explore page
        """
        if not manual:
            self.driver.get(ClientUrls.EXPLORE_PAGE)
            if self._is_valid_page(ClientUrls.EXPLORE_PAGE):
                return True
            return False
        else:
            self._show_nav_bar()
            explore_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.EXPLORE_BTN)))
            self._press_button(explore_btn)
