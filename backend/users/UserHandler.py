import json
from google.appengine.api import users
import webapp2
from UsersConnector import UserConnector


class UserHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.user_conn = UserConnector()

    def get(self):
        current_user = users.get_current_user()
        row = self.user_conn.select_all_where("name = '%s'" % current_user)
        print row
        response = []
        obj = {
            'name': row[0][1],
            'money': row[0][2]
            }
        response.append(obj)
        return self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
    ('/user', UserHandler)
])
