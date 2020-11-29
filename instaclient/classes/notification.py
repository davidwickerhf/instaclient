from instaclient.classes.baseprofile import BaseProfile
from instaclient.classes.instaobject import InstaBaseObject


class Notification(InstaBaseObject):
    def __init__(self, id:str, viewer:int or BaseProfile, from_user:BaseProfile, type:str, timestamp):
        super().__init__(id, viewer, type)
        self.from_user = from_user
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f'Notification<{self.type}, {self.from_user}>'

    def __lt__(self, o) -> bool:
        if self.timestamp < o.timestamp:
            return True
        else:
            return False

    def __gt__(self, o) -> bool:
        if self.timestamp > o.timestamp:
            return True
        else:
            return False

    def get_timestamp(self):
        return self.timestamp
