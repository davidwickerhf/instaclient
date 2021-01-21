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
            ``InstaBaseObject.GRAPH_IMAGE``,  ``InstaBaseObject.GRAPH_VIDEO``,
            ``InstaBaseObject.GRAPH_SIDECAR``

        viewer (str): The instagram account's username of the account the user is 
            currently logged in with, when loading this object from Instagram.
        
        owner (str): The username of the instagram account this Post belongs to.

        shortcode (str): Unique identifier of the Post.

        timestamp (int): Timestamp of the date of pubblication of the post on IG.

        likes_count (int): Number of likes a post has received.
        
        comments_disabled (bool): IF set to True, the owner of this post has
            disabled comments for this post.

        is_ad (bool): If True, this post is an Advertisement.

        media (List[:class:`PostMedia`]): List of :class:`PostMedia` objects, which
            contain information about the post media.

        caption (str, optional): The caption of the post. Defaults to None.

        comments_count (int, optional): The number of comments under the post. 
            Defaults to None.

        tagged_users (List[str], optional): A list of usernames of the 
            instagram users tagged on this post. Defaults to None.

        comments (List[:class:`Comment`], optional): List of available comments,
            present in the graphql response. Defaults to None.

            Note:
                Not all comments on this post might be included in this list.

        location (:class:`Location`, optional): Location attached to this post. 
            Defaults to None.
    
        commenting_disabled_for_viewer (bool, optional): If True, the viewer is
            not allowed to comment on this post. Defaults to None.

        viewer_has_liked (bool, optional): If True, the viewer has liked this
            post. Defaults to None.

        viewer_has_saved (bool, optional): If True, the viewer has saved this
            post. Defaults to None.

        viewer_has_saved_to_collection (bool, optional): If True, the viewer
            has saved this post to a collection. Defaults to None.

        viewer_in_photo_of_you (bool, optional): If True, the viwer has been
            tagged in this post. Defaults to None.

        viewer_can_reshare (bool, optional): If True, the viewer can share
            this post. Defaults to None.
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
    **kwargs
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
        """Syncs this object instance with Instagram.

        The object instance on which this method is called on will be
        refreshed to match the data available on the instagram website.

        Args:
            context (bool): Set this to True if you wish for the client to 
                log in before scraping data.
        """
        refreshed = self.client.get_post(self.shortcode, context)
        return self._update(refreshed)


    def load_page(self):
        """Loads the page of this object on the webdriver
        """
        self.client._nav_post(self.shortcode)
        return self


    def get_owner(self) -> Optional[Profile]:
        """Shortcut for::
            client.get_profile(owner, context=True)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_profile`.

        Returns:
            Optional[:class:`instagram.Profile`]: If the owner of this post
                is valid, its Profile object will be returned.
        """
        return self.client.get_profile(self.owner)


    def add_comment(self, text) -> Optional[Comment]:
        """Shortcut for::
            client.comment_post(shortcode, text)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.comment_post`.

        Returns:
            Optional[:class:`instagram.Comment`]: If the comment
                is posted correctly, it will be returned.
        """
        result = self.client.comment_post(self.shortcode, text)
        if result:
            self.comments_count += 1
            return self.client._find_comment(self.shortcode, self.client.username, text)
        return None


    def like(self):
        """Shortcut for::
            client.like_post(shortcode)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.like_post`.

        Returns:
            Optional[:class:`instagram.Post`]: If the post is
                liked successfully, the instace this method is
                called on will be refreshed.
        """
        post = self.client.like_post(self.shortcode)
        return self._update(post)


    def unlike(self):
        """Shortcut for::
            client.unlike_post(shortcode)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.inlike_post`.

        Returns:
            Optional[:class:`instagram.Post`]: If the post is
                unliked successfully, the instace this method is
                called on will be refreshed.
        """
        post = self.client.unlike_post(self.shortcode)
        return self._update(post)


    




