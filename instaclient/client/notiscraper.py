from instaclient.errors.common import InvalidNotificationTypeError
import json, requests
import types
from instaclient.client.urls import GraphUrls
from instaclient.classes.instaobject import InstaBaseObject
from instaclient.classes.baseprofile import BaseProfile
from instaclient.classes.notification import Notification

class NotificationScraper:

    def __init__(self, logger):
        self.logger = logger


    def _scrape_notifications(self, source:int, viewer:int, types:list=None, count:int=None):

        if types is None or len(types) == 0:
            types = [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]
        else:
            for type in types:
                if type not in [InstaBaseObject.GRAPH_FOLLOW, InstaBaseObject.GRAPH_LIKE, InstaBaseObject.GRAPTH_TAGGED, InstaBaseObject.GRAPH_COMMENT, InstaBaseObject.GRAPH_MENTION]:
                    raise InvalidNotificationTypeError(type)
        
        nodes = self.__scrape_nodes(source, types, count)
        notifications = []

        # Map nodes into Notification Objects
        viewer = BaseProfile.from_username(viewer)
        for node in nodes:
            user = BaseProfile(
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
        self.logger.debug('NODE COUNT:\n{}'.format(len(nodes)))

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
    
    """ def __get_url(self, url):
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url  """