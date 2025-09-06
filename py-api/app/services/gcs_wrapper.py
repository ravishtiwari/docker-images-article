from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from typing import Optional, BinaryIO, List
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)


class GCSWrapper:
    def __init__(self):
        self.client = storage.Client(project=settings.gcp_project_id)
        self.bucket_name = settings.gcs_bucket_name
        self.bucket = self.client.bucket(self.bucket_name) if self.bucket_name else None

    def upload_file(
        self, file_obj: BinaryIO, object_key: str, content_type: Optional[str] = None
    ) -> Optional[str]:
        """Upload a file to GCS and return the URL"""
        try:
            if not self.bucket:
                logger.error("GCS bucket not configured")
                return None

            blob = self.bucket.blob(object_key)

            if content_type:
                blob.content_type = content_type

            blob.upload_from_file(file_obj)

            # Generate public URL
            url = f"https://storage.googleapis.com/{self.bucket_name}/{object_key}"
            logger.info(f"File uploaded to GCS: {url}")
            return url

        except GoogleCloudError as e:
            logger.error(f"Error uploading to GCS: {e}")
            return None

    def download_file(self, object_key: str, file_path: str) -> bool:
        """Download a file from GCS"""
        try:
            if not self.bucket:
                logger.error("GCS bucket not configured")
                return False

            blob = self.bucket.blob(object_key)
            blob.download_to_filename(file_path)
            logger.info(f"File downloaded from GCS: {object_key}")
            return True
        except GoogleCloudError as e:
            logger.error(f"Error downloading from GCS: {e}")
            return False

    def delete_file(self, object_key: str) -> bool:
        """Delete a file from GCS"""
        try:
            if not self.bucket:
                logger.error("GCS bucket not configured")
                return False

            blob = self.bucket.blob(object_key)
            blob.delete()
            logger.info(f"File deleted from GCS: {object_key}")
            return True
        except GoogleCloudError as e:
            logger.error(f"Error deleting from GCS: {e}")
            return False

    def generate_signed_url(
        self, object_key: str, expiration: int = 3600, method: str = "GET"
    ) -> Optional[str]:
        """Generate a signed URL for GCS object"""
        try:
            if not self.bucket:
                logger.error("GCS bucket not configured")
                return None

            blob = self.bucket.blob(object_key)
            url = blob.generate_signed_url(expiration=expiration, method=method)
            return url
        except GoogleCloudError as e:
            logger.error(f"Error generating signed URL: {e}")
            return None

    def list_files(self, prefix: str = "") -> List[str]:
        """List files in GCS bucket with optional prefix"""
        try:
            if not self.bucket:
                logger.error("GCS bucket not configured")
                return []

            blobs = self.bucket.list_blobs(prefix=prefix)
            files = [blob.name for blob in blobs]
            return files
        except GoogleCloudError as e:
            logger.error(f"Error listing GCS files: {e}")
            return []

    def make_public(self, object_key: str) -> bool:
        """Make a GCS object publicly readable"""
        try:
            if not self.bucket:
                logger.error("GCS bucket not configured")
                return False

            blob = self.bucket.blob(object_key)
            blob.make_public()
            logger.info(f"File made public in GCS: {object_key}")
            return True
        except GoogleCloudError as e:
            logger.error(f"Error making file public in GCS: {e}")
            return False


gcs_wrapper = GCSWrapper()
