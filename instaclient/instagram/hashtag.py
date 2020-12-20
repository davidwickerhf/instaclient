import json
from urllib.parse import urlencode
from instaclient.errors.common import InvalidInstaRequestError
from instaclient.client.constants import GraphUrls
from instaclient.instagram import InstaBaseObject, Post, Profile
import requests

class Hashtag(InstaBaseObject):
    def __init__(self, id:str, viewer:int or Profile, name:str, count:int, posts_data:str or dict, loaded_posts:list=[]):
        super().__init__(id, viewer, InstaBaseObject.GRAPH_HASHTAG)
        self.name = name
        self.count = count
        self.posts_data = posts_data
        self.loaded_posts = loaded_posts

    def __repr__(self) -> str:
        return f'Hashtag<{self.name}: {self.count}>'

    def get_posts_data(self):
        return self.posts_data.copy()

    def get_loaded_posts(self):
        return self.load_posts.copy()

    def load_posts(self, count:int, types:list=None):
        loaded = list()
        posts_data = self.get_posts_data()
        for index, data in enumerate(posts_data['edges']):
            post = Post(
                id=data[index]['id'],
                viewer=self.viewer,
                type=data[index]['__typename'],
                text=data[index]['edge_media_to_caption']['edges'][0]['node']['text'],
                shortcode=data[index]['shortcode'],
                proxy=self.proxy,
                scraperapi_key=self.scraperapi_key
            )
            loaded.append(post)
            if index >= count-1:
                break

        self.load_posts.extend(loaded)
        return self.loaded_posts.copy()

        """ # TODO
        if posts_data['page_info']['has_next_page']:
            di = {'id': user_id, 'first': 12, 'after': cursor}
            print(di)
            params = {'query_hash': 'e769aa130647d2354c40ea6a439bfc08', 'variables': json.dumps(di)}
            url = 'https://www.instagram.com/graphql/query/?' + urlencode(params) """

            



