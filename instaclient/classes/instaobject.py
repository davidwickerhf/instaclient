import abc

class InstaBaseObject(abc.ABC):
    GRAPH_IMAGE = 'GraphImage'
    GRAPH_VIDEO = 'GraphVideo'
    GRAPH_SIDECAR = 'GraphSidecar'

    GRAPH_FOLLOW = 'GraphFollowAggregatedStory'
    GRAPH_LIKE = 'GraphLikeAggregatedStory'
    GRAPTH_TAGGED = 'GraphUserTaggedStory'
    GRAPH_MENTION = 'GraphMentionStory'
    GRAPH_COMMENT = 'GraphCommentMediaStory'

    def __init__(self, id:str, viewer:str):
        self.id = id
        self.viewer = viewer

    def get_id(self):
        return self.id

    def get_viewer(self):
        return self.viewer
