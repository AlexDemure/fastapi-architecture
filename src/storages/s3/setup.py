from src.framework import settings
from src.tools.s3 import S3

s3 = S3(
    bucket=settings.S3_BUCKET,
    endpoint_url=settings.S3_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_SECRET_KEY,
)
