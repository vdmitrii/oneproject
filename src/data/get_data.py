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
    df = pd.read_csv(input_path, usecols=['date', 'time_interval', 'quantity'])
    click.echo(f'Всего {len(df)} строк.')
    
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    load_dotenv()
    get_data()
