from instaclient.classes.hashtag import Hashtag
from instaclient.errors.common import InvalidInstaRequestError, InvalidInstaSchemaError
import json

import requests
from instaclient.client.urls import GraphUrls
from instaclient.classes.instaobject import InstaBaseObject
from instaclient.classes.baseprofile import BaseProfile
from instaclient.classes.notification import Notification

class TagScraper: # TODO
    TYPES = [InstaBaseObject.GRAPH_IMAGE, InstaBaseObject.GRAPH_VIDEO, InstaBaseObject.GRAPH_SIDECAR]

    def __init__(self, logger):
        self.logger = logger


    def _scrape_tag(self, tag:str, viewer:str or int or BaseProfile):
        request = GraphUrls.GRAPH_TAGS.format(tag)
        try:
            result = requests.get(request).json()
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
            self.logger.info('Scraped hashtag: {}'.format(tag))
            return tag
        except:
            raise InvalidInstaSchemaError(__name__)