from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.instagram.instaobject import InstaBaseObject
from instaclient.instagram.address import Address

class Location(InstaBaseObject):
    def __init__(self, 
    # Required
    client: 'InstaClient',
    id: str, 
    type: str, 
    viewer: str,
    name:str,
    slug:str,
    # Optional
    has_public_page:bool=None,
    lat:int=None,
    lng:int=None,
    posts_count:int=None,
    blurb:str=None,
    website:str=None,
    primary_alias_on_fb:str=None,
    phone:str=None,
    address:Address=None,
    ):
        super().__init__(client, id, type, viewer=viewer)
        self.name = name
        self.slug = slug
        # Optional
        self.has_public_page = has_public_page
        self.latitude = lat
        self.longitude = lng
        self.posts_count = posts_count
        self.blurb = blurb
        self.website = website
        self.primary_alias_on_fb = primary_alias_on_fb
        self.phone = phone
        self.address = address

    def __repr__(self) -> str:
        return f'Location<{self.slug}>'

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Location):
            if o.id == self.id or o.slug == self.slug:
                return True
        return False
        