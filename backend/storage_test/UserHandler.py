import json

import webapp2

from google.appengine.api import users

from backend.storage_test.User import User


class UserHandler(webapp2.RequestHandler):

    def get(self):
        current_use = users.get_current_user()
        obj = {
            'id': current_use.user_id(),
            'name': current_use.nickname(),
            'email': current_use.email(),
            'money': 0
            }
        return self.response.out.write(json.dumps(obj))


def get_user():
    user = users.get_current_user()
    if user:
        User.query(User.name == user).get()
        response = User.query(User.name == user).get()
        if len(response) < 1:
            new_user = User()
            new_user.name = user.nickname()
            new_user.google_id = user.user_id()
            return new_user.put()
    else:
        return False

app = webapp2.WSGIApplication([
    ('/newusers', UserHandler)
])

