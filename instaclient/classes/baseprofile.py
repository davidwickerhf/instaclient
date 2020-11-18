from instaclient.classes.instaobject import InstaBaseObject

class BaseProfile(InstaBaseObject):
    def __init__(self, id:str, viewer:str, username:str, name:str):
        id = id.replace('profilePage_', '')
        
        super().__init__(id=id, viewer=viewer)
        self.username = username
        self.name = name.split('\\')[0]

    def __repr__(self) -> str:
        return f'BaseProfile<{self.username}>'

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name