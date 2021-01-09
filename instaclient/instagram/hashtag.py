import json
from urllib.parse import urlencode
from instaclient.errors.common import InvalidInstaRequestError
from instaclient.client.constants import GraphUrls
from instaclient.instagram import InstaBaseObject, Post, Profile

class Hashtag(InstaBaseObject):
    def __init__(self, 
    id:str, 
    viewer:str,
    name:str, 
    count:int):
        super().__init__(id, viewer, InstaBaseObject.GRAPH_HASHTAG)
        self.name = name
        self.count = count

    def __repr__(self) -> str:
        return f'Hashtag<{self.name}: {self.count}>'

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Hashtag):
            if o.name == self.name:
                return True
        return False


