import json

import webapp2
from google.appengine.api import users

from backend.users.User import User


class UserHandler(webapp2.RequestHandler):
    def get(self):
        user = get_user()
        if user:
            self.response.status = 200
            response_object = user.to_json_obj()
            self.response.out.write(json.dumps(response_object))
        else:
            self.response.status = 400


def get_user():
    current_user = users.get_current_user()
    if current_user:
        query_user = User.query(User.name == current_user.nickname()).get()
        if query_user is None:
            return create_user(current_user)
        else:
            return query_user
    else:
        return False


def create_user(current_user):
    new_user = User()
    new_user.name = current_user.nickname()
    new_user.google_id = current_user.user_id()
    new_user.admin = users.is_current_user_admin()
    if new_user.put():
        return new_user
    else:
        return False

app = webapp2.WSGIApplication([
    ('/user', UserHandler)
])
