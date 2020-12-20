import requests, json

from instaclient.client import *
if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.client.component import Component


class Scraper(Component):
    TYPES = [InstaBaseObject.GRAPH_IMAGE, InstaBaseObject.GRAPH_VIDEO, InstaBaseObject.GRAPH_SIDECAR]

    # SCRAPE HASHTAG
    @Component._manage_driver(login=False)
    def _scrape_tag(self:'InstaClient', tag:str, viewer:str):
        LOGGER.debug('INSTACLIENT: scrape hashtag')
        result = self._request(GraphUrls.GRAPH_TAGS.format(tag))

        try:
            data = result['graphql']['hashtag']
            tag:Hashtag = Hashtag(
                id=data['id'],
                viewer=viewer,
                name=data['name'],
                count=data['edge_hashtag_to_media']['count'],
                posts_data=data['edge_hashtag_to_media']
            )
            LOGGER.info('Scraped hashtag: {}'.format(tag))
            return tag
        except:
            raise InvalidInstaSchemaError(__name__)


    # SCRAPE PROFILE
        
    @Component._manage_driver()
    def get_notifications(self, types:list=None, count:int=None, _discard_driver=False):
        LOGGER.debug('INSTACLIENT: check_notifications')
        self.driver.get(GraphUrls.GRAPH_ACTIVITY)
        element:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.QUERY_ELEMENT)))
        source = element.text        
        notifications = self._scrape_notifications(source, viewer=self.username, types=types, count=count)
        return notifications




    # SCRAPE NOTIFICATIONS
    
    def _scrape_notifications(cls, client:'InstaClient', source:int, viewer:str, types:list=None, count:int=None):

        if types is None or len(types) == 0:
            types = [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]
        else:
            for type in types:
                if type not in [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]:
                    raise InvalidNotificationTypeError(type)
        
        nodes = self.__scrape_nodes(source, types, count)
        notifications = []

        # Map nodes into Notification Objects
        try:
            viewer = Profile.from_username(viewer, proxy=client.proxy, scraperapi_key=client.scraperapi_key)
        except InvalidInstaRequestError as error:
            LOGGER.error(f'InvalidInstaRequestError intercepted. Creating {viewer} profile with username.', exc_info=error)
            viewer = Profile.username_profile(viewer)
            
        for node in nodes:
            user = Profile(
                id=node['user']['id'],
                viewer=viewer,
                username=node['user']['username'],
                name=node['user']['full_name']
            )
            notifications.append(Notification(
                id=node['id'],
                viewer=viewer,
                from_user=user,
                type=node['__typename'],
                timestamp=node['timestamp'],
            ))
        return notifications


    def __scrape_nodes(self, source:str, types:list, count:int=None):
        data = json.loads(source)
        nodes = self.__parse_notifications(data)
        LOGGER.info('NODE COUNT: {}'.format(len(nodes)))

        selected_nodes = []
        for node in nodes:
            if count is not None and len(selected_nodes) >= count:
                break
            else:
                if node.get('__typename') in types:
                    selected_nodes.append(node)
        return selected_nodes


    def __parse_notifications(self, data):
        try:
            edges = data['graphql']['user']['activity_feed']['edge_web_activity_feed']['edges']
            nodes = []
            for edge in edges:
                if edge.get('node') is not None:
                    nodes.append(edge.get('node'))
            return nodes
        except:
            raise InvalidInstaSchemaError(__name__)


    def _request(self: 'InstaClient', url:str, use_driver):
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
            raise InvalidInstaRequestError(url)


    # USER DATA PRODECURES
    @Component._manage_driver()
    def get_user_images(self, user:str, _discard_driver:bool=False):
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
            
            elements = self._find_element((EC.presence_of_element_located(By.CLASS_NAME, 'FFVAD')))
            img_srcs.extend([img.get_attribute('src') for img in elements]) # scrape srcs

        img_srcs = list(set(img_srcs)) # clean up duplicates
        return img_srcs
    
 
    @Component._manage_driver(login=False)
    def _scrape_followers(self, user:str, count:int, check_user=True, _discard_driver=False, callback_frequency:int=100, callback=None, **callback_args):
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
        followers_btn:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.FOLLOWERS_BTN)), url=ClientUrls.NAV_USER.format(user))
        # Click followers btn
        self._press_button(followers_btn)
        time.sleep(2)
        LOGGER.info(f'Got Followers page for <{user}>')

        followers = list()
        failed = list()
        last_callback = 0

        start = time.time() # TODO
        
        try:
            while len(followers) < count:
                finished_warning = False
                

                loop = time.time() # TODO
                LOGGER.debug(f'Starting Scrape Loop. Followers: {len(followers)}')
                
                scraped_count = len(followers)
                divs = self._find_element(EC.presence_of_all_elements_located((By.XPATH, Paths.FOLLOWER_USER_DIV)), wait_time=2)

                got_elements = time.time() # TODO
                LOGGER.debug(f'Got Divs in {got_elements - loop}')

                new = 0
                for div in divs:
                    try:
                        username = div.text.split('\n')[0]
                        if username not in followers and username not in('Follow',) and len(followers) < count:
                            followers.append(username)
                            new += 1

                            if (last_callback + new) % callback_frequency == 0:
                                if callable(callback):
                                    LOGGER.debug('Called Callback')
                                    callback(**callback_args)

                    except:
                        failed.append(div)
                        pass
                
                if len(followers) >= count:
                    break

                if not finished_warning and len(followers) == scraped_count:
                    LOGGER.info('Detected End of Followers Page')
                    finished_warning = True
                    time.sleep(3)
                elif finished_warning:
                    LOGGER.info('Finished Followers')
                    break

                LOGGER.debug('Scroll')
                self.scroll(mode=self.END_PAGE_SCROLL, times=2, interval=1)
        except Exception as error:
            LOGGER.error('ERROR IN SCRAPING FOLLOWERS', exc_info=error)
                

        end = time.time() # TODO
        LOGGER.debug(f'Finished. Total: {end - start}')
        LOGGER.debug(f'Failed: {len(failed)}')
        return followers
        