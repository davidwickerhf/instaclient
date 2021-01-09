# Others
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
    """Class reppresenting an Instagram Post

    The instagram post class inherits from the `instagram.InstaBaseObjects` class.
    This class should contain all methods related to actions one can execute on 
    posts on Instagram (such as liking, commenting, etc).

    Two `instagram.Post` objects are considered equal if they share the 
    same `shortcode` and the same `owner`.

    Attributes:
        client (:class:`instaclient.InstaClient`): This is the client instance that 
            will be used to perform actions on the object. Many methods included in 
            this class are in fact shortcuts for the `instaclient.InstaClient` 's methods. 

        id (str): The unique ID of the post, provided and defined by Instagram.

        type (str): Type of Post. This can be:
            `InstaBaseObject.GRAPH_IMAGE`,  `InstaBaseObject.GRAPH_VIDEO`,
            `InstaBaseObject.GRAPH_SIDECAR`

        viewer (str): The instagram account's username of the account the user is 
            currently logged in with, when loading this object from Instagram.
        
        owner (str): The username of the instagram account this Post belongs to.

        shortcode (str): Unique identifier of the Post.

        timestamp (int): Timestamp of the date of pubblication of the post on IG.

        likes_count (int): Number of likes a post has received.
        
        comments_disabled (bool): [description]
        is_ad (bool): [description]
        media (List[PostMedia]): [description]
        caption (str, optional): [description]. Defaults to None.
        comments_count (int, optional): [description]. Defaults to None.
        tagged_users (List[str], optional): [description]. Defaults to None.
        comments (List[Comment], optional): [description]. Defaults to None.
        location (Location, optional): [description]. Defaults to None.
        commenting_disabled_for_viewer (bool, optional): [description]. Defaults to None.
        viewer_has_liked (bool, optional): [description]. Defaults to None.
        viewer_has_saved (bool, optional): [description]. Defaults to None.
        viewer_has_saved_to_collection (bool, optional): [description]. Defaults to None.
        viewer_in_photo_of_you (bool, optional): [description]. Defaults to None.
        viewer_can_reshare (bool, optional): [description]. Defaults to None.
     """
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
    caption:str=None,
    comments_count:int=None,
    tagged_users:List[str]=None,
    comments:List[Comment]=None,
    location:Location=None,
     
    # Context Based
    commenting_disabled_for_viewer:bool=None,
    viewer_has_liked:bool=None,
    viewer_has_saved:bool=None,
    viewer_has_saved_to_collection:bool=None,
    viewer_in_photo_of_you:bool=None,
    viewer_can_reshare:bool=None,
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


    




