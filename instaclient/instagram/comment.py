from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
    from instaclient.client.instaclient import Profile
from instaclient.instagram.instaobject import InstaBaseObject

class Comment(InstaBaseObject):
    """Class reppresenting an Instagram Comment

    The instagram comment class inherits from the `instagram.InstaBaseObjects` class.
    This class should contain all methods related to actions one can execute on 
    comments on Instagram (such as liking, replying, etc).

    Two `instagram.Comment` objects are considered equal if they share the 
    same `id`, `post_shortcde` and `owner`.

    Attributes:
        client (:class:`instaclient.InstaClient`): This is the client instance that 
            will be used to perform actions on the object. Many methods included in 
            this class are in fact shortcuts for the `instaclient.InstaClient` 's methods. 

        id (str): The unique ID of the post, provided and defined by Instagram.

        type (str): Type of Instagram Object. 
            This is set to `InstaBaseObject.GRAPH_COMMENT`.

        viewer (str): The instagram account's username of the account the user is 
            currently logged in with, when loading this object from Instagram.

        owner (str): Username of the owner of this comment

        post_shortcode (str): Unique shortcode of the comment

        text (str): The text of the comment

        created_at (int, optional): timestamp of the creation of the comment.
            Defaults to None.

        likes_count (int, optional): Number of likes on the comment. 
            Defaults to None.

        did_report_as_spam (bool, optional): Context based. If viewer has
            reported the comment as spam. Defaults to None.

        viewer_has_liked (bool, optional): Context based. If viewer has
            liked the comment. Defaults to None.

        parent_comment (Comment, optional): Optional parent comment. 
            Defaults to None.
            
        threaded_comments (List[Comment], optional): Optional list of threaded
            comments. Defaults to None.
    """
    def __init__(self, 
    client: 'InstaClient',
    id: str,
    viewer: str,
    owner:str,
    post_shortcode:str,
    text:str,
    created_at:int=None,
    likes_count:int=None,
    # Optional
    did_report_as_spam:bool=None,
    viewer_has_liked:bool=None,
    parent_comment:'Comment'=None,
    threaded_comments:List['Comment']=None,
    ):
        super().__init__(client, id, type=InstaBaseObject.GRAPH_COMMENT, viewer=viewer)
        # REQUIRED
        self.owner = owner
        self.post_shortcode = post_shortcode
        self.text = text
        self.created_at = created_at
        self.likes_count = likes_count
        # REQUIRE CONTEXT (Log In)
        self.did_report_as_spam = did_report_as_spam
        self.viewer_has_liked = viewer_has_liked
        # Additional
        self.parent_comment = parent_comment
        self.threaded_comments = threaded_comments

    def __repr__(self) -> str:
        return f'Comment<{self.owner}>'


    def __eq__(self, o: object) -> bool:
        if isinstance(o, Comment):
            if self.id == o.id and self.owner == o.owner and self.post_shortcode == o.post_shortcode:
                return True
            return False
        return False


    def get_owner(self, context:bool=True) -> Optional['Profile']:
        """Shortcut for::

            client.get_profile(owner, context)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_profile`.

        Returns:
            Optional[:class:`instagram.Profile`]: If the operation is successful, an instance of a new `Profile` object matching the `owner` attribute of the class.
        """
        return self.client.get_profile(username=self.owner, context=context)

    def get_post(self, context:bool=True):
        """Shortcut for::

            client.get_post(shortcode, context)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_post`.

        Returns:
            Optional[:class:`instagram.Post`]: If the operation is successful, an instance of a new `Post` object matching the `post_shortcode` attribute of the class.
        """
        return self.client.get_post(shortcode=self.post_shortcode, context=context)


        