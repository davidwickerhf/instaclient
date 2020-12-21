from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.instagram.instaobject import InstaBaseObject

class Comment(InstaBaseObject):
    def __init__(self, client: 'InstaClient', id: str, type: str, viewer: str):
        super().__init__(client, id, type, viewer=viewer)