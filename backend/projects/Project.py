from google.appengine.ext import ndb


class Project(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    money = ndb.IntegerProperty(default=0)
    createdOn = ndb.DateTimeProperty(auto_now_add=True)
    creator = ndb.KeyProperty(kind='User')

    def to_json_object(self):
        user = self.creator.get()
        obj = {
            'id': int(self.key.id()),
            'name': self.name,
            'description': self.description,
            'creatoryid': user.google_id,
            'creatorname': user.name,
            'money': self.money,
            'date': str(self.createdOn.date()),
            'time': str(self.createdOn.time())
        }
        return obj

    def save_entity(self):
        self.put()


def get_entities_by_name(name):
    if name != "":
        project = Project.query(Project.name == name).get()
        return project.to_json_object()

    else:
        projects = Project.query().fetch(25)
        projects_jsons = []
        for project in projects:
            obj = project.to_json_object()
            projects_jsons.append(obj)
        return projects_jsons
