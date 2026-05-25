"""Minimal LocalStack demo using S3 via boto3.

Requires LocalStack running locally (default http://localhost:4566).
"""

import os
import sys
from datetime import datetime

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def main() -> None:
    # Host-style endpoint recommended by LocalStack for S3
    endpoint = os.getenv("LOCALSTACK_ENDPOINT_URL", "http://s3.localhost.localstack.cloud:4566")
    bucket = "hello-localstack-bucket"
    key = "hello.txt"
    body = f"Hello LocalStack! UTC now: {datetime.now().isoformat()}\n"

    s3 = boto3.client("s3", endpoint_url=endpoint)

    try:
        s3.create_bucket(Bucket=bucket)
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")
        # If bucket already exists in LocalStack, proceed.
        if error_code not in {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}:
            raise

    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body.encode())
    except (BotoCoreError, ClientError) as exc:
        print(f"Failed to put object: {exc}", file=sys.stderr)
        raise

    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read().decode()
    print(f"Endpoint: {endpoint}")
    print(f"Bucket: {bucket}")
    print(f"Key: {key}")
    print("Content:")
    print(content)


if __name__ == "__main__":
    main()
