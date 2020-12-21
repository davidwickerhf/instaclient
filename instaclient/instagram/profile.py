from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.instagram.instaobject import InstaBaseObject

class Profile(InstaBaseObject):
    def __init__(self, 
    client:'InstaClient',
    id:str, 
    viewer:str, 
    username:str,
    name:str=None,
    biography:str=None,
    is_private:bool=None,
    is_verified:bool=None,
    is_business_account:bool=None,
    is_joined_recently:bool=None,
    follower_count:int=None,
    followed_count:int=None,
    post_count:int=None,
    business_category_name:str=None,
    overall_category_name:str=None,
    external_url:str=None,
    business_email:str=None,
    blocked_by_viewer:bool=None,
    restricted_by_viewer:bool=None,
    has_blocked_viewer:bool=None,
    has_requested_viewer:bool=None,
    mutual_followed:bool=None,
    requested_by_viewer:bool=None,
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
        self.business_email = business_email

        self.blocked_by_viewer = blocked_by_viewer
        self.restricted_by_viewer = restricted_by_viewer
        self.has_blocked_viewer = has_blocked_viewer
        self.has_requested_viewer = has_requested_viewer
        self.mutual_followed = mutual_followed
        self.requested_by_viewer = requested_by_viewer
        

    def __str__(self) -> str:
        return f'Profile<{self.username}>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Profile):
            return False
        try:
            self_id = self.get_id()
            o_id = o.get_id()
            return self_id == o_id
        except:
            return self.username == o.username


    @classmethod
    def de_json(cls, data: str, client: 'InstaClient'):
        if not data:
            return None
        return cls(client=client, **data)  # type: ignore[call-arg]


    @staticmethod
    def from_username(username:str, client:'InstaClient', context:bool=True):
        return client._scrape_profile(username, login=context)


    @property
    def viewer_profile(self):
        return self.client._scrape_profile(self.viewer)
        

    def get_username(self):
        return self.username


    def get_name(self):
        return self.name