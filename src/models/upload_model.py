import boto3
import os
from os import path
from dotenv import load_dotenv
import pandas as pd
import click
from botocore.exceptions import ClientError


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
def upload_model(input_path: str):
    bucket_name = 'junk'
    file_name = 'models/catboost_model.cbm'
    session = boto3.session.Session()

    ENDPOINT = "https://storage.yandexcloud.net"

    session = boto3.Session(
        aws_access_key_id=(os.environ['ACCESS_KEY_ID']),
        aws_secret_access_key=(os.environ['SECRET_ACCESS_KEY']),
        region_name="ru-central1",
    )
    s3 = session.client("s3", endpoint_url=ENDPOINT)
    with open(file_name, "rb") as f:
            s3.upload_fileobj(f, bucket_name, "model/catboost_model.cbm")


if __name__ == "__main__":
    load_dotenv()
    upload_model()
