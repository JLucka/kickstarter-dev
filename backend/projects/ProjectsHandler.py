import json

import MySQLdb
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

        if name != "" and ';' not in name:
            rows = self.project_conn.select_all_where("name = '%s'" % name)
        else:
            rows = self.project_conn.select_all()

        response = []
        for row in rows:
            obj = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'creatorid': row[3],
                'creatorname': self.user_conn.select_where(["name"], "id = %s" % row[3])[0][0],
                'money': row[4],
                'date': str(row[5]).split(" ")[0],
                'time': str(row[5]).split(" ")[1]
            }
            response.append(obj)

        self.response.out.write(json.dumps(response))

    def post(self):
        self.response.status = 400
        if ';' not in (self.request.get("name") and self.request.get("desc") and self.request.get("creatorId")):
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
