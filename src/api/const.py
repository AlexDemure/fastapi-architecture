from fastapi import status

from src.enums.errors import AccessPermissionsErrors, AuthErrors
from src.schemas.base import MessageErrorSchema

USER_BASE_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": MessageErrorSchema,
        'description': AuthErrors.credentials_not_validate.docs_response
    },
    status.HTTP_403_FORBIDDEN: {
        "model": MessageErrorSchema,
        'description': AccessPermissionsErrors.access_denied.docs_response
    },
}
