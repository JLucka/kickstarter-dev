import webapp2

from backend.users.UserHandler import get_user


class MainPage(webapp2.RequestHandler):
    def get(self):
        get_user()
        with open('frontend/index.html', 'r') as myfile:
            data = myfile.read()

        self.response.write(data)

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
