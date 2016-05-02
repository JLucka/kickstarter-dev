#-*- coding: utf-8 -*-

import json

import webapp2
from backend.projects.Project import *
from backend.projects.ProjectValidator import validate
from backend.users.User import User
from collections import defaultdict

DEFAULT_PAGE = 0
DEFAULT_PAGE_SIZE = 24

FUNCTION_MAP = defaultdict(lambda: get_all_projects, {'best': get_best_projects, 'trending': get_trending_projects, 'status': get_projects_by_status})


class ProjectsHandler(webapp2.RequestHandler):
    def get(self):
        update_projects_status()
        status = int(self.request.get("status") or 0)
        projects = FUNCTION_MAP[self.request.get('function')](int(self.request.get('pageSize') or DEFAULT_PAGE_SIZE),
                                                              status)
        self.response.out.write(json.dumps(projects))


    def get_by_name(self, name):
        project = get_project_by_name(name)
        if project:
            self.response.out.write(json.dumps(project))
        else:
            self.response.out.write("Project with name: " + name + " was not found")
            self.response.out.status = 404

    def post(self):
        new_project = self.create_project_from_params()
        validate(self.response, new_project)

        if new_project.put():
            self.response.status = 201
            self.response.out.write(json.dumps(new_project.to_json_object()))
        else:
            self.response.status = 500

    def put(self):
        new_project_body = json.loads(self.request.body)
        project_id = new_project_body['id']
        old_project = Project.get_by_id(project_id)
        if not old_project:
            self.response.out.write("Project with id: " + str(project_id) + " was not found")
            self.response.out.status = 404
            return

        self.update_project(old_project, new_project_body)
        self.response.out.write(old_project)
        self.response.status = 200

    def create_project_from_params(self):
        new_project = Project()
        new_project.name = unicode(self.request.get("name"))
        new_project.description = unicode(self.request.get("desc"))
        new_project.creator = User.query(User.google_id == str(self.request.get("creatorId"))).get().key

        return new_project

    def update_project(self, old_project, new_project_body):
        old_project.name = new_project_body['name']
        old_project.description = new_project_body['desc']
        old_project.put()


app = webapp2.WSGIApplication([
    webapp2.Route('/api/projects', handler=ProjectsHandler),
    webapp2.Route('/api/projects/<name:.+>', handler=ProjectsHandler, handler_method='get_by_name')])