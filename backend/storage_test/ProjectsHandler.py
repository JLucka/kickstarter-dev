import json
import webapp2
from backend.storage_test.Project import Project


class ProjectsHandler(webapp2.RequestHandler):
    def get(self):
        name = str(self.request.get("name"))
        if name != "":
            project = Project.query(Project.name == name).get()
            obj = project.to_json_object()
            self.response.out.write(json.dumps(obj))
        else:
            projects = Project.query().fetch(25)
            response = []
            for project in projects:
                obj = project.to_json_object()
                response.append(obj)
            self.response.out.write(json.dumps(response))

    def post(self):
        self.response.status = 400
        new_project = Project()
        new_project.name = str(self.request.get("name"))
        new_project.description = str(self.request.get("desc"))
        new_project.creator = str(self.request.get("creatorId"))
        if new_project.put():
            self.response.status = 201
            self.response.write(new_project)


app = webapp2.WSGIApplication([('/newprojects', ProjectsHandler)])