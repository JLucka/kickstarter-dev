#-*- coding: utf-8 -*-

import json

import webapp2
from backend.projects.Project import Project, get_entities_by_name, update_projects_status, get_best_projects, \
    get_trending_projects, get_projects_by_status
from backend.projects.ProjectValidator import validate
from backend.users.User import User

DEFAULT_PAGE = 0
DEFAULT_PAGE_SIZE = 24


class ProjectsHandler(webapp2.RequestHandler):
    def get(self):
        update_projects_status()
        status = self.request.get("status")
        if status:
            projects = get_projects_by_status(int(status))
        elif self.request.get("best") != "":
            projects = get_best_projects(int(self.request.get("best")))
        elif self.request.get('trending') != "":
            projects = get_trending_projects(int(self.request.get('trending')))
        else:
            name = unicode(self.request.get("name"))
            projects = self.with_paging(get_entities_by_name(name))
        self.response.out.write(json.dumps(projects))

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

    def with_paging(self, projects):
        request_page = self.request.get('page')
        request_page_size = self.request.get('pageSize')

        page = int(request_page if request_page else DEFAULT_PAGE)
        page_size = int(request_page_size if request_page_size else DEFAULT_PAGE_SIZE)

        return projects[page * page_size:(page + 1) * page_size] if (page + 1) * page_size <= len(projects) else projects[page * page_size:]


app = webapp2.WSGIApplication([('/api/projects', ProjectsHandler)])