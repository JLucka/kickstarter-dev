import backend.transactions.Transaction
from backend.projects.Project import Status


def validate(response, new_transaction):
    user = new_transaction.user.get()
    project = new_transaction.project.get()

    if user.google_id == project.creator.get().google_id:
        response.status = 401
        response.write("You can't support your own project!")
        return False
    elif project.status == Status.EXPIRED:
        response.status = 400
        response.write("You can't support expired project")
        return False
    elif new_transaction.money > user.money:
        response.status = 400
        response.write("You dont't have enough money")
        return False
    elif new_transaction.project is None:
        response.status = 400
        response.write("project id can not be empty")
        return False
    elif new_transaction.user is None:
        response.status = 400
        response.write("user id can not be empty")
        return False

    return True

