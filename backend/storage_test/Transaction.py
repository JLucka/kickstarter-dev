from google.appengine.ext import ndb
import datetime


class Transaction(ndb.Model):
    project_id = ndb.IntegerProperty(default=0)
    user_id = ndb.IntegerProperty(default=0)
    money = ndb.IntegerProperty(default=0)
    ndb.DateProperty(default= datetime.datetime.now().isoformat(' '))
    time = datetime.datetime.now().isoformat(' ')

    def to_json_obj(self):
        obj = {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'money': self.money,
            'time': self.time
            }
        return obj
