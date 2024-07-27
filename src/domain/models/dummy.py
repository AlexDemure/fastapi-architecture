from .base import Model


class Dummy(Model):
    id: int

    @classmethod
    def init(cls) -> dict:
        return dict()

    def jwt(self) -> None: ...


class DummyDocument(Model):
    id: str

    @classmethod
    def init(cls) -> dict:
        return dict()
