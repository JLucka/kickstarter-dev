from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    money = ndb.IntegerProperty(default=15)
    google_id = ndb.StringProperty()

    def to_json_obj(self):
        obj = {
            'name': self.name,
            'money': self.money,
            'google_id': self.google_id
            }
        return obj
