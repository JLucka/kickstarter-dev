import webapp2
import json
from backend.projects.Project import Project
from backend.transactions.Transaction import Transaction
from backend.users.User import User


class TransactionHandler(webapp2.RequestHandler):
    def post(self):
        new_transaction = Transaction()
        new_transaction.project = Project.get_by_id(int(str(self.request.get("projectId")))).key
        new_transaction.user = User.query(User.google_id == str(self.request.get("userId"))).get().key
        new_transaction.money = int(self.request.get("money"))
        new_transaction.project.get().money += new_transaction.money
        new_transaction.project.get().put()
        new_transaction.user.get().money -= new_transaction.money
        new_transaction.user.get().put()
        new_transaction.put()
        self.response.status = 201
        obj = new_transaction.to_json_obj()
        self.response.out.write(json.dumps(obj))

app = webapp2.WSGIApplication([
    ('/transaction', TransactionHandler)
])