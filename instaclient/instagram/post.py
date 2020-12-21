from instaclient.errors.common import InvalidInstaRequestError, InvalidInstaSchemaError
from instaclient.client.constants import GraphUrls
# Objects
from instaclient.instagram.instaobject import InstaBaseObject
from instaclient.instagram.profile import Profile
from instaclient import LOGGER
# Others
import requests
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient


class Post(InstaBaseObject):
    def __init__(self, 
    # Required
    id:str, 
    type:str,
    client:'InstaClient',
    # Optional
    viewer:Profile=None, 
    text:str=None,
    shortcode:str=None,
    ):
        id = id
        type = self.index_type(type)
        
        super().__init__(id=id, type=type, viewer=viewer, client=client)
        self.text = text
        self.shortcode = shortcode

    def __repr__(self) -> str:
        return f'BasePost<{self.shortcode}>'

    def get_owner(self):
        """
        get_owner get information about the owner of the post in the form of a `instaclient.classes.baseprofile.BaseProfile` object

        Raises:
            InvalidInstaRequestError: raised if there is an error in the instagram request URL. Notify package developers.
            InvalidInstaSchemaError: raised if there is an error in the instagram result query shema. Notify package developers.

        Returns:
            BaseProfile: User account of the owner of the post
        """

        # Send Request
        request = self._get_url(GraphUrls.GRAPH_POST.format(self.shortcode))
        if self.proxy:
            proxyDict = { 
              "http"  : self.proxy, 
              "https" : self.proxy, 
              "ftp"   : self.proxy
            }
            result = requests.get(request, proxies=proxyDict)
        else:
            result = requests.get(request) #TODO

        try:
            data = result.json()
        except:
            LOGGER.debug('No result')
            raise InvalidInstaRequestError(request)

        # Process Result Json
        try:
            owner = data['graphql']['shortcode_media']['owner']
            owner:Profile = Profile(
                id=owner['id'],
                viewer=self.viewer,
                username=owner['username'],
                name=owner['full_name']
            )
        except:
            raise InvalidInstaSchemaError(__name__)

        # Return Object
        return owner





