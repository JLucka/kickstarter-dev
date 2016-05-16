#-*- coding: utf-8 -*-

import json

import webapp2
from backend.projects.Project import *
from backend.projects.ProjectValidator import validate
from backend.users.User import User
from backend.files.File import attach_to_project, clear_files
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
        project_id = int(self.request.get('id'))
        if project_id:
            project = Project.get_by_id(project_id)
            self.update_from_params(project)
        else:
            project = self.create_project_from_params()
        validate(self.response, project)

        if project.put():
            if self.request.get("files"):
                clear_files(project)
                files = json.loads(str(self.request.get('files')))
                attach_to_project(files, project.key)
            self.response.status = 201
            self.response.out.write(json.dumps(project.to_json_object()))
        else:
            self.response.status = 500

    def create_project_from_params(self):
        new_project = Project()
        new_project.name = unicode(self.request.get("name"))
        new_project.description = unicode(self.request.get("desc"))
        new_project.creator = User.query(User.google_id == str(self.request.get("creatorId"))).get().key

        return new_project

    def update_from_params(self, project):
        project.name = unicode(self.request.get("name"))
        project.description = unicode(self.request.get("desc"))


app = webapp2.WSGIApplication([
    webapp2.Route('/api/projects', handler=ProjectsHandler),
    webapp2.Route('/api/projects/<name:.+>', handler=ProjectsHandler, handler_method='get_by_name')])