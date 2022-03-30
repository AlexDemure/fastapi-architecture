from enum import Enum


class BaseMessage(Enum):
    obj_is_created = "Object is created."
    obj_already_exist = "Object already exist."
    obj_is_changed = "Object is changed."
    obj_is_not_found = "Object is not found."
    obj_data = "Object data."
    obj_is_not_created = "Object is not created reason bad request."
    obj_is_deleted = "Object is deleted."
    OK = "OK"
    forbidden = "Forbidden"
