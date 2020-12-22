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
    has_public_page:bool,
    slug:str,
    # Optional
    lat:Optional[int]=None,
    lng:Optional[int]=None,
    posts_count:Optional[int]=None,
    blurb:Optional[str]=None,
    website:Optional[str]=None,
    primary_alias_on_fb:Optional[str]=None,
    phone:Optional[str]=None,
    address:Optional[Address]=None,
    ):
        super().__init__(client, id, type, viewer=viewer)
        self.name = name
        self.posts_count = posts_count
        self.has_public_page = has_public_page
        self.latitude = lat
        self.longitude = lng
        self.slug = slug
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
        