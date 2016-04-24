import json
import webapp2
from google.appengine.api import users

from backend.projects.Project import Project
from backend.users.User import User


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        current_user = User.query(User.name == users.get_current_user().nickname()).get()
        if users.is_current_user_admin() or current_user.admin:
            current_user.make_admin()
            self.response.status = 200
            users_query = User.query().fetch()
            users_json = []
            for user in users_query:
                users_json.append(user.to_json_obj())
            self.response.out.write(json.dumps(users_json))
        else:
            self.response.status = 401

    def post(self):
        current_user = User.query(User.name == users.get_current_user().nickname()).get()
        if users.is_current_user_admin() or current_user.admin:
            current_user.make_admin()
            function = self.request.get("function")
            if function == "hide":
                project = Project.get_by_id(int(str(self.request.get("projectId"))))
                project.hide()
            else:
                user = User.query(User.google_id == str(self.request.get("userId"))).get()
                amount = int(self.request.get("amount"))
                if function == "substract":
                    user.substract_money(amount)
                    self.response.out.write(user.to_json_obj())
                elif function == 'add':
                    user.add_money(amount)
                    self.response.out.write(user.to_json_obj())
                elif function == 'set':
                    user.set_money(amount)
                    self.response.out.write(user.to_json_obj())
                else:
                    self.response.status = 400
        else:
            self.response.status = 401


app = webapp2.WSGIApplication([('/admin', AdminHandler)])