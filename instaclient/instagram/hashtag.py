import json
from typing import TYPE_CHECKING
from urllib.parse import urlencode
from instaclient.errors.common import InvalidInstaRequestError
from instaclient.client.constants import GraphUrls
from instaclient.instagram import InstaBaseObject, Post, Profile
if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient

class Hashtag(InstaBaseObject):
    def __init__(self, 
    client:'InstaClient',
    id:str, 
    viewer:str,
    name:str, 
    posts_count:int=None,
    allow_following:bool=None,
    is_top_media_only:bool=None,
    is_following:bool=None
    ):
        super().__init__(client, id, InstaBaseObject.GRAPH_HASHTAG, viewer)
        self.name = name
        self.posts_count = posts_count
        self.allow_following = allow_following
        self.is_top_media_only = is_top_media_only
        self.is_following = is_following


    def __repr__(self) -> str:
        return f'Hashtag<{self.name}: {self.posts_count}>'


    def __eq__(self, o: object) -> bool:
        if isinstance(o, Hashtag):
            if o.name == self.name:
                return True
        return False


    def get_posts(self, count:int=None, deep_scrape:bool=False, callback_frequency:int=100, callback=None, **callback_args):
        if not count:
            count = self.posts_count
        return self.client.get_hashtag_posts(self.name, count, deep_scrape, callback_frequency, callback, **callback_args)

    


