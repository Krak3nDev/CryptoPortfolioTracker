import io
import logging

import uuid6
from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError, EndpointConnectionError
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

from cryptoapp.application.interfaces.storage import StorageService
from cryptoapp.application.portfolio.create import BUCKET
from cryptoapp.main.config import S3MinioConfig

logger = logging.getLogger(__name__)


def resize_image_to_150x150(data: bytes) -> io.BytesIO:
    with io.BytesIO(data) as byte_file:
        image = Image.open(byte_file)
        image.thumbnail((150, 150), Image.Resampling.BICUBIC)
        output = io.BytesIO()
        image.save(output, format="WEBP", quality=85)
        output.seek(0)
        return output


class S3Minio(StorageService):
    def __init__(self, minio_config: S3MinioConfig, client: AioBaseClient):
        self._s3_client = client
        self._bucket = BUCKET
        self._minio_config = minio_config

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30)
    )
    async def upload_from_bytes(self, data: bytes, file_name: str) -> str:
        unique_file_name = f"{file_name}_{uuid6.uuid7().hex}.webp"

        processed_image = resize_image_to_150x150(data)

        try:
            await self._s3_client.upload_fileobj(
                processed_image, self._bucket, unique_file_name
            )
            return f"s3://{self._bucket}/{unique_file_name}"
        except EndpointConnectionError as e:
            logger.error(f"Could not connect to MinIO endpoint: {e}")
            raise e
        except ClientError as e:
            logger.error(f"S3 ClientError: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise e

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30)
    )
    async def get_presigned_url(self, s3_url: str, expires_in: int = 3600) -> str:
        if not s3_url.startswith("s3://"):
            raise ValueError(f"Invalid s3_url format: {s3_url}")

        path_part = s3_url.replace("s3://", "")

        try:
            bucket_name, object_key = path_part.split("/", 1)
        except ValueError:
            raise ValueError(f"Invalid s3_url format (missing '/'): {s3_url}")

        try:
            presigned_url: str = await self._s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": bucket_name,
                    "Key": object_key,
                },
                ExpiresIn=expires_in,
            )
            return presigned_url

        except EndpointConnectionError as e:
            logger.error(f"Could not connect to MinIO endpoint: {e}")
            raise e
        except ClientError as e:
            logger.error(f"S3 ClientError: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise e
