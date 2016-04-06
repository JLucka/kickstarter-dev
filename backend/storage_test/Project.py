from google.appengine.ext import ndb


class Project(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    money = ndb.IntegerProperty(default=0)
    createdOn = ndb.DateTimeProperty(auto_now_add=True)
    # user = ndb.KeyProperty(kind='User')

    def to_json_object(self):
        obj = {
                'id': int(self.key.id()),
                'name': self.name,
                'description': self.description,
                'creatorid': 1,
                'creatorname': 'Test',
                'money': self.money,
                'date': str(self.createdOn.date()),
                'time': str(self.createdOn.time())
            }
        return obj
