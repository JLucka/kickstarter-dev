import webapp2
from google.appengine.api import users


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.request.get("name")
        return webapp2.redirect(users.create_logout_url("/"))

app = webapp2.WSGIApplication([
    ('/newlogout', LogoutHandler)
])