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

FUNCTION_MAP = defaultdict(lambda: get_all_projects, {'best': get_best_projects, 'trending': get_trending_projects,
                                                      'status': get_projects_by_status, 'search': get_searched_projects,
                                                      'search': search_for_projects})


class ProjectsHandler(webapp2.RequestHandler):
    def get(self):
        update_projects_status()
        params = QueryParams(self.request)
        projects = FUNCTION_MAP[params.function](params)
        self.response.out.write(json.dumps(projects))

    def get_by_name(self, name):
        project = get_project_by_name(name)
        if project:
            self.response.out.write(json.dumps(project))
        else:
            self.response.out.write("Project with name: " + name + " was not found")
            self.response.out.status = 404

    def post(self):
        params = QueryParams(self.request)
        if params.id != "":
            project = Project.get_by_id(int(params.id))
            update_from_params(project, params)
        else:
            project = create_project_from_params(params)
        validate(self.response, project)

        if project.put():
            if params.files:
                clear_files(project.key)
                files = json.loads(str(params.files))
                attach_to_project(files, project.key)
            self.response.status = 201
            self.response.out.write(json.dumps(project.to_json_object()))
        else:
            self.response.status = 500


def create_project_from_params(params):
    new_project = Project()
    new_project.name = unicode(params.name)
    new_project.description = unicode(params.description)
    new_project.creator = User.query(User.google_id == str(params.creator_id)).get().key

    return new_project


def update_from_params(project, params):
    project.name = unicode(params.name)
    project.description = unicode(params.description)


class QueryParams:
    def __init__(self, request):
        self.id = request.get("id")
        self.name = request.get("name")
        self.description = request.get("desc")
        self.creator_id = request.get("creatorId")
        self.files = request.get("files")
        self.name = request.get("name")
        self.status = int(request.get("status") or 0)
        self.page = int(request.get("page") or 0)
        self.page_size = int(request.get("pageSize") or DEFAULT_PAGE_SIZE)
        self.phrase = str(request.get("phrase"))
        self.function = request.get("function")

app = webapp2.WSGIApplication([
    webapp2.Route('/api/projects', handler=ProjectsHandler),
    webapp2.Route('/api/projects/<name:.+>', handler=ProjectsHandler, handler_method='get_by_name')])
