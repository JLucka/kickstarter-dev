from google.appengine.ext import ndb


class Transaction(ndb.Model):
    project = ndb.KeyProperty(kind='Project')
    user = ndb.KeyProperty(kind='User')
    money = ndb.IntegerProperty(default=0)
    time_stamp = ndb.DateTimeProperty(auto_now_add=True)

    def to_json_obj(self):
        user = self.user.get()
        project = self.project.get()
        obj = {
            'id': int(self.key.id()),
            'project': int(project.key.id()),
            'user': user.google_id,
            'money': self.money,
            'time': str(self.time_stamp.time())
            }
        return obj
