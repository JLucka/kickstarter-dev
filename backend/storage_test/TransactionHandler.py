import webapp2

from backend.storage_test.Transaction import Transaction
from backend.transactions.TransactionValidator import validate


class TransactionHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)

    def post(self):
        new_transaction = Transaction()
        new_transaction.project_id = self.request.get("projectId")
        new_transaction.user_id = self.request.get("userId")
        new_transaction.money = self.request.get("money")

        if validate(self.response, new_transaction):
            if self.transaction_conn.support_project(new_transaction.user_id, new_transaction.project_id, new_transaction.money):
                self.response.status = 201
            else:
                self.response.status = 400

app = webapp2.WSGIApplication([
    ('/newtransaction', TransactionHandler)
])