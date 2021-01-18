from instaclient.client.constants import QueryHashes
import json, requests

from instaclient.client import *
if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.client.component import Component


class Scraper(Component):
    TYPES = [InstaBaseObject.GRAPH_IMAGE, InstaBaseObject.GRAPH_VIDEO, InstaBaseObject.GRAPH_SIDECAR]

    # SCRAPE USER DATA
    @Component._login_required
    def get_notifications(self:'InstaClient', types:list=None, count:int=None) -> Optional[List[Notification]]:

        if types is None or len(types) == 0:
            types = [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]
        else:
            for type in types:
                if type not in [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]:
                    raise InvalidNotificationTypeError(type)
        
        LOGGER.debug('INSTACLIENT: check_notifications')

        # Deserialize Response
        data = self._request(GraphUrls.GRAPH_ACTIVITY, use_driver=True)
        nodes = list()
        try:
            edges = data['graphql']['user']['activity_feed']['edge_web_activity_feed']['edges']
            for edge in edges:
                if edge.get('node') is not None:
                    nodes.append(edge.get('node'))
        except:
            raise InvalidInstaSchemaError(__name__)
        LOGGER.info('NODE COUNT: {}'.format(len(nodes)))

        # Retrieve Nodes
        selected_nodes = []
        for node in nodes:
            if count is not None and len(selected_nodes) >= count:
                break
            else:
                if node.get('__typename') in types:
                    selected_nodes.append(node)

        notifications = []

        # Map nodes into Notification Objects
        for node in nodes:
            user = Profile(
                client=self,
                id=node['user']['id'],
                viewer=self.username,
                username=node['user']['username'],
                name=node['user']['full_name'],
                profile_pic_url= node['user'].get('profile_pic_url')
            )
            notifications.append(Notification(
                client=self,
                id=node['id'],
                viewer=self.username,
                from_user=user,
                type=node['__typename'],
                timestamp=node['timestamp'],
            ))
        return notifications


    @Component._driver_required
    def get_profile(self:'InstaClient', username:str, context:bool=True) -> Optional['Profile']:
        
        if context and not self.logged_in and None not in (self.username, self.password):
            self.login(self.username, self.password)
        data = self._request(GraphUrls.GRAPH_USER.format(username), use_driver=True)

        if not data:
            if ClientUrls.LOGIN_URL in self.driver.current_url:
                raise NotLoggedInError()
            return None

        try:
            user = data['graphql']['user']
            profile:Profile = Profile(
                client=self,
                id=user['id'],
                viewer=self.username,
                username=user['username'],
                name=user['full_name'],
                biography = user['biography'],
                is_private = user['is_private'],
                is_verified = user['is_verified'],
                is_business_account = user['is_business_account'],
                is_joined_recently = user['is_joined_recently'],
                follower_count = user['edge_followed_by']['count'],
                followed_count = user['edge_follow']['count'],
                post_count = user['edge_owner_to_timeline_media']['count'],
                business_category_name = user['business_category_name'],
                overall_category_name = user['overall_category_name'],
                external_url = user['external_url'],
                fb_id = user.get('fbid'),
                profile_pic_url= user.get('profile_pic_url'),
                
                # Context Based
                business_email = user.get('business_email'),
                blocked_by_viewer = user['blocked_by_viewer'],
                restricted_by_viewer = user['restricted_by_viewer'],
                has_blocked_viewer = user['has_blocked_viewer'],
                has_requested_viewer = user['has_requested_viewer'],
                mutual_followed = user['edge_mutual_followed_by']['count'],
                requested_by_viewer = user['requested_by_viewer']
            )
            LOGGER.debug(f'Loaded profile: {profile}')
            return profile
        except Exception as error:
            LOGGER.exception(f'Error loading profile with username {username}')
            raise InvalidInstaSchemaError(__name__)

    
    @Component._driver_required
    def get_post(self:'InstaClient', shortcode:str, context:bool=True) -> Optional['Post']:
        if context and not self.logged_in and None not in (self.username, self.password):
            self.login(self.username, self.password)

        data = self._request(GraphUrls.GRAPH_POST.format(shortcode), use_driver=True)
        if not data:
            raise InvalidInstaRequestError(GraphUrls.GRAPH_POST.format(shortcode))

        try:
            data = data['graphql']['shortcode_media']

            # Get Location
            location = data['location']
            if location:
                location = Location(
                    client=self,
                    id=location['id'],
                    viewer=self.username,
                    name=location['name'],
                    slug=location['slug'],
                    has_public_page=location['has_public_page'],
                    address=Address(location['address_json'],) if location['address_json'] else None
                )

            # TODO Deserialize Comments
            # Get Comments
            comments = list()
            for cdata in data['edge_media_to_parent_comment']['edges']:
                node = cdata['node']
                comments.append(
                    Comment(
                        client=self,
                        id=node['id'],
                        viewer=self.username,
                        owner=node['owner']['username'],
                        post_shortcode=data['shortcode'],
                        text=node['text'],
                        created_at=node['created_at'],
                        likes_count=node['edge_liked_by']['count'],
                        did_report_as_spam=node['did_report_as_spam'],
                        viewer_has_liked=node['viewer_has_liked'],
                    )
                )
            
            # Get Post Media Info
            media = list()
            type = data['__typename']
            if type == InstaBaseObject.GRAPH_SIDECAR:
                # Get PostMedias
                for edge in data['edge_sidecar_to_children']['edges']:
                    # Get Tagged Users
                    node = edge['node']
                    tagged_users = list()
                    for user in node['edge_media_to_tagged_user']['edges']:
                        tagged_users.append(user['node']['user']['username'])

                    # Append PostMedia
                    if type == InstaBaseObject.GRAPH_VIDEO:
                        src_url = node['video_url']
                    else:
                        src_url = node['display_url']

                    media.append(
                        PostMedia(
                            client=self,
                            id=node['id'],
                            type=node['__typename'],
                            viewer=self.username,
                            shortcode=node['shortcode'],
                            src_url=src_url,
                            is_video=['is_video'],
                            accessibility_caption=['accessibility_caption'],
                            tagged_users=tagged_users,
                            has_audio=data.get('has_audio'),
                            video_duration=data.get('video_duration'),
                            video_view_count=data.get('video_view_count')
                        )
                    )
            else:
                if type == InstaBaseObject.GRAPH_VIDEO:
                    src_url = data['video_url']
                else:
                    src_url = data['display_url']

                tagged_users = list()
                for user in data['edge_media_to_tagged_user']['edges']:
                    tagged_users.append(user['node']['user']['username'])

                media.append(
                    PostMedia(
                        client=self,
                        id=data['id'],
                        type=data['__typename'],
                        viewer=self.username,
                        shortcode=data['shortcode'],
                        src_url=src_url,
                        is_video=['is_video'],
                        accessibility_caption=['accessibility_caption'],
                        tagged_users=tagged_users,
                        has_audio=data.get('has_audio'),
                        video_duration=data.get('video_duration'),
                        video_view_count=data.get('video_view_count')
                    )
                )

            # Get Tagged Users
            tagged_users = list()
            for user in data['edge_media_to_tagged_user']['edges']:
                tagged_users.append(user['node']['user']['username'])

            # Get Caption
            caption = None
            caption_edges = data['edge_media_to_caption']['edges']
            for edge in caption_edges:
                caption = edge['node']['text']

            post:Post = Post(
                client=self,
                id=data['id'],
                type=type,
                viewer=self.username,
                owner=data['owner']['username'],
                shortcode=data['shortcode'],
                caption=caption,
                timestamp=data['taken_at_timestamp'],
                likes_count=data['edge_media_preview_like']['count'],
                comments_disabled=data['comments_disabled'],
                is_ad=data['is_ad'],
                media=media,
                # Require Context
                commenting_disabled_for_viewer=data['commenting_disabled_for_viewer'],
                viewer_has_liked=data['viewer_has_liked'],
                viewer_has_saved=data['viewer_has_saved'],
                viewer_has_saved_to_collection=data['viewer_has_saved_to_collection'],
                viewer_in_photo_of_you=data['viewer_in_photo_of_you'],
                viewer_can_reshare=data['viewer_can_reshare'],
                tagged_users=tagged_users,
                comments=comments,
                location=location
            )
            return post
        except Exception as error:
            LOGGER.error('Error scraping post: ', exc_info=error)
            raise InvalidInstaSchemaError(__name__)


    @Component._login_required
    def _find_comment(self:'InstaClient', shortcode:str, owner:str, text:str) -> Optional['Comment']:
        post:Post = self.get_post(shortcode, context=True)
        if post.comments:
            for comment in post.comments:
                if comment.owner == owner and comment.text == text:
                    return comment
        return None


    @Component._login_required
    def get_user_posts(self:'InstaClient', username:str, count:Optional[int]=30, deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List[str], List[Profile]]]:
        """Get a list of posts of a specified user.

        Args:
            username (str): User to scrape from.
            count (int): Number of posts to load.
            deep_scrape (Optional[bool], optional): If set to True, every scraped post will
                be fully loaded into :class:`instaclient.Post` objects. Defaults to False.
            callback_frequency (int, optional): Frequency with which the method will
                call a specified callback method. The assigned value reflects the
                number of objects to scrape before calling the method. Defaults to 100.
            callback (callable, optional): Callable method that gets called with the frequency
                set by `callback_frequency`. Defaults to None.

        Returns:
            Optional[Union[List[str], List[Post]]]: Optional list of scraped posts. 
                The list may either contain a list of shortcodes or of :class:`instaclient.Post`
                based on the value of the attribute `deep_scrape`.
        """
        # Nav to User Page
        self._nav_user(username)

        # Scroll down and save shortcodes
        shortcodes = list()
        failed = list()
        last_callback = 0
        finished_warning = False
        
        # Shortcodes scraper loop
        try:
            while len(shortcodes) < count:
                
                

                loop = time.time() # TODO
                LOGGER.debug(f'Starting Post Scrape Loop. Posts: {len(shortcodes)}')
                
                scraped_count = len(shortcodes)
                divs = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.SHORTCODE_DIV)), wait_time=2)

                got_elements = time.time() # TODO
                LOGGER.debug(f'Got Divs in {got_elements - loop}')

                new = 0
                for div in divs:
                    try:
                        shortcode = div.get_attribute('href')
                        if shortcode:
                            shortcode = shortcode.replace('https://www.instagram.com/p/', '')
                            shortcode = shortcode.replace('/', '')
                        if shortcode not in shortcodes and shortcode not in (None,) and len(shortcodes) < count:
                            shortcodes.append(shortcode)
                            new += 1

                            if (last_callback + new) % callback_frequency == 0:
                                if callable(callback):
                                    LOGGER.debug('Called Callback')
                                    callback(scraped = shortcodes, **callback_args)

                    except:
                        failed.append(div)
                        pass
                
                if len(shortcodes) >= count:
                    break

                if not finished_warning and len(shortcodes) == scraped_count:
                    LOGGER.info('Detected End of Posts Page')
                    finished_warning = True
                    time.sleep(3)
                elif finished_warning:
                    LOGGER.info('Finished Posts')
                    break
                else:
                    finished_warning = False

                LOGGER.debug('Scroll')
                self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
        except Exception as error:
            LOGGER.error('ERROR IN SCRAPING POSTS', exc_info=error)
                
        LOGGER.warn(f'Failed: {len(failed)}')

        if not deep_scrape:
            return shortcodes
        else:
            # For every shortlink, scrape Post
            LOGGER.info('Deep scraping posts...')
            posts = list()
            for index, shortcode in enumerate(shortcodes):
                LOGGER.debug(f'Deep scraped {index} posts out of {len(shortcodes)}')
                posts.append(self.get_post(shortcode))
            return posts
 

    @Component._login_required
    def get_followers(self:'InstaClient', user:str, count:int, use_api:bool=True, deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List[Profile], List[str]]]:
        """Scrape an instagram user's followers.

        Args:
            user (str): User to scrape
            count (int): Number of followers to scrape
            use_api (bool): If set to True, the instaclient module will take advantage
                of instagram graphql requests to scrape followers. Defaults to False.
            callback_frequency (int, optional): Number of scraped followers between updates
            callback (function): Function with no parameters that gets called with the frequency set by ``callback_frequency``. This method must take a ``scraped`` argument.

        Returns:
            Optional[Union[List[Profile], List[str]]]: List of instagram usernames or of instagram profile objects

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account
            NoSuchElementException: Raised if an element is not found when compiling operation.
        """
        profile = self.get_profile(user)
        if not profile:
            raise InvalidUserError(user)

        followers = list()
        failed = list()
        last_callback = 0
        finished_warning = False

        start = time.time() # TODO
        
        if not use_api:
            # Nav User Page
            self._nav_user(user, check_user=False)

            # Nav Followers Page
            followers_btn:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_BTN)), url=ClientUrls.NAV_USER.format(user))
            # Click followers btn
            self._press_button(followers_btn)
            time.sleep(2)
            LOGGER.debug(f'Got Followers page for <{user}>')

            # Scrape
            try:
                while len(followers) < count:
                    loop = time.time() # TODO
                    LOGGER.debug(f'Starting Scrape Loop. Followers: {len(followers)}')
                    
                    scraped_count = len(followers)
                    divs = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.FOLLOWER_USER_DIV)), wait_time=2)

                    got_elements = time.time() # TODO
                    LOGGER.debug(f'Got Divs in {got_elements - loop}')

                    for div in divs:
                        try:
                            username = div.text.split('\n')[0]
                            if username not in followers and username not in('Follow',) and len(followers) < count:
                                followers.append(username)

                                if len(followers) % callback_frequency == 0:
                                    if callable(callback):
                                        LOGGER.debug('Called Callback')
                                        callback(scraped = followers, **callback_args)
                                    else:
                                        LOGGER.info(f'Scraped {len(followers)} followers so far...')

                        except:
                            failed.append(div)
                            pass
                    
                    if len(followers) >= count:
                        break

                    if not finished_warning and len(followers) == scraped_count:
                        if len(followers) == profile.follower_count:
                            LOGGER.info('Finished Followers')
                            break
                        LOGGER.info('Detected End of Followers Page')
                        finished_warning = True
                        time.sleep(3)
                    elif finished_warning:
                        LOGGER.info('Finished Followers')
                        break
                    else:
                        finished_warning = False

                    LOGGER.debug('Scroll')
                    self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
            except Exception as error:
                LOGGER.error('ERROR IN SCRAPING FOLLOWERS', exc_info=error)
        else:
            request = GraphUrls.GRAPH_FIRST_FOLLOWERS.format(QUERY_HASH=QueryHashes.FOLLOWERS_HASH, ID=profile.id)
            looping = True
            while looping:
                result = self._request(request, use_driver=True)

                if not result:
                    break

                status = result.get('status')
                if not status == 'ok':
                    break

                data = result['data']['user']['edge_followed_by']
                # Load users
                
                for user_data in data['edges']:
                    user = user_data['node']
                    follower = Profile(
                        client = self,
                        id = user['id'],
                        viewer = self.username,
                        username = user['username'],
                        name = user['full_name'],
                        is_private = user['is_private'],
                        is_verified = user['is_verified'],
                        requested_by_viewer = user['requested_by_viewer'],
                        profile_pic_url= user.get('profile_pic_url')
                    )
                    if len(followers) >= count:
                        looping = False
                        break
                    if follower not in followers:
                        followers.append(follower)

                        if len(followers) % callback_frequency == 0:
                            if callable(callback):
                                LOGGER.debug('Called Callback')
                                callback(scraped = followers, **callback_args)
                            else:
                                LOGGER.info(f'Scraped {len(followers)} followers so far...')

                # Get Page Info
                page_info = data['page_info']
                if not page_info['has_next_page']:
                    break
                else:
                    cursor = page_info['end_cursor'].replace('==', '')
                    request = GraphUrls.GRAPH_CURSOR_FOLLOWERS.format(QUERY_HASH=QueryHashes.FOLLOWERS_HASH, ID=profile.id, END_CURSOR=cursor)
                    continue
 

        end = time.time() # TODO
        LOGGER.info(f'Scraped Followers: Total: {len(followers)}')

        if not deep_scrape:
            return followers
        else:
            LOGGER.info('Deep scraping profiles...')
            # For every shortlink, scrape Post
            profiles = list()
            for index, follower in enumerate(followers):
                try:
                    if isinstance(follower, Profile):
                        profiles.append(follower.refresh())
                    else:
                        profiles.append(self.get_profile(follower))
                    LOGGER.debug(f'Deep scraped {index} profiles out of {len(followers)}')
                except:
                    failed.append(follower)
            LOGGER.warning(f'Failed: {len(failed)}')
            return profiles


    @Component._login_required
    def get_following(self:'InstaClient', user:str, count:int, use_api:bool=True, deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List[Profile], List[str]]]:
        """Scrape an instagram user's following.

        Args:
            user (str): User to scrape
            count (int): Number of followers to scrape
            use_api (bool): If set to True, the instaclient module will take advantage
                of instagram graphql requests to scrape followers. Defaults to False.
            callback_frequency (int, optional): Number of scraped followers between updates
            callback (function): Function with no parameters that gets called with the frequency set by ``callback_frequency``. This method must take a ``scraped`` argument.

        Returns:
            Optional[Union[List[Profile], List[str]]]: List of instagram usernames or of instagram profile objects

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account
            NoSuchElementException: Raised if an element is not found when compiling operation.
        """
        profile = self.get_profile(user)
        if not profile:
            raise InvalidUserError(user)

        following = list()
        failed = list()
        last_callback = 0
        finished_warning = False

        start = time.time() # TODO
        
        if not use_api:
            # Nav User Page
            self._nav_user(user, check_user=False)

            # Nav Followers Page
            following_btn:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWED_BTN)), url=ClientUrls.NAV_USER.format(user))
            # Click followers btn
            self._press_button(following_btn)
            time.sleep(2)
            LOGGER.debug(f'Got Following page for <{user}>')

            # Scrape
            try:
                while len(following) < count:
                    loop = time.time() # TODO
                    LOGGER.debug(f'Starting Scrape Loop. Following: {len(following)}')
                    
                    scraped_count = len(following)
                    divs = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.FOLLOWER_USER_DIV)), wait_time=2)

                    got_elements = time.time() # TODO
                    LOGGER.debug(f'Got Divs in {got_elements - loop}')

                    for div in divs:
                        try:
                            username = div.text.split('\n')[0]
                            if username not in following and username not in('Follow',) and len(following) < count:
                                following.append(username)

                                if len(following) % callback_frequency == 0:
                                    if callable(callback):
                                        LOGGER.debug('Called Callback')
                                        callback(scraped = following, **callback_args)
                                    else:
                                        LOGGER.info(f'Scraped {len(following)} following so far...')

                        except:
                            failed.append(div)
                            pass
                    
                    if len(following) >= count:
                        break

                    if not finished_warning and len(following) == scraped_count:
                        if len(following) == profile.follower_count:
                            LOGGER.info('Finished Following')
                            break
                        LOGGER.info('Detected End of Following Page')
                        finished_warning = True
                        time.sleep(3)
                    elif finished_warning:
                        LOGGER.info('Finished Following')
                        break
                    else:
                        finished_warning = False

                    LOGGER.debug('Scroll')
                    self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
            except Exception as error:
                LOGGER.error('ERROR IN SCRAPING FOLLOWERS', exc_info=error)
        else:
            request = GraphUrls.GRAPH_FIRST_FOLLOWING.format(QUERY_HASH=QueryHashes.FOLLOWING_HASH, ID=profile.id)
            looping = True
            while looping:
                result = self._request(request, use_driver=True)

                if not result:
                    break

                status = result.get('status')
                if not status == 'ok':
                    break

                data = result['data']['user']['edge_follow']
                # Load users
                
                for user_data in data['edges']:
                    user = user_data['node']
                    follower = Profile(
                        client = self,
                        id = user['id'],
                        viewer = self.username,
                        username = user['username'],
                        name = user['full_name'],
                        is_private = user['is_private'],
                        is_verified = user['is_verified'],
                        requested_by_viewer = user['requested_by_viewer'],
                        profile_pic_url= user.get('profile_pic_url')
                    )
                    if len(following) >= count:
                        looping = False
                        break
                    if follower not in following:
                        following.append(follower)

                        if len(following) % callback_frequency == 0:
                            if callable(callback):
                                LOGGER.debug('Called Callback')
                                callback(scraped = following, **callback_args)
                            else:
                                LOGGER.info(f'Scraped {len(following)} following so far...')

                # Get Page Info
                page_info = data['page_info']
                if not page_info['has_next_page']:
                    break
                else:
                    cursor = page_info['end_cursor'].replace('==', '')
                    request = GraphUrls.GRAPH_CURSOR_FOLLOWING.format(QUERY_HASH=QueryHashes.FOLLOWING_HASH, ID=profile.id, END_CURSOR=cursor)
                    continue
 

        end = time.time() # TODO
        LOGGER.info(f'Scraped Followers: Total: {len(following)}')

        if not deep_scrape:
            return following
        else:
            LOGGER.info('Deep scraping profiles...')
            # For every shortlink, scrape Post
            profiles = list()
            for index, follower in enumerate(following):
                try:
                    if isinstance(follower, Profile):
                        profiles.append(follower.refresh())
                    else:
                        profiles.append(self.get_profile(follower))
                    LOGGER.debug(f'Deep scraped {index} profiles out of {len(following)}')
                except:
                    failed.append(follower)
            LOGGER.warning(f'Failed: {len(failed)}')
            return profiles

        """Scrape an instagram user's following.

        Args:
            user (str): User to scrape
            count (int): Number of followers to scrape
            check_user (bool, optional): If set to True, checks if the `user` is a valid instagram username. Defaults to True.
            callback_frequency (int, optional): Number of scraped followers between updates
            callback (function): Function with no parameters that gets called with the frequency set by ``callback_frequency``. This method must take a ``scraped`` argument.

        Returns:
            Optional[Union[List[Profile], List[str]]]: List of instagram usernames or of instagram profile objects.

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account
            NoSuchElementException: Raised if an element is not found when compiling operation.
        """
        self._nav_user(user, check_user=check_user)
        following_btn:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWED_BTN)), url=ClientUrls.NAV_USER.format(user))
        # Click followers btn
        self._press_button(following_btn)
        time.sleep(2)
        LOGGER.debug(f'Got Following page for <{user}>')

        following = list()
        failed = list()
        last_callback = 0
        finished_warning = False

        start = time.time() # TODO
        
        try:
            while len(following) < count:
                loop = time.time() # TODO
                LOGGER.debug(f'Starting Scrape Loop. Followers: {len(following)}')
                
                scraped_count = len(following)
                divs = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.FOLLOWER_USER_DIV)), wait_time=2)

                got_elements = time.time() # TODO
                LOGGER.debug(f'Got Divs in {got_elements - loop}')

                new = 0
                for div in divs:
                    try:
                        username = div.text.split('\n')[0]
                        if username not in following and username not in('Follow',) and len(following) < count:
                            following.append(username)
                            new += 1

                            if (last_callback + new) % callback_frequency == 0:
                                if callable(callback):
                                    LOGGER.debug('Called Callback')
                                    callback(scraped = following, **callback_args)

                    except:
                        failed.append(div)
                        pass
                
                if len(following) >= count:
                    break

                if not finished_warning and len(following) == scraped_count:
                    LOGGER.info('Detected End of Followers Page')
                    finished_warning = True
                    time.sleep(3)
                elif finished_warning:
                    LOGGER.info('Finished Followers')
                    break
                else:
                    finished_warning = False

                LOGGER.debug('Scroll')
                self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
        except Exception as error:
            LOGGER.error('ERROR IN SCRAPING FOLLOWERS', exc_info=error)
                

        end = time.time() # TODO
        LOGGER.info(f'Scraped Followers: Total: {len(following)}')

        if not deep_scrape:
            return following
        else:
            LOGGER.info('Deep scraping profiles...')
            # For every shortlink, scrape Post
            profiles = list()
            for index, follower in enumerate(following):
                try:
                    LOGGER.debug(f'Deep scraped {index} profiles out of {len(following)}')
                    profiles.append(self.get_profile(follower))
                except:
                    failed.append(follower)
            LOGGER.warning(f'Failed: {len(failed)}')
            return profiles
    
    
    # SCRAPE HASHTAG
    @Component._driver_required
    def get_hashtag(self:'InstaClient', tag:str) -> Optional['Hashtag']:
        LOGGER.debug('INSTACLIENT: scrape hashtag')
        result = self._request(GraphUrls.GRAPH_TAGS.format(tag))

        if not result:
            return None

        try:
            data = result['graphql']['hashtag']
            tag:Hashtag = Hashtag(
                client=self,
                id=data['id'],
                viewer=self.username,
                name=data['name'],
                posts_count=data['edge_hashtag_to_media']['count'],
                allow_following=data['allow_following'],
                is_top_media_only=data['is_top_media_only'],
                is_following=data['is_following'],
            )
            LOGGER.info('Scraped hashtag: {}'.format(tag))
            return tag
        except Exception as error:
            LOGGER.exception('Error scraping hashtag', exc_info=error)
            raise InvalidInstaSchemaError(__name__)


    @Component._login_required
    def get_hashtag_posts(self:'InstaClient', tag:str, count:int, deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List[str], List[Post]]]:
        """Get a list of posts that match a specified hashtag.

        Args:
            tag (str): Hashtag to scrape from.
            count (int): Number of posts to load.
            deep_scrape (Optional[bool], optional): If set to True, every scraped post will
                be fully loaded into :class:`instaclient.Post` objects. Defaults to False.
            callback_frequency (int, optional): Frequency with which the method will
                call a specified callback method. The assigned value reflects the
                number of objects to scrape before calling the method. Defaults to 100.
            callback (callable, optional): Callable method that gets called with the frequency
                set by `callback_frequency`. Defaults to None.

        Returns:
            Optional[Union[List[str], List[Post]]]: Optional list of scraped posts. 
                The list may either contain a list of shortcodes or of :class:`instaclient.Post`
                based on the value of the attribute `deep_scrape`.
        """
        # Nav to Tag Page
        self._nav_tag(tag)

        # Scroll down and save shortcodes
        shortcodes = list()
        failed = list()
        last_callback = 0
        finished_warning = False
        
        # Shortcodes scraper loop
        try:
            while len(shortcodes) < count:
                
                

                loop = time.time() # TODO
                LOGGER.debug(f'Starting Post Scrape Loop. Posts: {len(shortcodes)}')
                
                scraped_count = len(shortcodes)
                divs = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.SHORTCODE_DIV)), wait_time=2)

                got_elements = time.time() # TODO
                LOGGER.debug(f'Got Divs in {got_elements - loop}')

                new = 0
                for div in divs:
                    try:
                        shortcode = div.get_attribute('href')
                        if shortcode:
                            shortcode = shortcode.replace('https://www.instagram.com/p/', '')
                            shortcode = shortcode.replace('/', '')
                        if shortcode not in shortcodes and shortcode not in (None,) and len(shortcodes) < count:
                            shortcodes.append(shortcode)
                            new += 1

                            if (last_callback + new) % callback_frequency == 0:
                                if callable(callback):
                                    LOGGER.debug('Called Callback')
                                    callback(scraped = shortcodes, **callback_args)

                    except:
                        failed.append(div)
                        pass
                
                if len(shortcodes) >= count:
                    break

                if not finished_warning and len(shortcodes) == scraped_count:
                    LOGGER.info('Detected End of Posts Page')
                    finished_warning = True
                    time.sleep(3)
                elif finished_warning:
                    LOGGER.info('Finished Posts')
                    break
                else:
                    finished_warning = False

                LOGGER.debug('Scroll')
                self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
        except Exception as error:
            LOGGER.error('ERROR IN SCRAPING POSTS', exc_info=error)
                
        LOGGER.warn(f'Failed: {len(failed)}')

        if not deep_scrape:
            return shortcodes
        else:
            # For every shortlink, scrape Post
            LOGGER.info('Deep scraping posts...')
            posts = list()
            for index, shortcode in enumerate(shortcodes):
                LOGGER.debug(f'Deep scraped {index} posts out of {len(shortcodes)}')
                posts.append(self.get_post(shortcode))
            return posts

    
    # SCRAPE LOCATION
    @Component._driver_required
    def get_location(self:'InstaClient', id:str, slug:str) -> Optional[Location]:
        """Get information about an instagram Location

        Args:
            id (str): `id` of the instagram location
            slug (str): `slug` of the instagram location

        Raises:
            InvalidInstaSchemaError: error raised if there is an error
                in the graphql instagram response. This error might be caused by changes
                in the instagram API. If you receive this error, contact
                the developers of this package.

        Returns:
            Optional[:class:`Location`]: If the `id` and `slug` attributes are valid,
                a :meth:`instagram.Location` object is returned.
        """
        result = self._request(GraphUrls.GRAPH_LOCATION.format(id, slug))

        if not result:
            return None

        try:
            data = result['graphql']['location']
            address = Address(data['address_json'])
            location:Location = Location(
                client=self,
                id=data['id'],
                viewer=self.username, 
                name=data['name'],
                slug=data['slug'],
                has_public_page=data['has_public_page'],
                lat=data['lat'],
                lng=data['lng'],
                posts_count=data['edge_location_to_media']['count'],
                blurb=data['blurb'],
                website=data['website'],
                primary_alias_on_fb=data['primary_alias_on_fb'],
                address=address
            )
            return location
        except Exception as error:
            LOGGER.exception('Error scraping location', exc_info=error)
            raise InvalidInstaSchemaError(__name__)

    
    @Component._driver_required
    def get_location_posts(self:'InstaClient', id:str, slug:str, count:int, deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List[str], List[Post]]]:
        """Get a list of posts that match a specified location.

        Args:
            id (str): ID of the location to scrape from.
            slug (str): Slug of the location to scrape from.
            count (int): Number of posts to load.
            deep_scrape (Optional[bool], optional): If set to True, every scraped post will
                be fully loaded into :class:`instaclient.Post` objects. Defaults to False.
            callback_frequency (int, optional): Frequency with which the method will
                call a specified callback method. The assigned value reflects the
                number of objects to scrape before calling the method. Defaults to 100.
            callback (callable, optional): Callable method that gets called with the frequency
                set by `callback_frequency`. Defaults to None.

        Returns:
            Optional[Union[List[str], List[Post]]]: Optional list of scraped posts. 
                The list may either contain a list of shortcodes or of :class:`instaclient.Post`
                based on the value of the attribute `deep_scrape`.
        """
        # Nav to Tag Page
        self._nav_location(id, slug)

        # Scroll down and save shortcodes
        shortcodes = list()
        failed = list()
        last_callback = 0
        finished_warning = False
        
        # Shortcodes scraper loop
        try:
            while len(shortcodes) < count:
                loop = time.time() # TODO
                LOGGER.debug(f'Starting Post Scrape Loop. Posts: {len(shortcodes)}')
                
                scraped_count = len(shortcodes)
                divs = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.SHORTCODE_DIV)), wait_time=2)

                got_elements = time.time() # TODO
                LOGGER.debug(f'Got Divs in {got_elements - loop}')

                new = 0
                for div in divs:
                    try:
                        shortcode = div.get_attribute('href')
                        if shortcode:
                            shortcode = shortcode.replace('https://www.instagram.com/p/', '')
                            shortcode = shortcode.replace('/', '')
                        if shortcode not in shortcodes and shortcode not in (None,) and len(shortcodes) < count:
                            shortcodes.append(shortcode)
                            new += 1

                            if (last_callback + new) % callback_frequency == 0:
                                if callable(callback):
                                    LOGGER.debug('Called Callback')
                                    callback(scraped = shortcodes, **callback_args)

                    except:
                        failed.append(div)
                        pass
                
                if len(shortcodes) >= count:
                    break

                if not finished_warning and len(shortcodes) == scraped_count:
                    LOGGER.info('Detected End of Posts Page')
                    finished_warning = True
                    time.sleep(3)
                elif finished_warning:
                    LOGGER.info('Finished Posts')
                    break
                else:
                    finished_warning = False

                LOGGER.debug('Scroll')
                self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
        except Exception as error:
            LOGGER.error('ERROR IN SCRAPING POSTS', exc_info=error)
                
        LOGGER.warn(f'Failed: {len(failed)}')

        if not deep_scrape:
            return shortcodes
        else:
            # For every shortlink, scrape Post
            LOGGER.info('Deep scraping posts...')
            posts = list()
            for index, shortcode in enumerate(shortcodes):
                LOGGER.debug(f'Deep scraped {index} posts out of {len(shortcodes)}')
                posts.append(self.get_post(shortcode))
            return posts


    # GENERAL TOOLS
    @Component._driver_required
    def get_search_results(self:'InstaClient', query:str) -> dict:
        """Get the results of a search query on Instagram.

        Args:
            query (str): Query to search on Instagram.

        Returns:
            dict: A dictionary with 3 keys: ``users``, ``locations``
                and ``hashtags``. Each respective value holds a list with
                the respective object types.
        """
        result = self._request(GraphUrls.GRAPH_SEARCH.format(query))

        if not result:
            return None

        users_data = result.get('users')
        locations_data = result.get('places')
        hashtags_data = result.get('hashtags')

        data = dict()

        users = list()
        for item in users_data:
            try:
                item = item['user']
                friendship_status = item.get('friendship_status')
                users.append(Profile(
                    self,
                    id=item['pk'],
                    viewer=self.username,
                    username=item['username'],
                    name=item['full_name'],
                    is_private=item['is_private'],
                    is_verified=item['is_verified'],
                    has_requested_viewer=friendship_status.get('incoming_request') if friendship_status else None,
                    requested_by_viewer=friendship_status.get('outgoing_request') if friendship_status else None,
                    profile_pic_url= item.get('profile_pic_url'),
                ))
            except:
                LOGGER.warning('Skipping user due to schema error...')
                pass

        locations = list()
        for item in locations_data:
            try:
                item = item['place']
                locations.append(Location(
                    client=self,
                    id=item['location']['pk'],
                    viewer=self.username,
                    name=item['title'],
                    slug=item['slug'],
                    lat=item['location']['lat'],
                    lng=item['location']['lng'],
                ))
            except:
                LOGGER.warning('Skipping location due to schema error...')
                pass

        tags = list()
        for item in hashtags_data:
            try:
                item = item['hashtag']
                tags.append(Hashtag(
                    client=self,
                    id=item['id'],
                    viewer=self.username,
                    name=item['name'],
                    posts_count=item['media_count'],
                ))
            except:
                LOGGER.warning('Skipping hashtag due to schema error...')
                pass

        data['users'] = users
        data['locations'] = locations
        data['hashtags'] = tags
        return data


    def _request(self: 'InstaClient', url:str, use_driver:bool=False) -> Optional[dict]:
        if not use_driver:
            if self.proxy:
                proxyDict = { 
                "http"  : self.proxy, 
                "https" : self.proxy, 
                "ftp"   : self.proxy
                }
                result = requests.get(url, proxies=proxyDict)
            else:
                result = requests.get(url)

            try:
                return result.json()
            except:
                use_driver = True
        
        if use_driver:
            try:
                self.driver.get(url)
                element:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.QUERY_ELEMENT)), wait_time=2, retry=False)
                source = element.text
                return json.loads(source)
            except:
                return None


    