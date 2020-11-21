from instaclient.classes.baseprofile import BaseProfile
from instaclient.classes.instaobject import InstaBaseObject


class Notification(InstaBaseObject):
    def __init__(self, id:str, viewer:int or BaseProfile, from_user:BaseProfile, type:str, timestamp):
        super().__init__(id, viewer, type)
        self.from_user = from_user
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f'Notification<{self.type}, {self.from_user}>'

    def get_timestamp(self):
        return self.timestamp
