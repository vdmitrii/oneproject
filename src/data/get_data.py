import boto3
import os
from os import path
from dotenv import load_dotenv
import pandas as pd
import click
from botocore.exceptions import ClientError

@click.command()
@click.argument("input_path", type=click.Path())
@click.argument("output_path", type=click.Path())
def get_data(input_path: str, output_path: str):
    bucket_name = 'junk'
    session = boto3.session.Session()
    ENDPOINT = "https://storage.yandexcloud.net"

    session = boto3.Session(
        aws_access_key_id=(os.environ['ACCESS_KEY_ID']),
        aws_secret_access_key=(os.environ['SECRET_ACCESS_KEY']),
        region_name="ru-central1",
    )
    s3 = session.client("s3", endpoint_url=ENDPOINT)
    
    with open(input_path, "wb") as f:
            s3.download_fileobj(bucket_name, 'data/data.xlsx', f)
            
    df = pd.read_excel(input_path, usecols=['date', 'time_interval', 'quantity'])
    click.echo(f'Selected {len(df)} samples.')
    
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    load_dotenv()
    get_data()
