"""This module contains an object that reppresents an Instagram Profile."""
from typing import Optional, TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
    from instaclient.instagram import Post
from instaclient.instagram.instaobject import InstaBaseObject

class Profile(InstaBaseObject):
    """Class reppresenting an Instagram profile.

    The instagram profile class inherits from the `instagram.InstaBaseObjects` class.
    This class should contain all methods related to actions that can be executed 
    on the profile page of a user on the Instagram website.

    Two `instagram.Profile` objects are considered equal if they share the 
    same ID or the same instagram username.

    Attributes:
        client (:class:`instaclient.InstaClient`): This is the client instance that 
            will be used to perform actions on the object. Many methods included in 
            this class are in fact shortcuts for the `instaclient.InstaClient` 's methods. 

        id (str): The unique ID of the profile, provided and defined by Instagram.

        viewer (str): The instagram account's username of the account the user is 
            currently logged in with, when loading this object from Instagram.

        username (str): The instagram profile's unique username.
            Note:
                Instagram usernames are mutable, so don't rely on them too much for 
                persistence. The instagram ID won't change when a user changes the 
                account's username.

        name (str, optional): The instagram profile's name, seen at the top of the 
            profile page, under the profile picture and over the bio. Defaults to None.
            Note: 
                Special characters, such as emojis, might be saved in unicode notation.

        biography (str, optional): The profile's bio. Also in this case, special 
            characters might be translated into unicode. Defaults to None.

        is_private (bool, optional): Variable retreived from Instagram. 
            Is `True` if the profile is private. Defaults to None.

        is_verified (bool, optional): Variable retreived from Instagram. 
            Is `True` if the profile is verified by instagram. Defaults to None.

        is_business_account (bool, optional): Variable retreived from Instagram. 
            Is `True` if the profile is a business account. Defaults to None.

        is_joined_recently (bool, optional): Variable retreived from Instagram. 
            Is `True` if the profile has been created recently. Defaults to None.

        follower_count (int, optional): The number of followers the profile has. 
            Defaults to None.

        followed_count (int, optional): The number of accounts a profile follows. 
            Defaults to None.

        post_count (int, optional): The number of posts on the profile. Defaults to None.

        business_category_name (str, optional): If the profile is a business account,
            the business category's name is saved in this attribute. Defaults to None.

        overall_category_name (str, optional): If the user has defined a category 
            for the profile, the value of such category will be saved in this attribute. 
            Defaults to None.

        external_url (str, optional): Optional URL that the user might have placed 
            under the bio. Defaults to None.

        fb_id (str, optional): Optional ID of the connected Facebook Page
            This attribute is valid only if the user has connected the account 
            to FB. Defaults to None.

        profile_pic_url (str, optional): Optional url of the profile picture.

        business_email (str, optional): If the profile is a business account
            and if the email is set to be public, it will be saved in this attribute. 
            Defaults to None.

        blocked_by_viewer (bool, optional): Is true if the `viewer` is currently 
            blocked by this profile. Defaults to None.

        restricted_by_viewer (bool, optional): Is true if the `viewer` has restricted 
            this profile. Defaults to None.

        has_blocked_viewer (bool, optional): Is true if the `viewer` has blocked this 
            profile. Defaults to None.

        has_requested_viewer (bool, optional): Is true if the `viewer` was  sent a 
            follow request by this profile. Defaults to None.

        mutual_followed (bool, optional): Is true if the `viewer` is followed by 
            this profile and viceversa. Defaults to None.

        requested_by_viewer (bool, optional): Is try if the `viewer` has sent a 
            follow request to this profile. Defaults to None.

        Note:
            The attributes `blocked_by_viewer`, `restricted_by_viewer`, `has_blocked_viewer`, 
            `has_requested_viewer`, `mutual_followed` and `requested_by_viewer` all depend 
            on the `viewer` attribute.

            If this instagram object is loaded when the client is not signed in, these values 
            will be either set to None or False.
    """
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
    fb_id:str=None,
    profile_pic_url:str=None,

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
        self.fb_id = fb_id
        self.profile_pic_url = profile_pic_url

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


    def refresh(self, context:bool=True):
        """Syncs this object instance with Instagram.

        The object instance on which this method is called on will be
        refreshed to match the data available on the instagram website.

        Args:
            context (bool): Set this to True if you wish for the client to 
                log in before scraping data.
        """
        refreshed = self.client.get_profile(self.username, context)
        return self._update(refreshed)

    
    def get_posts(self, count:Optional[int], deep_scrape:Optional[bool]=False, callback_frequency:int=100, callback=None, **callback_args) -> Optional[Union[List['Post'], List[str]]]:
        """Shortcut for::
            client.get_user_posts(username, count, deep_scrape, callback_frequency, callback, **callback_args)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_user_posts`.

        Returns:
            Optional[Union[List[`instagram.Post`], List[str]]]: If the `deep_scrape` attribute is set to true,
            this method will return a list of `instagram.Post` objects. Else, a list of post shortcodes 
            will be returned instead.
        """
        return self.client.get_user_posts(self.username, count, deep_scrape, callback_frequency, callback, **callback_args)

    
    def get_followers(self, count: int=None, use_api:bool=True, deep_scrape:Optional[bool]=False, callback_frequency: int=100, callback=None, **callback_args) -> Optional[Union[List['Profile'], List[str]]]:
        """Shortcut for::
            client.get_followers(username, count, use_api, deep_scrape, callback_frequency, callback, **callback_args)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_followers`.

        Returns:
            Optional[Union[List[`instagram.Profile`], List[str]]]: If the `deep_scrape` attribute is set to true,
            this method will return a list of `instagram.Profile` objects. Else, a list of profile usernames 
            will be returned instead.
        """
        if not count:
            count = self.follower_count
        return self.client.get_followers(user=self.username, count=count, use_api=use_api, deep_scrape=deep_scrape, callback_frequency=callback_frequency, callback=callback, **callback_args)

    
    def get_following(self, count: int=None, use_api:bool=True, deep_scrape:Optional[bool]=False, callback_frequency: int=100, callback=None, **callback_args) -> Optional[Union[List['Profile'], List[str]]]:
        """Shortcut for::
            client.get_followers(username, count, use_api, deep_scrape, callback_frequency, callback, **callback_args)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.get_following`.

        Returns:
            Optional[Union[List[`instagram.Profile`], List[str]]]: If the `deep_scrape` attribute is set to true,
            this method will return a list of `instagram.Profile` objects. Else, a list of profile usernames 
            will be returned instead.
        """
        if not count:
            count = self.followed_count
        return self.client.get_following(user=self.username, count=count, use_api=use_api,  deep_scrape=deep_scrape, callback_frequency=callback_frequency, callback=callback, **callback_args)


    def follow(self):
        """Shortcut for::
            client.follow_user(username)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.follow_user`.
        """
        self.client.follow_user(user=self.username)

    
    def unfollow(self):
        """Shortcut for::
            client.unfollow_user(username)

        for the full documentation of this method, please see
        :meth:`instaclient.InstaClient.unfollow_user`.
        """
        self.client.unfollow_user(user=self.username)