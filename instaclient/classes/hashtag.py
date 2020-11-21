from instaclient.errors.common import InvalidInstaRequestError
from instaclient.client.urls import GraphUrls
from instaclient.classes import InstaBaseObject, BasePost, BaseProfile
import requests

class Hashtag(InstaBaseObject):
    def __init__(self, id:str, viewer:int or BaseProfile, name:str, count:int, posts_data:str or dict, loaded_posts:list=None):
        super().__init__(id, viewer, InstaBaseObject.GRAPH_HASHTAG)
        self.name = name
        self.count = count
        self.posts_data = posts_data
        self.loaded_posts = loaded_posts

    def __repr__(self) -> str:
        return f'Hashtag<{self.name}: {self.count}>'

    def load_posts(self, count:int, types:list=None):
        print()


