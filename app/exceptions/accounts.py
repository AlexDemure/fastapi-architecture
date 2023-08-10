from app.exceptions.business import BusinessError


class AccountNotFoundError(BusinessError):
    status_code = 404
    description = "Account is not found"
