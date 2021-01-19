import abc, json
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient

class InstaBaseObject(abc.ABC):
    GRAPH_IMAGE = 'GraphImage'
    GRAPH_VIDEO = 'GraphVideo'
    GRAPH_SIDECAR = 'GraphSidecar'
    GRAPH_PROFILE = 'GraphProfile'
    GRAPH_HASHTAG = 'GraphHashtag'
    GRAPH_LOCATION = 'GraphLocation'

    GRAPH_FOLLOW = 'GraphFollowAggregatedStory'
    GRAPH_LIKE = 'GraphLikeAggregatedStory'
    GRAPTH_TAGGED = 'GraphUserTaggedStory'
    GRAPH_MENTION = 'GraphMentionStory'
    GRAPH_COMMENT = 'GraphCommentMediaStory'

    def __init__(self, client:'InstaClient', id:str, type:str, viewer:str=None, **kwargs):
        """Base class for most Instagram objects

        The base condition for two InstaBaseObjects to be equal is if they share
        the same ID. This condition may be overriden by classes which inherit from
        this base class.

        Args:
            client (:class:`instaclient.InstaClient`): This is the client instance that 
                will be used to perform actions on the object. Many methods included in 
                this class are in fact shortcuts for the `instaclient.InstaClient` 's methods. 

            id (str): Unique ID of the object, provided by instagram.

            type (str): Object type. Can be:
                `InstaBaseObject.GRAPH_IMAGE`,  `InstaBaseObject.GRAPH_VIDEO`,
                `InstaBaseObject.GRAPH_SIDECAR`, `InstaBaseObject.GRAPH_PROFILE`,
                `InstaBaseObject.GRAPH_HASHTAG`, `InstaBaseObject.GRAPH_LOCATION`,
                `InstaBaseObject.GRAPH_FOLLOW`, `InstaBaseObject.GRAPH_LIKE`,
                `InstaBaseObject.GRAPH_TAGGED`, `InstaBaseObject.GRAPH_MENTION`, 
                `InstaBaseObject.GRAPH_COMMENT` 

            viewer (str, optional): Username of the viewer account. Defaults to None.
        """
        # Required
        self.client = client
        self.id = id
        self.type = type
        self.viewer = viewer
        

    def __repr__(self) -> str:
        return f'InstaBaseObject<{self.id}>'


    def __getitem__(self, item: str):
        return self.__dict__[item]


    def __eq__(self, o: object) -> bool:
        if isinstance(o, InstaBaseObject):
            if o.get_id() == self.id:
                return True
            else:
                return False
        else:
            return 
            
    
    def _update(self, o: object) -> object:
        """Updates the current object instance with the values
        of another object of the same class.

        Args:
            o (object): Instagram object.
                Note:
                    The provided object must be of the same class
                    ass the object upon which this method is called.

        Returns:
            object: Updated instance of the current object.
        """
        client = self.client
        if isinstance(o, self.__class__):
            args = o.to_dict()
            for attr in vars(self):
                setattr(self, attr, args.get(attr))
            self.client = client
            return self
        return None


    @classmethod
    def de_json(cls, data: dict, client: 'InstaClient') -> Optional['InstaBaseObject']:
        """Turns a valid json or dict reppresentation of the object
        into an instance of the object.

        Args:
            data (dict): Dict reppresentation of the object
            client (:class:`instaclient.InstaClient`): client object
                that will be attached to this instagram object.

        Returns:
            Optional[:class:`instagram.InstaBaseObject`]: Instagram object
        """
        if not data:
            return None
        return cls(client=client, **data)  # type: ignore[call-arg]


    def to_json(self) -> str:
        """
        Returns:
            str: Json string reppresentation of the object. Any 'client' attribute will be ignored.
        """
        return json.dumps(self.to_dict())


    def to_dict(self) -> dict:
        """
        Returns:
            dict: Dict reppresentation of the object. Any 'client' attribute will be ignored.
        """
        data = dict()

        for key in iter(self.__dict__):
            if key == 'client' or key.startswith('_'):
                continue

            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value
        return data


    @property
    def viewer_profile(self):
        """
        Returns:
            Optional[:class:`instagram.Profile`]: Profile object of the 
                `viewer` of the current instagram object.
        """
        return self.client.get_profile(self.viewer)
        

    def get_id(self):
        return self.id


    def get_viewer(self):
        return self.viewer


    def get_type(self):
        return self.type

