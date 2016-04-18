
def validate(response, new_project):
    if new_project.name == "":
        response.status = 400
        response.write("name can not be empty")
        return False
    elif new_project.description == "":
        response.status = 400
        response.write("description can not be empty")
        return False
    elif new_project.creator is None:
        response.status = 400
        response.write("creator can not be empty")
        return False
    return True
