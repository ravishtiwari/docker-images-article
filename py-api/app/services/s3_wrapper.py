import boto3
from botocore.exceptions import ClientError
from typing import Optional, BinaryIO
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)


class S3Wrapper:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        self.bucket_name = settings.s3_bucket_name

    def upload_file(
        self, file_obj: BinaryIO, object_key: str, content_type: Optional[str] = None
    ) -> Optional[str]:
        """Upload a file to S3 and return the URL"""
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type

            self.s3_client.upload_fileobj(
                file_obj, self.bucket_name, object_key, ExtraArgs=extra_args
            )

            # Generate URL
            url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{object_key}"
            logger.info(f"File uploaded to S3: {url}")
            return url

        except ClientError as e:
            logger.error(f"Error uploading to S3: {e}")
            return None

    def download_file(self, object_key: str, file_path: str) -> bool:
        """Download a file from S3"""
        try:
            self.s3_client.download_file(self.bucket_name, object_key, file_path)
            logger.info(f"File downloaded from S3: {object_key}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading from S3: {e}")
            return False

    def delete_file(self, object_key: str) -> bool:
        """Delete a file from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            logger.info(f"File deleted from S3: {object_key}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting from S3: {e}")
            return False

    def generate_presigned_url(
        self, object_key: str, expiration: int = 3600, method: str = "get_object"
    ) -> Optional[str]:
        """Generate a presigned URL for S3 object"""
        try:
            url = self.s3_client.generate_presigned_url(
                method,
                Params={"Bucket": self.bucket_name, "Key": object_key},
                ExpiresIn=expiration,
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    def list_files(self, prefix: str = "") -> List[str]:
        """List files in S3 bucket with optional prefix"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix
            )

            files = []
            if "Contents" in response:
                files = [obj["Key"] for obj in response["Contents"]]

            return files
        except ClientError as e:
            logger.error(f"Error listing S3 files: {e}")
            return []


s3_wrapper = S3Wrapper()
