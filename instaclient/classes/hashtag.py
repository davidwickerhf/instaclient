from instaclient.classes import InstaBaseObject, BasePost, BaseProfile

class Hashtag(InstaBaseObject):
    def __init__(self, id:str, viewer:int or BaseProfile, name:str, count:int, loaded_posts:list, data:str or dict):
        super().__init__(id, viewer, InstaBaseObject.GRAPH_HASHTAG)
        self.name = name
        self.count = count
        self.loaded_posts = loaded_posts
        self.data = data

    def from_data(data:str, count:int):
        