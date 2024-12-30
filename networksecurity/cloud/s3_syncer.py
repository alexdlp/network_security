import os
import re

class S3Sync:
    def _validate_bucket_name(self, bucket_url: str) -> str:
        """
        Validate and ensure the bucket name follows AWS S3 naming conventions.
        If the bucket name does not start with "s3://", it will be added.
        """

        # Remove "s3://" for validation purposes
        normalized_name = bucket_url.replace("s3://", "")

        bucket_name = normalized_name.split("/")[0]  # Obtener solo el nombre del bucket

        # Validate the bucket name (without the prefix)
        pattern = r"^[a-zA-Z0-9.\-_]{3,63}$"
        if not re.match(pattern, bucket_name):
            raise ValueError(f"Invalid bucket name: {bucket_name}")

        # Add "s3://" if not already present
        if not bucket_url.startswith("s3://"):
            bucket_url = f"s3://{bucket_url}"

        return bucket_url

    def sync_folder_to_s3(self, folder: str, bucket_name: str):
        """
        Sync a local folder to an S3 bucket.
        """
        bucket_name = self._validate_bucket_name(bucket_name)

        if not os.path.isdir(folder):
            raise ValueError(f"Local folder does not exist: {folder}")

        # Sync local folder to S3 bucket
        command = f'aws s3 sync "{folder}" "{bucket_name}/"'
        result = os.system(command)
        if result != 0:
            raise RuntimeError(f"Command failed: {command}")

    def sync_folder_from_s3(self, folder: str, bucket_name: str):
        """
        Sync an S3 bucket to a local folder.
        """
        bucket_name = self._validate_bucket_name(bucket_name)

        if not os.path.isdir(folder):
            raise ValueError(f"Local folder does not exist: {folder}")

        # Sync S3 bucket to local folder
        command = f'aws s3 sync "{bucket_name}/" "{folder}"'
        result = os.system(command)
        if result != 0:
            raise RuntimeError(f"Command failed: {command}")