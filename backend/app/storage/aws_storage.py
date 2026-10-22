"""
AWS Storage Adapter for InsightPulse AI

This module provides AWS cloud storage integration using:
- Amazon S3 for file storage
- Amazon DynamoDB for structured data
- AWS Lambda for serverless processing
- Amazon CloudWatch for logging

Note: This is a stub implementation. Full AWS integration requires:
1. Valid AWS credentials configured in environment variables
2. AWS resources provisioned (S3 bucket, DynamoDB table, Lambda function)
3. Proper IAM permissions

Set STORAGE_MODE=aws in .env to enable this adapter.
"""

import boto3
from botocore.exceptions import ClientError
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class AWSStorageAdapter:
    """AWS-based storage adapter for cloud deployment"""
    
    def __init__(self):
        if not settings.aws_access_key_id or not settings.aws_secret_access_key:
            raise ValueError("AWS credentials not configured. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in environment variables.")
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        
        self.dynamodb_client = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        
        self.lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        
        self.cloudwatch_client = boto3.client(
            'logs',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        
        self.s3_bucket = settings.aws_s3_bucket
        self.dynamodb_table = settings.aws_dynamodb_table
        self.lambda_function = settings.aws_lambda_function
        
        logger.info("AWS Storage Adapter initialized")
    
    def log_to_cloudwatch(self, message: str, level: str = 'INFO'):
        """Log message to CloudWatch Logs"""
        try:
            log_group_name = '/insightpulse/processing'
            log_stream_name = datetime.utcnow().strftime('%Y/%m/%d')
            
            # Ensure log group and stream exist
            try:
                self.cloudwatch_client.create_log_group(logGroupName=log_group_name)
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    raise
            
            try:
                self.cloudwatch_client.create_log_stream(
                    logGroupName=log_group_name,
                    logStreamName=log_stream_name
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    raise
            
            # Put log event
            self.cloudwatch_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(datetime.utcnow().timestamp() * 1000),
                        'message': f'[{level}] {message}'
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to log to CloudWatch: {e}")
    
    def upload_to_s3(self, file_key: str, file_content: bytes) -> bool:
        """Upload file to S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=file_key,
                Body=file_content
            )
            self.log_to_cloudwatch(f"Uploaded file to S3: {file_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload to S3: {e}")
            self.log_to_cloudwatch(f"S3 upload failed: {e}", 'ERROR')
            return False
    
    def download_from_s3(self, file_key: str) -> Optional[bytes]:
        """Download file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=file_key
            )
            return response['Body'].read()
        except Exception as e:
            logger.error(f"Failed to download from S3: {e}")
            return None
    
    def invoke_lambda(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke Lambda function for processing"""
        try:
            response = self.lambda_client.invoke(
                FunctionName=self.lambda_function,
                InvocationType='RequestResponse',
                Payload=str(payload)
            )
            return response
        except Exception as e:
            logger.error(f"Failed to invoke Lambda: {e}")
            self.log_to_cloudwatch(f"Lambda invocation failed: {e}", 'ERROR')
            return {}
    
    def put_dynamodb_item(self, item: Dict[str, Any]) -> bool:
        """Put item to DynamoDB table"""
        try:
            table = self.dynamodb_client.Table(self.dynamodb_table)
            table.put_item(Item=item)
            return True
        except Exception as e:
            logger.error(f"Failed to put DynamoDB item: {e}")
            return False
    
    def get_dynamodb_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get item from DynamoDB table"""
        try:
            table = self.dynamodb_client.Table(self.dynamodb_table)
            response = table.get_item(Key=key)
            return response.get('Item')
        except Exception as e:
            logger.error(f"Failed to get DynamoDB item: {e}")
            return None
    
    def query_dynamodb(self, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query DynamoDB table"""
        try:
            table = self.dynamodb_client.Table(self.dynamodb_table)
            response = table.query(**query_params)
            return response.get('Items', [])
        except Exception as e:
            logger.error(f"Failed to query DynamoDB: {e}")
            return []
    
    # Note: Full implementation would mirror LocalStorageAdapter interface
    # This is a stub showing the AWS integration pattern
