class CRUDError(Exception):
    pass


class ObjectNotFoundError(CRUDError):
    pass
