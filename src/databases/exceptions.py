from src.tools.exceptions import Error


class ObjectNotFoundError(Error):
    status_code = 404
    description = "Object is not found. Something went wrong"
