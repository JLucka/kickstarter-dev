import json

import webapp2
from google.appengine.api import users

from backend.users.User import User


class UserHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if current_user:
            query_user = User.query(User.name == current_user.nickname()).get()
            if query_user:
                response_object = query_user.to_json_obj()
                self.response.out.write(json.dumps(response_object))


def get_user():
    current_user = users.get_current_user()
    if current_user:
        response = User.query(User.name == current_user.nickname()).get()
        if response is None:
            new_user = User()
            new_user.name = current_user.nickname()
            new_user.google_id = current_user.user_id()
            print "new user is created: " + new_user.google_id
            return new_user.put()
    else:
        return False


app = webapp2.WSGIApplication([
    ('/user', UserHandler)
])
