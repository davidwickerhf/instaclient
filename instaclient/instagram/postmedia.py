#!/usr/bin/env python
#
# Unofficial Instagram Python client. Built with the use of the selenium,
# and requests modules.
# Copyright (C) 2015-2021
# David Henry Francis Wicker <wickerdevs@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
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
    **kwargs
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