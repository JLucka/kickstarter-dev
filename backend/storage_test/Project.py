from google.appengine.ext import ndb


class Project(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    money = ndb.IntegerProperty(default=0)
    createdOn = ndb.DateTimeProperty(auto_now_add=True)
    creator = ndb.KeyProperty(kind='User')

    def to_json_object(self):
        print "beg"
        print self.creator
        print "end"
        obj = {
                'id': int(self.key.id()),
                'name': self.name,
                'description': self.description,
                'creatoryid': self.creator.google_id,
                'creatorname': self.creator.name,
                'money': self.money,
                'date': str(self.createdOn.date()),
                'time': str(self.createdOn.time())
            }
        return obj
