from backend.projects.Project import check_if_name_is_taken


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
    elif check_if_name_is_taken(new_project.name):
        response.status = 400
        response.write("project name is taken")
        return False
    return True
