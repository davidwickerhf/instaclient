from instaclient.utilities.utilities import get_url
from instaclient.classes.hashtag import Hashtag
from instaclient.errors.common import InvalidInstaRequestError, InvalidInstaSchemaError
import json, requests
from instaclient.client.urls import GraphUrls
from instaclient.classes.instaobject import InstaBaseObject
from instaclient.classes.baseprofile import BaseProfile

class TagScraper: # TODO
    TYPES = [InstaBaseObject.GRAPH_IMAGE, InstaBaseObject.GRAPH_VIDEO, InstaBaseObject.GRAPH_SIDECAR]

    def __init__(self, logger, proxy:str=None, scraperapi_key:str=None):
        self.logger = logger
        self.proxy=proxy
        self.scraperapi_key=scraperapi_key


    def _scrape_tag(self, tag:str, viewer:str or int or BaseProfile):
        request = get_url(GraphUrls.GRAPH_TAGS.format(tag), self.scraperapi_key)
        if self.proxy:
            proxyDict = { 
              "http"  : self.proxy, 
              "https" : self.proxy, 
              "ftp"   : self.proxy
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
            self.logger.info('Scraped hashtag: {}'.format(tag))
            return tag
        except:
            raise InvalidInstaSchemaError(__name__)

    def _get_url(self, url):
        return get_url(url, self.scraperapi_key)