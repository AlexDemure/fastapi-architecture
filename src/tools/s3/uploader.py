from contextlib import asynccontextmanager

import aioboto3
import aiofiles

from .enums import Mimetype
from .enums import Storage


class S3:
    bucket: str = None
    endpoint_url: str = None
    aws_access_key_id: str = None
    aws_secret_access_key: str = None

    def __init__(self, bucket: str, endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str) -> None:
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    @asynccontextmanager
    async def client(self):
        async with aioboto3.Session().client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as _client:
            yield _client

    def file_uri(self, filename: str, mimetype: Mimetype, storage: Storage) -> str:
        return f"{self.endpoint_url}/{self.bucket}/{self.file_path(filename, mimetype, storage)}"

    @classmethod
    def file_path(cls, filename: str, mimetype: Mimetype, storage: Storage) -> str:
        return f"{storage.dir}/{cls.file_name(filename, mimetype)}"

    @classmethod
    def file_name(cls, filename: str, mimetype: Mimetype) -> str:
        return f"{filename}{mimetype.format}"

    async def upload(self, file: bytes, filename: str, mimetype: Mimetype, storage: Storage) -> None:
        async with aiofiles.tempfile.NamedTemporaryFile("wb", suffix=mimetype.format) as tmp:
            await tmp.write(file)
            async with self.client() as client:
                await client.upload_file(
                    Filename=tmp.name,
                    Bucket=self.bucket,
                    Key=self.file_path(filename=filename, mimetype=mimetype, storage=storage),
                )

    async def download(self, filename: str, mimetype: Mimetype, storage: Storage) -> bytes:
        async with aiofiles.tempfile.NamedTemporaryFile() as tmp:
            async with self.client() as client:
                await client.download_file(
                    Filename=tmp.name,
                    Bucket=self.bucket,
                    Key=self.file_path(filename=filename, mimetype=mimetype, storage=storage),
                )
                await tmp.seek(0)
                file = await tmp.read()
        return file

    async def delete(self, filename: str, mimetype: Mimetype, storage: Storage) -> None:
        async with self.client() as client:
            await client.delete_object(
                Bucket=self.bucket,
                Key=self.file_path(filename=filename, mimetype=mimetype, storage=storage),
            )
