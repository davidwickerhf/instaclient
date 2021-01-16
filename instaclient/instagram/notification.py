from instaclient.instagram.profile import Profile
from instaclient.instagram.instaobject import InstaBaseObject


class Notification(InstaBaseObject):
    def __init__(self, client, id:str, viewer:str, from_user:Profile, type:str, timestamp):
        super().__init__(client, id, type, viewer)
        # Required
        self.from_user = from_user
        self.timestamp = timestamp

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Notification):
            if self.from_user == o.from_user:
                if self.timestamp == o.timestamp:
                    if self.type == o.type:
                        return True
        return False


    def __repr__(self) -> str:
        return f'Notification<{self.type} | {self.from_user}>'


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


    def refresh(self):
        """Syncs this object instance with Instagram.

        The object instance on which this method is called on will be
        refreshed to match the data available on the instagram website.
        """
        notifications = self.client.get_notifications(types=[self.type])
        for noti in notifications:
            if noti == self:
                return self._update(noti)
        return None

    
    