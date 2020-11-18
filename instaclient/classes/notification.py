from instaclient.classes.baseprofile import BaseProfile
from instaclient.classes.instaobject import InstaBaseObject


from instaclient.classes.instaobject import InstaBaseObject


class Notification(InstaBaseObject):
    def __init__(self, id:str, viewer:str, user:BaseProfile, type, timestamp):
        super().__init__(id, viewer)
        self.user = user
        self.type = type
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f'Notification<{self.type}, {self.user}>'

    def get_user(self):
        return self.user

    def get_type(self):
        return self.type

    def get_timestamp(self):
        return self.timestamp
