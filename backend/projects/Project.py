import urllib

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from google.appengine.api import mail
from protorpc import messages
import datetime

from backend.files.File import File

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
        return "https://kickstarter-dev.appspot.com/project/" + str(self.name)


def send_accepted_emails(project):
        recipient = project.creator.get().name
        if '@' not in recipient:
            recipient += "@gmail.com"
        message = mail.EmailMessage(sender="Ocado Kickstarter <a.sokolowski@ocado.com>",
                            subject="[Ocado Kickstarter] Your project {0} has reached its goal!".format(project.name))
        message.to = "%s <%s>" % (project.creator.get().name, recipient)
        message.body = """
            Dear {0}:
            Your project has reached its goal. Congratulations! You've earned it.
            {1}
            """.format(project.creator.get().name, urllib.quote_plus(project.get_url()))
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


def get_all_projects(*arg):
    projects = Project.query().fetch(arg[0])
    return convert_to_json(projects)


def update_projects_status():
    month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    expired_projects = Project.query().filter(Project.createdOn < month_ago).fetch()
    for project in expired_projects:
        if project.status == Status.ACTIVE:
            project.status = Status.EXPIRED
            project.put()


def get_best_projects(*arg):
    projects = Project.query().order(-Project.money).fetch(arg[0])
    return convert_to_json(projects)


def get_trending_projects(*arg):
    projects = Project.query().filter(Project.money > 30).order(Project.money).order(-Project.createdOn).fetch(arg[0])
    return convert_to_json(projects)


def get_projects_by_status(*arg):
    projects = Project.query(Project.status == Status(arg[1])).fetch(arg[0])
    return convert_to_json(projects)


def get_attachments(project):
    urls = []
    attachments = File.query(File.project == project.key).fetch()
    for attachment in attachments:
        urls.append('https://kickstarter-dev.appspot.com/api/file_download?blob_key=' + str(attachment.blobKey))

    return urls if len(urls) > 0 else ''
