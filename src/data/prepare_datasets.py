import pandas as pd
import numpy as np
import click
import os
import dvc.api


@click.command()
@click.argument("input_filepath", type=click.Path())
@click.argument("output_file_paths", type=click.Path(), nargs=2)
def prepare_datasets(input_filepath: str, output_file_paths: str):
    df = pd.read_csv(input_filepath)
    df['quantity'] = np.where(df['time_interval'].shift() == 24, df['quantity'].shift() + df['quantity'], df['quantity'])
    df = df[df.time_interval != 24]
    
    params = dvc.api.params_show()
    split_date = params['prep']['split_date']
    click.echo(split_date)
    
    df.fillna(0, inplace=True)
    
    train = df.sample(frac=0.80, random_state=42)
    test = df.drop(train.index)

    train.to_csv(output_file_paths[0], index=False)
    test.to_csv(output_file_paths[1], index=False)



if __name__ == "__main__":
    prepare_datasets()
