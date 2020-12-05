import requests, logging
from instaclient.errors.common import InvalidInstaRequestError, InvalidInstaSchemaError
from instaclient.client.urls import GraphUrls
from instaclient.classes.instaobject import InstaBaseObject

logger = logging.getLogger(__name__)

class BaseProfile(InstaBaseObject):
    def __init__(self, id:str, viewer:str, username:str, name:str):
        id = id.replace('profilePage_', '')
        
        super().__init__(id=id, viewer=viewer, type=self.GRAPH_PROFILE)
        self.username = username
        self.name = name.split('\\')[0]

    def __repr__(self) -> str:
        return f'BaseProfile<{self.username}>'

    def from_username(username:str):
        request = GraphUrls.GRAPH_USER.format(username)
        result = requests.get(request)
        try:
            data = result.json()
            try:
                user = data['graphql']['user']
                profile = BaseProfile(
                    id=user['id'],
                    viewer=None,
                    username=user['username'],
                    name=user['full_name']
                )
                return profile
            except:
                raise InvalidInstaSchemaError(__name__)
        except:
            logger.error(f'Invalid request. Data: {result.raw}')
            raise InvalidInstaRequestError(request)

    
    def username_profile(username:str):
        return BaseProfile(
            id=None,
            viewer=None,
            username=username,
            name=None
        )
        

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name