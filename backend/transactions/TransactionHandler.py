import webapp2
import json
from backend.projects.Project import Project
from backend.transactions.Transaction import Transaction
from backend.transactions.TransactionValidator import validate
from backend.users.User import User


class TransactionHandler(webapp2.RequestHandler):
    def post(self):
        new_transaction = self.create_transaction_from_params()
        if validate(self.response, new_transaction):
            transfer_money(new_transaction)
            new_transaction.project.get().check_if_accepted()
            if new_transaction.put():
                self.response.status = 201
                obj = new_transaction.to_json_obj()
                self.response.out.write(json.dumps(obj))
            else:
                self.response.status = 400

    def create_transaction_from_params(self):
        new_transaction = Transaction()
        new_transaction.project = Project.get_by_id(int(str(self.request.get("projectId")))).key
        new_transaction.user = User.query(User.google_id == str(self.request.get("userId"))).get().key
        new_transaction.money = int(self.request.get("money"))

        return new_transaction


def transfer_money(transaction):
    transaction.project.get().money += transaction.money
    transaction.project.get().put()
    transaction.user.get().money -= transaction.money
    transaction.user.get().put()



app = webapp2.WSGIApplication([
    ('/transaction', TransactionHandler)
])