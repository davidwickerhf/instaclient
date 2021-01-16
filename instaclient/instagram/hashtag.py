import json
from typing import TYPE_CHECKING, Optional, Union, List
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


    def get_posts(self, count:Optional[int]=None, deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List['Post'], List[str]]]:
        """Shortcut for::
            client.get_hashtag_posts(username, count, deep_scrape, callback_frequency, callback, **callback_args)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_hashtag_posts`.

        Returns:
            Optional[Union[List[`instagram.Post`], List[str]]]: If the `deep_scrape` attribute is set to true,
            this method will return a list of `instagram.Post` objects. Else, a list of post shortcodes 
            will be returned instead.
        """
        if not count:
            count = self.posts_count
        return self.client.get_location_posts(self.name, count, deep_scrape, callback_frequency, callback, **callback_args)

    


