from instaclient.client import *
from instaclient.client.component import Component
from instaclient.client.navigator import Navigator

if TYPE_CHECKING:
    from instaclient import InstaClient


class Interactions(Navigator):
    PIXEL_SCROLL=3
    END_PAGE_SCROLL=4
    PAGE_DOWN_SCROLL=5
    # FOLLOW PROCEDURE
    @Component._login_required
    def follow_user(self:'InstaClient', user:str, nav_to_user:bool=True):
        """
        _follow_user follows the instagram user that matches the username in the `user` attribute.
        If the target account is private, a follow request will be sent to such user and a `PrivateAccountError` will be raised.

        Args:
            user (str): Username of the user to follow.

        Raises:
            PrivateAccountError: Raised if the `user` is a private account - A request to follow the user will be sent eitherway.
            InvalidUserError: Raised if the `user` is invalid
        """
        # Check User Vadility
        profile = self.get_profile(user)
        if not profile:
            raise InvalidUserError(user)

        # Navigate to User Page
        self._nav_user(user, check_user=False)
        
        if self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.MESSAGE_USER_BTN))):
            # User already followed
            pass
        else:
            follow_button = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOW_BTN)), url=ClientUrls.NAV_USER.format(user))
            self._press_button(follow_button)
            profile.requested_by_viewer = True
        return profile

    
    @Component._login_required
    def unfollow_user(self:'InstaClient', user:str, nav_to_user=True, check_user=True):
        """
        Unfollows a given user.

        Args:
            user (str): User to unfollow
            nav_to_user (bool, optional): Navigate to user profile page. Defaults to True.
            check_user (bool, optional): Check user vadility. Defaults to True.

        Raises:
            InvalidUserError: raised if the user specified by the `user` argument is invalid.
        """
        profile = self.get_profile(user)
        if not profile:
            raise InvalidUserError(user)

        LOGGER.debug('INSTACLIENT: User <{}> is valid'.format(user))
        self._nav_user(user, check_user=False)
        
        if profile.requested_by_viewer:
            requested_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.REQUESTED_BTN)))
            self._press_button(requested_btn)
            confirm_unfollow = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.CONFIRM_UNFOLLOW_BTN)))
            self._press_button(confirm_unfollow)
            LOGGER.debug(f'Cancelled Follow Request for user <{user}>')
        
        elif self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.UNFOLLOW_BTN))):
            unfollow_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.UNFOLLOW_BTN)))
            self._press_button(unfollow_btn)
            time.sleep(1)
            confirm_unfollow = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.CONFIRM_UNFOLLOW_BTN)))
            self._press_button(confirm_unfollow)
            LOGGER.debug('INSTACLIENT: Unfollowed user <{}>'.format(user))

    
    @Component._login_required
    def like_user_posts(self, user:str, n_posts:int, like:bool=True):
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

        self._nav_user(user)

        imgs = []
        elements = self._find_element(EC.presence_of_all_elements_located((By.CLASS_NAME, '_9AhH0')))
        imgs.extend(elements)

        for img in imgs[:n_posts]:
            img.click() 
            time.sleep(1) 
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                LOGGER.error(e)

            self.driver.find_elements_by_class_name('ckWGn')[0].click()


    @Component._login_required
    def send_dm(self:'InstaClient', user:str, message:str):
        """
        Send an Instagram Direct Message to a user. 

        Args:
            user (str): Instagram username of the account to send the DM to
            message (str): Message to send to the user via DMs

        Raises:
            InvalidUserError: if the user is invalid.
        """
        # Navigate to User's dm page
        try:
            self._nav_user_dm(user)
            text_area = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.DM_TEXT_AREA)))
            text_area.send_keys(message)
            time.sleep(1)
            send_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_DM_BTN)))
            self._press_button(send_btn)
            time.sleep(1)
        except Exception as error: 
            if self.error_callback:
                self.error_callback(self.driver)
            LOGGER.error('INSTACLIENT: An error occured when sending a DM to the user <{}>'.format(user))
            raise error


    @Component._login_required
    def forward_post(self:'InstaClient', shortcode:str, user:str, message:str=None):
        # Load Post Page
        post = self.get_post(shortcode)
        if not post:
            raise InvalidShortCodeError(shortcode)

        # Nav home page
        self._nav_home(manual=True)
        # Nav search page
        self._nav_explore(manual=True)
        # Insert username in field
        input_bar:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.EXPLORE_SEARCH_INPUT)))
        input_bar.send_keys(post.owner)
        # Click user div
        user_div:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEARCH_USER_DIV.format(post.owner))))
        self._press_button(user_div)
        self._dismiss_useapp_bar()
        # Scroll through posts to find correct one
        last = None
        break_warning = False
        while True:
            self.scroll(interval=1)
            posts:WebElement = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.SHORTCODE_DIV)))
            if posts[-1] == last:
                if break_warning:
                    raise InvalidShortCodeError(shortcode)
                else:
                    break_warning = True
            last = posts[-1]
            
            for post in posts:
                pshortcode = post.get_attribute('href')
                pshortcode = pshortcode.replace('https://www.instagram.com/p/', '')
                pshortcode = pshortcode.replace('/', '')
                if shortcode == pshortcode:
                    # Open Post
                    post:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.POST_DIV.format(pshortcode))))
                    post.click()
                    break
                else:
                    continue
            break
        # Forward
        share_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SHARE_POST_BTN)))
        LOGGER.debug("Found share button")
        self._press_button(share_btn)
        LOGGER.debug("Pressed Share button")

        user_input = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEARCH_USER_INPUT)))
        user_input.send_keys(user)
        LOGGER.debug("Found user input div")

        user_div = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEARCH_USER_DIV.format(user))))
        self._press_button(user_div)
        LOGGER.debug("Selected target user")

        send_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NEXT_BUTTON)))
        self._press_button(send_btn)

        if message:
            self.send_dm(user, message)
        return True

        



    # ENGAGEMENT PROCEDURES
    @Component._login_required
    def scroll(self, mode=PAGE_DOWN_SCROLL, size:int=500, times:int=1, interval:int=3):
        """
        Scrolls to the bottom of a users page to load all of their media

        Returns:
            bool: True if the bottom of the page has been reached, else false

        """
        for n in range(0, times):
            self._dismiss_dialogue(wait_time=1)
            LOGGER.debug('INSTACLIENT: Scrolling')
            if mode == self.PIXEL_SCROLL:
                self.driver.execute_script("window.scrollBy(0, {});".format(size))
            elif mode == self.PAGE_DOWN_SCROLL:
                url = self.driver.current_url
                body = self._find_element(EC.presence_of_element_located((By.TAG_NAME, 'body')), retry=True, url=url)
                body.send_keys(Keys.PAGE_DOWN)
            elif mode == self.END_PAGE_SCROLL:
                url = self.driver.current_url
                body = self._find_element(EC.presence_of_element_located((By.TAG_NAME, 'body')), retry=True, url=url)
                body.send_keys(Keys.END)
            time.sleep(interval)
        LOGGER.info('Scrolled')
        return False


    @Component._login_required
    def like_feed_posts(self, count):
        LOGGER.debug('INSTACLIENT: like_feed_posts')


    @Component._login_required
    def like_post(self:'InstaClient', shortcode:str) -> Optional[Post]:
        # Nav Post Page
        post:Post = self.get_post(shortcode=shortcode)
        if post and post.viewer_has_liked:
            return post

        self._nav_post(shortcode)

        try:
            like_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.LIKE_BTN)))
            self._press_button(like_btn)
            LOGGER.info(f'Liked Post<{shortcode}>')
            post.likes_count += 1
            post.viewer_has_liked = True
            return post
        except Exception as error:
            LOGGER.error(f'There was an error when liking the Post<{shortcode}>', exc_info=error)
            return post


    @Component._login_required
    def unlike_post(self:'InstaClient', shortcode:str) -> Optional[Post]:
        # Nav Post Page
        post:Post = self.get_post(shortcode=shortcode)
        if post and not post.viewer_has_liked:
            return post

        self._nav_post(shortcode)

        try:
            like_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.LIKE_BTN)))
            self._press_button(like_btn)
            LOGGER.info(f'Unliked Post<{shortcode}>')
            post.likes_count -= 1
            post.viewer_has_liked = False
            return post
        except Exception as error:
            LOGGER.error(f'There was an error when liking the Post<{shortcode}>', exc_info=error)
            return None


    @Component._login_required
    def comment_post(self:'InstaClient', shortcode:str, text:str) -> bool:
        # Load Page
        self._nav_post_comments(shortcode)

        # Find Comment Text Area
        comment_area = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.COMMENT_TEXT_AREA)))

        # Input Comment
        comment_area.send_keys(text)
        time.sleep(1)

        # Send Comment
        try:
            send_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_COMMENT_BTN)))
            self._press_button(send_btn) 
        except:
            comment_area.send_keys(Keys.ENTER)
            time.sleep(1)
            comment_area.send_keys(Keys.ENTER)
            
        LOGGER.info(f'Successfully commented on Post<{shortcode}>')
        return Comment(self, None, self.username, self.username, shortcode, text) # TODO Return Comment Instance