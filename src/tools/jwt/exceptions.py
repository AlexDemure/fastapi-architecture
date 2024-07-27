from src.tools.exceptions import Error


class JWTError(Error):
    status_code = 401
    description = "Unauthorized"
