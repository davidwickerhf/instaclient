import abc
from instaclient.utilities import get_url

class InstaBaseObject(abc.ABC):
    GRAPH_IMAGE = 'GraphImage'
    GRAPH_VIDEO = 'GraphVideo'
    GRAPH_SIDECAR = 'GraphSidecar'
    GRAPH_PROFILE = 'GraphProfile'
    GRAPH_HASHTAG = 'GraphHashtag'

    GRAPH_FOLLOW = 'GraphFollowAggregatedStory'
    GRAPH_LIKE = 'GraphLikeAggregatedStory'
    GRAPTH_TAGGED = 'GraphUserTaggedStory'
    GRAPH_MENTION = 'GraphMentionStory'
    GRAPH_COMMENT = 'GraphCommentMediaStory'

    def __init__(self, id:str, viewer:str, type:str, proxy:str=None, scraperapi_key:str=None):
        """
        Reppresents an abstract instagram object.

        Args:
            id (str): The ID of the object. Such ID is provided by Instagram.
            viewer (BaseProfile or str): Reppresents the user account that is viewing this content. Can be either a str (username) or a `BaseProfile` object.
            type (str): Instagram object type. Can be `GRAPTH_IMAGE`, `GRAPH_VIDEO`, `GRAPH_SIDECAR`,  `GRAPH_PROFILE`, `GRAPH_HASHTAG`
            proxy (str, optional): Proxy IP address (which must include the PORT). Defaults to None.
            scraperapi_key (str, optional): scraperapi API Key. Defaults to None.
        """
        self.id = id
        self.viewer = viewer
        self.type = type
        self.proxy=proxy
        self.scraperapi_key=scraperapi_key

    def __eq__(self, o: object) -> bool:
        if isinstance(o, InstaBaseObject):
            if o.get_id() == self.id:
                return True
            else:
                return False
        else:
            return False

    def get_id(self):
        return self.id

    def get_viewer(self):
        return self.viewer

    def get_type(self):
        return self.type

    def _get_url(self, url):
        return get_url(url, self.scraperapi_key)

