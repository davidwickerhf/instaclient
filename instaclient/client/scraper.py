import json, requests

from instaclient.client import *
from instaclient.client.instaclient import InstaClient
from instaclient.instagram import (InstaBaseObject, Profile, Notification, Hashtag)
from instaclient.errors.common import *


class Scraper:
    TYPES = [InstaBaseObject.GRAPH_IMAGE, InstaBaseObject.GRAPH_VIDEO, InstaBaseObject.GRAPH_SIDECAR]
    
    # SCRAPE HASHTAG
    @classmethod
    def _scrape_tag(cls, client:'InstaClient', tag:str, viewer:str):
        request = cls.get_url(GraphUrls.GRAPH_TAGS.format(tag), client.scraperapi_key)
        if client.proxy:
            proxyDict = { 
              "http"  : client.proxy, 
              "https" : client.proxy, 
              "ftp"   : client.proxy
            }
            result = requests.get(request, proxies=proxyDict)
        else:
            result = requests.get(request)

        try:
            result.json()
        except:
            raise InvalidInstaRequestError(request)

        try:
            data = result['graphql']['hashtag']
            tag:Hashtag = Hashtag(
                id=data['id'],
                viewer=viewer,
                name=data['name'],
                count=data['edge_hashtag_to_media']['count'],
                posts_data=data['edge_hashtag_to_media']
            )
            logger.info('Scraped hashtag: {}'.format(tag))
            return tag
        except:
            raise InvalidInstaSchemaError(__name__)


    # SCRAPE PROFILE


    # SCRAPE NOTIFICATIONS
    @classmethod
    def _scrape_notifications(cls, client:'InstaClient', source:int, viewer:str, types:list=None, count:int=None):

        if types is None or len(types) == 0:
            types = [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]
        else:
            for type in types:
                if type not in [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]:
                    raise InvalidNotificationTypeError(type)
        
        nodes = cls.__scrape_nodes(source, types, count)
        notifications = []

        # Map nodes into Notification Objects
        try:
            viewer = Profile.from_username(viewer, proxy=client.proxy, scraperapi_key=client.scraperapi_key)
        except InvalidInstaRequestError as error:
            logger.error(f'InvalidInstaRequestError intercepted. Creating {viewer} profile with username.', exc_info=error)
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
        logger.info('NODE COUNT: {}'.format(len(nodes)))

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


    def _request(self, url):
        pass
