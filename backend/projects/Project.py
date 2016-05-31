import urllib

import operator
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from google.appengine.api import mail
from protorpc import messages
import datetime

from backend.files.File import File
from backend.transactions.Transaction import Transaction

GOAL_OVC = 100


class Status(messages.Enum):
    ACTIVE = 0
    ACCEPTED = 1
    EXPIRED = 2
    HIDDEN = 3


class Project(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    money = ndb.IntegerProperty(default=0)
    createdOn = ndb.DateTimeProperty(auto_now_add=True)
    creator = ndb.KeyProperty(kind='User')
    status = msgprop.EnumProperty(Status, default=Status.ACTIVE, indexed=True)

    def to_json_object(self):
        user = self.creator.get()
        obj = {
            'id': int(self.key.id()),
            'name': self.name,
            'description': self.description,
            'creatoryid': user.google_id,
            'creatorname': user.name,
            'money': self.money,
            'status': int(self.status),
            'date': str(self.createdOn.date()),
            'time': str(self.createdOn.strftime('%H:%M:%S')),
            'attachments': str(get_attachments(self))
        }
        return obj

    def check_if_accepted(self):
        if self.money >= GOAL_OVC:
            self.status = Status.ACCEPTED
            self.put()
            send_accepted_emails(self)

    def hide(self):
        self.status = Status.HIDDEN
        self.put()

    def get_url(self):
        return "https://kickstarter-dev.appspot.com/project/" + urllib.quote(str(self.name))


def send_accepted_emails(project):
    recipient = project.creator.get().name
    if '@' not in recipient:
        recipient += "@gmail.com"
    message = mail.EmailMessage(sender="Ocado Kickstarter <a.sokolowski@ocado.com>",
                                subject="[Ocado Kickstarter] Your project {0} has reached its goal!".format(
                                    project.name))
    message.to = "%s <%s>" % (project.creator.get().name, recipient)
    message.body = """
            Dear {0}:
            Your project has reached its goal. Congratulations! You've earned it.
            {1}
            """.format(project.creator.get().name, project.get_url())
    message.send()


def convert_to_json(projects):
    projects_jsons = []
    for project in projects:
        obj = project.to_json_object()
        projects_jsons.append(obj)
    return projects_jsons


def get_project_by_name(name):
    project = Project.query(Project.name == name).get()
    if project:
        return project.to_json_object()


def get_all_projects(query_params):
    projects = get_with_pagination(Project.query(), query_params.page, query_params.page_size)
    return convert_to_json(projects)


def update_projects_status():
    month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    expired_projects = Project.query().filter(Project.createdOn < month_ago).fetch()
    for project in expired_projects:
        if project.status == Status.ACTIVE:
            project.status = Status.EXPIRED
            project.put()


def get_best_projects(query_params):
    project_query = Project.query().order(-Project.money)
    projects = get_with_pagination(project_query, query_params.page, query_params.page_size)
    return convert_to_json(projects)


def get_trending_projects(query_params):
    timestamp = datetime.datetime.now() - datetime.timedelta(weeks=1)
    transactions_from_last_week = Transaction.query(Transaction.time_stamp > timestamp).fetch()

    projects = {}
    for t in transactions_from_last_week:
        projects[t.project] = 0

    for t in transactions_from_last_week:
        projects[t.project] += t.money

    timestamp = datetime.datetime.now() - datetime.timedelta(weeks=4)
    pk = dict(sorted(projects.iteritems(), key=operator.itemgetter(1), reverse=True)[:query_params.page_size]).keys()
    return convert_to_json(Project.query(Project.key.IN(pk) and Project.createdOn > timestamp).fetch())


def get_searched_projects(query_params):
    return convert_to_json(Project.query(query_params.phrase.IN([Project.name, Project.description])).fetch())


def get_projects_by_status(query_params):
    project_query = Project.query(Project.status == Status(query_params.status))
    projects = get_with_pagination(project_query, query_params.page, query_params.page_size)
    return convert_to_json(projects)


def get_with_pagination(query, page, page_size):
    return query.fetch_page(page_size, offset=page * page_size)[0]


def get_attachments(project):
    urls = []
    attachments = File.query(File.project == project.key).fetch()
    for attachment in attachments:
        urls.append('https://kickstarter-dev.appspot.com/api/file_download?blob_key=' + str(attachment.blobKey))

    return urls if len(urls) > 0 else ''
