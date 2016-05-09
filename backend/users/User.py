from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    money = ndb.IntegerProperty(default=15)
    google_id = ndb.StringProperty()
    admin = ndb.BooleanProperty(default=False)

    def to_json_obj(self):
        obj = {
            'name': self.name,
            'money': self.money,
            'google_id': self.google_id,
            'admin': self.admin
            }
        return obj

    def substract_money(self, amount):
        self.money -= amount
        self.put()

    def add_money(self, amount):
        self.money += amount
        self.put()

    def set_money(self, amount):
        self.money = amount
        self.put()

    def make_admin(self):
        self.admin = True
        self.put()

    def remove_admin(self):
        self.admin = False
        self.put()

    @staticmethod
    def get_all_as_json():
        users_query = User.query().fetch()
        users_json = []
        for user in users_query:
            users_json.append(user.to_json_obj())
        return users_json
