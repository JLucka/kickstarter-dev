#-*- coding: utf-8 -*-

import json

import webapp2
from backend.projects.Project import Project, get_entities_by_name, update_projects_status, get_best_projects, \
    get_trending_projects
from backend.projects.ProjectValidator import validate
from backend.users.User import User


class ProjectsHandler(webapp2.RequestHandler):
    def get(self):
        update_projects_status()
        if self.request.get("best") != "":
            projects = get_best_projects(int(self.request.get("best")))
        elif self.request.get('trending') != "":
            projects = get_trending_projects(int(self.request.get('trending')))
        else:
            name = unicode(self.request.get("name"))
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
        new_project.name = unicode(self.request.get("name"))
        new_project.description = unicode(self.request.get("desc"))
        new_project.creator = User.query(User.google_id == str(self.request.get("creatorId"))).get().key

        return new_project


app = webapp2.WSGIApplication([('/api/projects', ProjectsHandler)])