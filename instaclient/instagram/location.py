from typing import List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
    from instaclient.instagram.post import Post
from instaclient.instagram.instaobject import InstaBaseObject
from instaclient.instagram.address import Address

class Location(InstaBaseObject):
    """Class reppresenting an Instagram profile.

    The instagram profile class inherits from the `instagram.InstaBaseObjects` class.
    This class should contain all methods related to actions that can be executed 
    on the profile page of a user on the Instagram website.

    Two `instagram.Location` objects are considered equal if they share the 
    same `id` or the same `slug`.

    Attributes:
        client (:class:`instaclient.InstaClient`): This is the client instance that 
            will be used to perform actions on the object. Many methods included in 
            this class are in fact shortcuts for the `instaclient.InstaClient` 's methods. 

        id (str): The unique ID of the location, provided and defined by Instagram.

        viewer (str): The instagram account's username of the account the user is 
            currently logged in with, when loading this object from Instagram.

        name (str): Name of the location on Instagram.

        slug (str): Unique instagram location identifier

        has_public_page (bool): True if the location info is accessible by everyone
            on Instagram. Defaults to None.

        lat (int): Latitude of the location

        lng (int): Longitude of the location

        posts_count (int): Number of instagram posts that present this location.

        blurb (str): Location blurb. Defaults to None.

        website (str): Optional website link attached to the Location page.
            Defaults to None.

        primary_alias_on_fb (str): If this location has an alias on Facebook, it
            will be saved in this attribute.

        phone (str): Optional phone number attached to the Location.

        address (:class:`instaclient.Address`): Address of the Location.
    """
    def __init__(self, 
    # Required
    client: 'InstaClient',
    id: str, 
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
    **kwargs
    ):
        super().__init__(client, id, InstaBaseObject.GRAPH_LOCATION, viewer=viewer)
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


    def refresh(self):
        """Syncs this object instance with Instagram.

        The object instance on which this method is called on will be
        refreshed to match the data available on the instagram website.
        """
        refreshed = self.client.get_location(self.id, self.slug)
        return self._update(refreshed)

    
    def get_posts(self, count:Optional[int]=None, deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List['Post'], List[str]]]:
        """Shortcut for::
            client.get_location_posts(username, count, deep_scrape, callback_frequency, callback, **callback_args)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_location_posts`.

        Returns:
            Optional[Union[List[`instagram.Post`], List[str]]]: If the `deep_scrape` attribute is set to true,
            this method will return a list of `instagram.Post` objects. Else, a list of post shortcodes 
            will be returned instead.
        """
        if not count:
            count = self.posts_count
        return self.client.get_location_posts(self.id, self.slug, count, deep_scrape, callback_frequency, callback, **callback_args)
        