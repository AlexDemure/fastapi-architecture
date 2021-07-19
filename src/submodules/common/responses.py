from fastapi import status

from .enums import BaseMessage

base_responses = {
    status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value}
}
