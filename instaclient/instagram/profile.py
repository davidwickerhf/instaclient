from typing import Optional
from instaclient.client.instaclient import InstaClient
import requests, logging
from instaclient.errors.common import InvalidInstaRequestError, InvalidInstaSchemaError
from instaclient.client.constants import GraphUrls
from instaclient.instagram.instaobject import InstaBaseObject
from instaclient.utilities import get_url

logger = logging.getLogger(__name__)

class Profile(InstaBaseObject):
    def __init__(self, 
    username:str,
    id:str, 
    viewer:str=None, 
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
    
        super().__init__(id=id, type=self.GRAPH_PROFILE, viewer=viewer, )
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
        

    def __repr__(self) -> str:
        return f'BaseProfile<{self.username}>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Profile):
            return False
        try:
            self_id = self.get_id()
            o_id = o.get_id()
            return self_id == o_id
        except:
            return self.username == o.username

    @property
    def viewer(self) -> Optional['Profile']:
        if self.viewer:
            return self.client.get_user(self.viewer)
        return self.viewer

    @classmethod
    def de_json(cls, data: str, client: 'InstaClient'):

        if not data:
            return None
        return cls(client=client, **data)  # type: ignore[call-arg]

    def from_username(username:str, proxy:str=None, scraperapi_key:str=None):
        url = GraphUrls.GRAPH_USER.format(username)
        request = get_url(url, scraperapi_key)
        if proxy:
            proxyDict = { 
              "http"  : proxy, 
              "https" : proxy, 
              "ftp"   : proxy
            }
            result = requests.get(request, proxies=proxyDict)
        else:
            result = requests.get(request)
            
        try:
            print(result)
            print(result.text)
            data = result.json()
            try:
                user = data['graphql']['user']
                profile = Profile(
                    id=user['id'],
                    viewer=None,
                    username=user['username'],
                    name=user['full_name'],
                    biography = user['biography'],
                    is_private = user['is_private'],
                    is_verified = user['is_verified'],
                    is_business_account = user['is_business_account'],
                    is_joined_recently = user['is_joined_recently'],
                    follower_count = user['edge_followed_by']['count'],
                    followed_count = user['edge_follow']['count'],
                    post_count = user['edge_owner_to_timeline_media']['count'],
                    business_category_name = user['business_category_name'],
                    overall_category_name = user['overall_category_name'],
                    external_url = user['external_url'],
                    business_email = user['business_email'],
                    
                    blocked_by_viewer = user['blocked_by_viewer'],
                    restricted_by_viewer = user['restricted_by_viewer'],
                    has_blocked_viewer = user['has_blocked_viewer'],
                    has_requested_viewer = user['has_requested_viewer'],
                    mutual_followed = user['edge_mutual_followed_by']['count'],
                    requested_by_viewer = user['requested_by_viewer']
                )
                return profile
            except Exception as error:
                logging.error(f'Invalid Schema')
                raise InvalidInstaSchemaError(__name__)
        except:
            logger.error(f'Invalid request. Data: {result.raw}')
            raise InvalidInstaRequestError(request)

    
    def username_profile(username:str):
        return Profile(
            id=None,
            viewer=None,
            username=username,
            name=None
        )
        

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name