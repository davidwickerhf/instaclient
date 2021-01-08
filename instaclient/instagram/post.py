# Others
import requests
from typing import TYPE_CHECKING, Type, List, Optional, Union

# Objects
if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
    from instaclient.instagram.location import Location
from instaclient.instagram.postmedia import PostMedia
from instaclient.instagram.instaobject import InstaBaseObject
from instaclient.instagram.comment import Comment
from instaclient.instagram.profile import Profile
# INSTACLIENT
from instaclient.errors.common import InvalidInstaRequestError, InvalidInstaSchemaError
from instaclient.client.constants import GraphUrls
from instaclient import LOGGER


class Post(InstaBaseObject):
    def __init__(self, 
    # Required
    client:'InstaClient',
    id:int, 
    type:str,
    viewer:str, 
    owner:str,
    shortcode:str,
    timestamp:int,
    likes_count:int,
    comments_disabled:bool,
    is_ad:bool,
    media:List[PostMedia],

    # Optional
    caption:Optional[str]=None,
    comments_count:Optional[int]=None,
    tagged_users:Optional[List[str]]=None,
    comments:Optional[List[Comment]]=None,
    location:Optional['Location']=None,
     
    # Context Based
    commenting_disabled_for_viewer:Optional[bool]=None,
    viewer_has_liked:Optional[bool]=None,
    viewer_has_saved:Optional[bool]=None,
    viewer_has_saved_to_collection:Optional[bool]=None,
    viewer_in_photo_of_you:Optional[bool]=None,
    viewer_can_reshare:Optional[bool]=None,
    ):  
        super().__init__(id=id, type=type, viewer=viewer, client=client)
        # Required
        self.owner = owner
        self.shortcode = shortcode
        
        self.timestamp = timestamp
        self.likes_count = likes_count
        self.comments_disabled = comments_disabled
        self.is_ad = is_ad
        self.media = media

        # Optional
        self.caption = caption
        self.comments_count = comments_count
        self.tagged_users = tagged_users
        self.comments = comments
        self.location = location

        # Context Based
        self.commenting_disabled_for_viewer = commenting_disabled_for_viewer
        self.viewer_has_liked = viewer_has_liked
        self.viewer_has_saved = viewer_has_saved
        self.viewer_has_saved_to_collection = viewer_has_saved_to_collection 
        self.viewer_in_photo_of_you = viewer_in_photo_of_you
        self.viewer_can_reshare = viewer_can_reshare

    def __repr__(self) -> str:
        return f'Post<{self.shortcode}>'

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Post):
            if o.owner == self.owner and o.shortcode == o.shortcode:
                return True
        return False

    def refresh(self, context:bool=True):
        refreshed = self.client.get_post(self.shortcode, context)
        return self._update(refreshed)

    def get_owner(self) -> Optional[Profile]:
        return self.client.get_profile(self.owner)

    def add_comment(self, text) -> Optional[Comment]:
        result = self.client.comment_post(self.shortcode, text)
        if result:
            return self.client._find_comment(self.shortcode, self.client.username, text)
        return None

    def like(self):
        post = self.client.like_post(self.shortcode)
        return self._update(post)

    def unlike(self):
        post = self.client.unlike_post(self.shortcode)
        return self._update(post)


    




