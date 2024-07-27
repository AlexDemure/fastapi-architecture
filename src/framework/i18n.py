from enum import Enum

from fastapi import Header

from src.tools.exceptions import Error


class Locale(str, Enum):
    en = "en"
    ru = "ru"

    @classmethod
    def to_list(cls) -> list[str]:
        return [locale.value for locale in list(Locale)]


def get_locale(locale: Locale = Header(Locale.en)) -> Locale:
    return locale


class I18Error(Error):
    def to_dict(self, locale: Locale = Locale.en) -> dict:
        return dict(
            status_code=self.status_code,
            detail=dict(type=self.__class__.__name__, description=getattr(self, locale.value)),
        )
