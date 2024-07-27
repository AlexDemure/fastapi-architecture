from enum import Enum


class Storage(str, Enum):
    channel = "channel"
    bot = "bot"
    account = "account"

    @property
    def dir(self):
        if self is self.channel:
            return "channels"
        elif self is self.bot:
            return "bots"
        elif self is self.account:
            return "accounts"


class Mimetype(str, Enum):
    png = "image/png"
    jpeg = "image/jpeg"
    mp4 = "video/mp4"

    @property
    def format(self):
        if self is self.png:
            return ".png"
        elif self is self.jpeg:
            return ".jpg"
        elif self is self.mp4:
            return ".mp4"
