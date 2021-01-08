from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
    from instaclient.client.instaclient import Profile
from instaclient.instagram.instaobject import InstaBaseObject

class Comment(InstaBaseObject):
    def __init__(self, 
    client: 'InstaClient',
    id: str,
    type: str,
    viewer: str,
    owner:str,
    post_shortcode:str,
    text:str,
    created_at:Optional[int]=None,
    likes_count:Optional[int]=None,
    # Optional
    did_report_as_spam:Optional[bool]=None,
    viewer_has_liked:Optional[bool]=None,
    parent_comment:Optional['Comment']=None,
    threaded_comments:Optional[List['Comment']]=None,
    ):
        super().__init__(client, id, type, viewer=viewer)
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

    def get_owner(self, context:bool=True) -> Optional['Profile']:
        return self.client.get_profile(username=self.owner, context=context)

    def get_post(self, context:bool=True):
       return self.client.get_post(shortcode=self.post_shortcode, context=context)


        