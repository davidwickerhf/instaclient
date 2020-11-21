from instaclient.client.scraper import Scraper
import json

import requests
from instaclient.client.urls import GraphUrls
from instaclient.classes.instaobject import InstaBaseObject
from instaclient.classes.baseprofile import BaseProfile
from instaclient.classes.notification import Notification

class TagScraper(Scraper): # TODO
    TYPES = [InstaBaseObject.GRAPH_IMAGE, InstaBaseObject.GRAPH_VIDEO, InstaBaseObject.GRAPH_SIDECAR]

    def __init__(self, logger):
        self.logger = logger


    def _scrape_tag(self, tag:str, viewer:int, types:list=None, count:int=None):

        if types is None or len(types) == 0:
            types = self.TYPES
        else:
            for type in types:
                if type not in self.TYPES:
                    raise InvalidNotificationTypeError(type)
        
        try:
            source = requests.get(GraphUrls.GRAPH_TAGS.format(tag)).json()
        except ValueError:
            print('No Data Found')
        nodes = self.__scrape_nodes(source, types, count)
        notifications = []

        # Map nodes into Notification Objects
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
                user=user,
                type=node['__typename'],
                timestamp=node['timestamp']
            ))
        return notifications


    def __parse_notifications(self, data):
        edges = data['graphql']['user']['activity_feed']['edge_web_activity_feed']['edges']
        nodes = []
        for edge in edges:
            if edge.get('node') is not None:
                nodes.append(edge.get('node'))
        return nodes

    def __parse_posts(self, data):
        edges = data[]
        node = []
        for edge in edges:
            if edge.get('node') is not None:
                nodes.append(edge.get('node'))
        return nodes