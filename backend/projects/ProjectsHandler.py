import json

import webapp2

from ProjectConnector import ProjectConnector, Project
from backend.projects.ProjectValidator import validate
from backend.users.UsersConnector import UserConnector


class ProjectsHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self.user_conn = UserConnector()
        self.project_conn = ProjectConnector()

    def get(self):
        name = str(self.request.get("name"))

        if name != "" not in name:
            rows = self.project_conn.select_all_where("name = %s", name)
        else:
            rows = self.project_conn.select_all()

        response = []
        for row in rows:
            print row
            obj = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'creatorid': row[3],
                'creatorname': self.user_conn.select_where(["name"], "id = %s" % row[3]),
                'money': row[4],
                'date': str(row[5]).split(' ')[0],
                'time': str(row[5]).split(' ')[1]
            }
            response.append(obj)
        if len(response) == 1:
            self.response.out.write(json.dumps(response[0]))
        else:
            self.response.out.write(json.dumps(response))

    def post(self):
        self.response.status = 400
        new_project = Project(str(self.request.get("name")),
                            str(self.request.get("desc")),
                            str(self.request.get("creatorId")))
        if validate(self.response, new_project):
            if self.project_conn.insert_into(new_project):
                self.response.status = 201
                self.response.write("nice to see your creativity, stay cool")

app = webapp2.WSGIApplication([
    ('/projects', ProjectsHandler)
])
