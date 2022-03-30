import re
from enum import Enum


class ErrorEnum(Enum):

    def _prepare_to_snake_case(self) -> str:
        """Convert error to snake_case."""

        class_type, error_type = self.__str__().split('.')

        class_type_items = re.sub(r'(?<!^)(?=[A-Z])', ' ', class_type).split(' ')

        class_type_in_snake_case = "_".join([item.lower() for item in class_type_items if item != 'Errors'])

        return f"{class_type_in_snake_case}.{error_type}"

    @property
    def client_response(self) -> dict:
        """Property for generating a response for HTTP."""

        return dict(msg=self.value, type=self._prepare_to_snake_case())

    @property
    def docs_response(self) -> str:
        """Property for generating a response for Swagger."""

        return f"**{self._prepare_to_snake_case()}** - {self.value}\n\n"


class AuthErrors(ErrorEnum):

    credentials_not_validate = "Could not validate credentials"


class AccessPermissionsErrors(ErrorEnum):

    access_denied = "Access denied"


class AccountErrors(ErrorEnum):

    account_not_found = "Account is not found."
