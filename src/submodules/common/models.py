from typing import TypeVar

from tortoise import models

ModelType = TypeVar("ModelType", bound=models.Model)
