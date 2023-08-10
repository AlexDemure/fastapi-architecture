from enum import Enum


class Permission(str, Enum):
    customer = "customer"
    admin = "admin"
