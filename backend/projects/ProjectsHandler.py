import json

import webapp2
import Project
from backend.projects.Project import Project, get_entities_by_name
from backend.projects.ProjectValidator import validate
from backend.users.User import User


class ProjectsHandler(webapp2.RequestHandler):
    def get(self):
        name = str(self.request.get("name"))
        projects = get_entities_by_name(name)
        self.response.out.write(json.dumps(projects))

    def post(self):
        new_project = self.create_project_from_params()
        validate(self.response, new_project)

        if new_project.put():
            self.response.status = 201
            self.response.out.write(json.dumps(new_project.to_json_object()))
        else:
            self.response.status = 500

    def create_project_from_params(self):
        new_project = Project()
        new_project.name = str(self.request.get("name"))
        new_project.description = str(self.request.get("desc"))
        new_project.creator = User.query(User.google_id == str(self.request.get("creatorId"))).get().key

        return new_project




app = webapp2.WSGIApplication([('/projects', ProjectsHandler)])