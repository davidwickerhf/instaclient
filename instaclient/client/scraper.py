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
        for node in selected_nodes:
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


    #@Component._login_required
    def get_profile(self:'InstaClient', username:str, context:bool=False) -> Optional['Profile']:
        
        if context and not self.logged_in:
            if None in (self.username, self.password):
                raise NotLoggedInError()
            self.login(self.username, self.password)
        data = self._request(GraphUrls.GRAPH_USER.format(username), use_driver=context)

        if not data:
            if self.driver and (ClientUrls.LOGIN_URL in self.driver.current_url) or not self.driver:
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
                followed_by_viewer = user.get('followed_by_viewer'),
                follows_viewer= user.get('follows_viewer'),
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

    
    #@Component._driver_required
    def get_post(self:'InstaClient', shortcode:str, context:bool=False) -> Optional['Post']:
        if context and not self.logged_in:
            if None in (self.username, self.password):
                raise NotLoggedInError()
            self.login(self.username, self.password)

        data = self._request(GraphUrls.GRAPH_POST.format(shortcode), use_driver=context)
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
    def get_followers(self:'InstaClient', user:str, count:int, use_api:bool=True, deep_scrape:Optional[bool]=False, end_cursor:str=None, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List[Profile], List[str]]]:
        """Scrape an instagram user's followers.

        If `use_api` is set to True, you may reach a rate limit after the first 200 requests.
        Each request can hold up to 50 users, so you will be able to scrape a max of about 10000
        users, in a matter of 2 minutes. When the rate limit is reached, a cursor will be returned 
        along with the followers, so you can in a later time resume the scrape, placing that cursor
        as the value for the `end_cursor` parameter.

        Args:
            user (str): User to scrape
            count (int): Number of followers to scrape. Insert None
                to scrape all of the profile's followers.
            use_api (bool): If set to True, the instaclient module will take advantage
                of instagram graphql requests to scrape followers. Defaults to False.
            deep_scrape (bool, optional): If set to True, the instaclient module will
                scrape each profile individually in order to get more information.
            end_cursor (str, optional): The END CURSOR of the scrape pagination that can be
                used to resume the scrape from a certain point.
            callback_frequency (int, optional): Number of scraped followers between updates
            callback (function): Function with no parameters that gets called with the frequency 
                set by ``callback_frequency``. This method must take a ``scraped`` argument.

        Returns:
            Union[Optional[Union[List[Profile], List[str]]], Optional[str]]: List of instagram 
                usernames or of instagram profile objects and the last cursor used for the scrape
                If the parameter `use_api` is set to True, the second returned value will be None.

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account
            NoSuchElementException: Raised if an element is not found when compiling operation.
        """
        profile = self.get_profile(user)
        if not profile:
            raise InvalidUserError(user)

        if not count:
            count = profile.follower_count

        followers = list()
        failed = list()
        finished_warning = False
        cursor = end_cursor
        
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
            if not cursor:
                request = GraphUrls.GRAPH_FIRST_FOLLOWERS.format(QUERY_HASH=QueryHashes.FOLLOWERS_HASH, ID=profile.id)
            else:
                request = GraphUrls.GRAPH_CURSOR_FOLLOWERS.format(QUERY_HASH=QueryHashes.FOLLOWERS_HASH, ID=profile.id, END_CURSOR=cursor)
            requests = 1
            looping = True
            while looping:
                result = self._request(request, use_driver=True)
                requests += 1

                if not result:
                    break

                status = result.get('status')
                if not status == 'ok':
                    if result.get('message') == 'rate limited':
                        LOGGER.exception('Rate limit reached. Stopping scrape.')
                        break
                    else:
                        LOGGER.exception(f'The request with cursor {cursor} failed')
                        break

                data = result['data']['user']['edge_followed_by']

                # Get Page Info
                page_info = data.get('page_info')
                if not page_info or not page_info.get('end_cursor'):
                    cursor = None
                    looping = False
                else:
                    cursor = page_info['end_cursor'].replace('==', '')
                    request = GraphUrls.GRAPH_CURSOR_FOLLOWERS.format(QUERY_HASH=QueryHashes.FOLLOWERS_HASH, ID=profile.id, END_CURSOR=cursor)
                
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
                        follows_viewer = user['follows_viewer'],
                        followed_by_viewer = user['followed_by_viewer'],
                        requested_by_viewer = user['requested_by_viewer'],
                        profile_pic_url= user.get('profile_pic_url')
                    )
                    if len(followers) >= count:
                        looping = False
                        break
                    if follower not in followers:
                        followers.append(follower)

                        if len(followers) % callback_frequency == 0:
                            LOGGER.debug(f'Requests made: {requests}')
                            if callable(callback):
                                LOGGER.debug('Called Callback')
                                callback(scraped = followers, **callback_args)
                            else:
                                LOGGER.info(f'Scraped {len(followers)} followers so far...')

            LOGGER.debug(f'Requests made: {requests}')

        LOGGER.info(f'Scraped: {len(followers)}')

        if not deep_scrape:
            return followers, cursor
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
            return profiles, cursor


    @Component._login_required
    def get_following(self:'InstaClient', user:str, count:int, use_api:bool=True, deep_scrape:Optional[bool]=False, end_cursor:str=None, callback_frequency:int=100, callback=None, **callback_args) -> Union[Optional[Union[List[Profile], List[str]]], Optional[str]]:
        """Scrape an instagram user's following.

        If `use_api` is set to True, you may reach a rate limit after the first 200 requests.
        Each request can hold up to 50 users, so you will be able to scrape a max of about 10000
        users, in a matter of 2 minutes. When the rate limit is reached, a cursor will be returned 
        along with the followers, so you can in a later time resume the scrape, placing that cursor
        as the value for the `end_cursor` parameter.

        Args:
            user (str): User to scrape
            count (int): Number of followers to scrape. Insert
                None to get all of the profile's following.
            use_api (bool): If set to True, the instaclient module will take advantage
                of instagram graphql requests to scrape followers. Defaults to False.
            end_cursor (str, optional): The END CURSOR of the scrape pagination that can be
                used to resume the scrape from a certain point.
            callback_frequency (int, optional): Number of scraped followers between updates
            callback (function): Function with no parameters that gets called with the frequency 
                set by ``callback_frequency``. This method must take a ``scraped`` argument.

        Returns:
            Union[Optional[Union[List[Profile], List[str]]], Optional[str]]: List of instagram 
                usernames or of instagram profile objects and the last cursor used for the scrape
                If the parameter `use_api` is set to True, the second returned value will be None.

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account
            NoSuchElementException: Raised if an element is not found when compiling operation.
        """
        profile = self.get_profile(user)
        if not profile:
            raise InvalidUserError(user)

        if not count:
            count = profile.followed_count

        following = list()
        failed = list()
        cursor = None
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
            
            if not end_cursor:
                request = GraphUrls.GRAPH_FIRST_FOLLOWING.format(QUERY_HASH=QueryHashes.FOLLOWING_HASH, ID=profile.id)
            else: 
                request = GraphUrls.GRAPH_CURSOR_FOLLOWING.format(QUERY_HASH=QueryHashes.FOLLOWING_HASH, ID=profile.id, END_CURSOR=end_cursor)
            requests = 1
            looping = True
            while looping:
                result = self._request(request, use_driver=True)
                requests += 1

                if not result:
                    break

                status = result.get('status')
                if not status == 'ok':
                    if result.get('message') == 'rate limited':
                        LOGGER.exception('Rate Limited. Stopping scrape')
                        break
                    else:
                        LOGGER.exception(f'The request with cursor {cursor} failed')
                        break
                data = result['data']['user']['edge_follow']
                

                # Get Page Info
                page_info = data.get('page_info')
                if not page_info or not page_info.get('end_cursor'):
                    cursor = None
                    looping = False
                else:
                    cursor = page_info['end_cursor'].replace('==', '')
                    request = GraphUrls.GRAPH_CURSOR_FOLLOWING.format(QUERY_HASH=QueryHashes.FOLLOWING_HASH, ID=profile.id, END_CURSOR=cursor)

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
                        follows_viewer = user['follows_viewer'],
                        followed_by_viewer = user['followed_by_viewer'],
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

                

            LOGGER.debug(f'Requests made: {requests}')
 
        LOGGER.info(f'Scraped: {len(following)}')

        if not deep_scrape:
            return following, cursor
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
            return profiles, cursor

    
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
                    followed_by_viewer = None if not friendship_status else friendship_status.get('is_following') ,
                    has_requested_viewer=None if not friendship_status else friendship_status.get('incoming_request'),
                    requested_by_viewer=None if not friendship_status else friendship_status.get('outgoing_request'),
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
            headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}
            if self.proxy:
                proxyDict = { 
                "http"  : f'{self.proxy}:{self.port}', 
                "https" : f'{self.proxy}:{self.port}', 
                "ftp"   : f'{self.proxy}:{self.port}'
                }
                result = requests.get(url, proxies=proxyDict, headers=headers)
            else:
                result = requests.get(url, headers=headers)

            try:
                if result.json():
                    return result.json()
                else:
                    use_driver = True
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