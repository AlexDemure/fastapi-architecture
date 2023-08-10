import json


class BusinessError(Exception):
    status_code: int
    description: str

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> dict:
        return dict(
            status_code=self.status_code,
            detail=dict(
                type=self.class_name,
                description=self.description,
            ),
        )

    def __repr__(self) -> str:
        return f"{self.class_name}({self.to_dict()})"

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
