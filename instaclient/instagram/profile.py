from typing import Optional, TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
    from instaclient.instagram import Post
from instaclient.instagram.instaobject import InstaBaseObject

class Profile(InstaBaseObject):
    def __init__(self, 
    client:'InstaClient',
    id:str, 
    viewer:str, 
    username:str,
    name:Optional[str]=None,
    biography:Optional[str]=None,
    is_private:Optional[bool]=None,
    is_verified:Optional[bool]=None,
    is_business_account:Optional[bool]=None,
    is_joined_recently:Optional[bool]=None,
    follower_count:Optional[int]=None,
    followed_count:Optional[int]=None,
    post_count:Optional[int]=None,
    business_category_name:Optional[str]=None,
    overall_category_name:Optional[str]=None,
    external_url:Optional[str]=None,
    fb_id:Optional[str]=None,

    business_email:Optional[str]=None,
    blocked_by_viewer:Optional[bool]=None,
    restricted_by_viewer:Optional[bool]=None,
    has_blocked_viewer:Optional[bool]=None,
    has_requested_viewer:Optional[bool]=None,
    mutual_followed:Optional[bool]=None,
    requested_by_viewer:Optional[bool]=None,
    ):
        super().__init__(client, id, self.GRAPH_PROFILE, viewer)
        # Required
        self.username = username
        # Optional
        self.name = name
        self.biography = biography
        self.is_private = is_private
        self.is_verified = is_verified
        self.is_business_account = is_business_account
        self.is_joined_recently = is_joined_recently
        self.follower_count = follower_count
        self.followed_count = followed_count
        self.post_count = post_count
        self.business_category_name = business_category_name
        self.overall_category_name = overall_category_name
        self.external_url = external_url
        self.fb_id = fb_id

        self.business_email = business_email
        self.blocked_by_viewer = blocked_by_viewer
        self.restricted_by_viewer = restricted_by_viewer
        self.has_blocked_viewer = has_blocked_viewer
        self.has_requested_viewer = has_requested_viewer
        self.mutual_followed = mutual_followed
        self.requested_by_viewer = requested_by_viewer
        

    def __repr__(self) -> str:
        return f'Profile<{self.username}>'


    def __eq__(self, o: object) -> bool:
        if isinstance(o, Profile):
            if o.id == self.id or o.username == self.username:
                return True
        return False


    @staticmethod
    def from_username(client:'InstaClient', username:str, context:bool=True) -> Optional['Profile']:
        return client._scrape_profile(username, context=context)


    def refresh(self, context:bool=True):
        refreshed = self.client._scrape_profile(self.username, context)
        return self._update(refreshed)

    
    def get_posts(self, count:Optional[int], deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List['Post'], List[str]]]:
        return self.client._scrape_user_posts(self.username, count, deep_scrape, callback_frequency, callback, **callback_args)

    
    def get_followers(self, count: int, deep_scrape:Optional[bool]=False, callback_frequency: int=100, callback=None, **callback_args) -> Optional[Union[List['Profile'], List[str]]]:
        return self.client._scrape_followers(user=self.username, count=count, deep_scrape=deep_scrape, check_user=False, callback_frequency=callback_frequency, callback=callback, **callback_args)
        

    def get_username(self):
        return self.username


    def get_name(self):
        return self.name


    def follow(self):
        self.client._follow_user(user=self.username)

    
    def unfollow(self):
        self.client._unfollow_user(user=self.username)