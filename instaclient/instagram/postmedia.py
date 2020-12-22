from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
from instaclient.instagram.instaobject import InstaBaseObject

class PostMedia(InstaBaseObject):
    def __init__(self, 
    client:'InstaClient',
    id:int,
    type:str,
    viewer:str,
    shortcode:str,
    src_url:str,
    is_video:bool,
    accessibility_caption:Optional[str]=None,
    tagged_users:Optional[List[str]]=None,
    # If Media is Video
    has_audio:Optional[bool]=None,
    video_duration:Optional[float]=None,
    video_view_count:Optional[int]=None,

    ) -> None:
        super().__init__(client, id, type, viewer)
        self.shortcode = shortcode
        self.src_url = src_url
        self.is_video = is_video
        self.accessibility_caption = accessibility_caption
        self.tagged_users = tagged_users
        # IF Media is Video
        self.has_audio = has_audio
        self.video_duration = video_duration
        self.video_view_count = video_view_count

    def __repr__(self) -> str:
        return f'PostMedia<{self.shortcode}>'

    def __eq__(self, o: object) -> bool:
        if isinstance(o, PostMedia):
            if o.shortcode == self.shortcode:
                return True
        return False