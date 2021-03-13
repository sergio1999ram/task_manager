from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json['_id']
        return str(object_id)
