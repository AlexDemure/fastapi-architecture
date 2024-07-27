from typing import Optional


class Error(Exception):
    status_code: int = 418
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return dict(
            status_code=self.status_code,
            detail=dict(type=self.__class__.__name__, description=self.description),
        )
