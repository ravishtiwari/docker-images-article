import pytest
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

from app.services.s3_wrapper import S3Wrapper
from app.services.gcs_wrapper import GCSWrapper


class TestS3Wrapper:

    @patch("app.services.s3_wrapper.boto3.client")
    def test_upload_file_success(self, mock_boto_client):
        """Test successful file upload to S3"""
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client

        wrapper = S3Wrapper()
        wrapper.bucket_name = "test-bucket"

        file_obj = BytesIO(b"test content")
        result = wrapper.upload_file(file_obj, "test-key.jpg", "image/jpeg")

        mock_s3_client.upload_fileobj.assert_called_once()
        assert result is not None
        assert "test-key.jpg" in result

    @patch("app.services.s3_wrapper.boto3.client")
    def test_upload_file_failure(self, mock_boto_client):
        """Test failed file upload to S3"""
        mock_s3_client = Mock()
        mock_s3_client.upload_fileobj.side_effect = Exception("Upload failed")
        mock_boto_client.return_value = mock_s3_client

        wrapper = S3Wrapper()
        wrapper.bucket_name = "test-bucket"

        file_obj = BytesIO(b"test content")
        result = wrapper.upload_file(file_obj, "test-key.jpg")

        assert result is None

    @patch("app.services.s3_wrapper.boto3.client")
    def test_delete_file_success(self, mock_boto_client):
        """Test successful file deletion from S3"""
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client

        wrapper = S3Wrapper()
        wrapper.bucket_name = "test-bucket"

        result = wrapper.delete_file("test-key.jpg")

        mock_s3_client.delete_object.assert_called_once_with(
            Bucket="test-bucket", Key="test-key.jpg"
        )
        assert result is True

    @patch("app.services.s3_wrapper.boto3.client")
    def test_generate_presigned_url(self, mock_boto_client):
        """Test generating presigned URL"""
        mock_s3_client = Mock()
        mock_s3_client.generate_presigned_url.return_value = "https://presigned-url.com"
        mock_boto_client.return_value = mock_s3_client

        wrapper = S3Wrapper()
        wrapper.bucket_name = "test-bucket"

        url = wrapper.generate_presigned_url("test-key.jpg", expiration=3600)

        assert url == "https://presigned-url.com"
        mock_s3_client.generate_presigned_url.assert_called_once()


class TestGCSWrapper:

    @patch("app.services.gcs_wrapper.storage.Client")
    def test_upload_file_success(self, mock_storage_client):
        """Test successful file upload to GCS"""
        mock_client = Mock()
        mock_bucket = Mock()
        mock_blob = Mock()

        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value = mock_client

        wrapper = GCSWrapper()
        wrapper.bucket_name = "test-bucket"
        wrapper.bucket = mock_bucket

        file_obj = BytesIO(b"test content")
        result = wrapper.upload_file(file_obj, "test-key.jpg", "image/jpeg")

        mock_blob.upload_from_file.assert_called_once_with(file_obj)
        assert result is not None
        assert "test-key.jpg" in result

    @patch("app.services.gcs_wrapper.storage.Client")
    def test_upload_file_no_bucket(self, mock_storage_client):
        """Test file upload when bucket is not configured"""
        wrapper = GCSWrapper()
        wrapper.bucket = None

        file_obj = BytesIO(b"test content")
        result = wrapper.upload_file(file_obj, "test-key.jpg")

        assert result is None

    @patch("app.services.gcs_wrapper.storage.Client")
    def test_delete_file_success(self, mock_storage_client):
        """Test successful file deletion from GCS"""
        mock_client = Mock()
        mock_bucket = Mock()
        mock_blob = Mock()

        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value = mock_client

        wrapper = GCSWrapper()
        wrapper.bucket_name = "test-bucket"
        wrapper.bucket = mock_bucket

        result = wrapper.delete_file("test-key.jpg")

        mock_blob.delete.assert_called_once()
        assert result is True

    @patch("app.services.gcs_wrapper.storage.Client")
    def test_make_public(self, mock_storage_client):
        """Test making a file public in GCS"""
        mock_client = Mock()
        mock_bucket = Mock()
        mock_blob = Mock()

        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value = mock_client

        wrapper = GCSWrapper()
        wrapper.bucket_name = "test-bucket"
        wrapper.bucket = mock_bucket

        result = wrapper.make_public("test-key.jpg")

        mock_blob.make_public.assert_called_once()
        assert result is True
