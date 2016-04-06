import json

import webapp2

from google.appengine.api import users

from backend.storage_test.User import User


class UserHandler(webapp2.RequestHandler):

    def get(self):
        current_user_name = users.get_current_user()
        row = User.query(User.name == current_user_name).get()
        obj = {
            'id': row[0][0],
            'name': row[0][1],
            'money': row[0][2]
            }
        return self.response.out.write(json.dumps(obj))


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.request.get("name")
        return webapp2.redirect(users.create_logout_url("/"))


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
    ('/newusers', UserHandler),
    ('/newlogout', LogoutHandler)
])

