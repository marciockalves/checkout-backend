import os
from botocore.client import Config
import boto3

class StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            endpoint_url=os.getenv("S3_ENDPOINT"), # Onde o Python "bate"
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'
        )
        self.bucket = os.getenv("S3_BUCKET_NAME")
        self.public_url = os.getenv("S3_PUBLIC_URL")

    async def upload_image(self, file):
        filename = file.filename
        
        self.s3.upload_fileobj(
            file.file,
            self.bucket,
            filename,
            ExtraArgs={'ContentType': file.content_type}
        )
        
        return f"{self.public_url}/{self.bucket}/{filename}"