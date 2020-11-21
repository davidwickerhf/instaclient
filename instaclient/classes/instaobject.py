import abc
from instaclient.classes.baseprofile import BaseProfile

class InstaBaseObject(abc.ABC):
    GRAPH_IMAGE = 'GraphImage'
    GRAPH_VIDEO = 'GraphVideo'
    GRAPH_SIDECAR = 'GraphSidecar'
    GRAPH_PROFILE = 'GRAPH_PROFILE'
    GRAPH_HASHTAG = 'GRAPH_HASHTAG'

    GRAPH_FOLLOW = 'GraphFollowAggregatedStory'
    GRAPH_LIKE = 'GraphLikeAggregatedStory'
    GRAPTH_TAGGED = 'GraphUserTaggedStory'
    GRAPH_MENTION = 'GraphMentionStory'
    GRAPH_COMMENT = 'GraphCommentMediaStory'

    def __init__(self, id:str, viewer:str or BaseProfile, type:str):
        self.id = id
        self.viewer = viewer
        self.type = type

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

