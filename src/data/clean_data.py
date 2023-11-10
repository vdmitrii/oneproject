import pandas as pd
import numpy as np
import click


@click.command()
@click.argument("input_path", type=click.Path())
@click.argument("output_path", type=click.Path())
def clean_data(input_path: str, output_path: str):
    df: pd.DataFrame = pd.read_csv(input_path)
    df['quantity'] = np.where(df['time_interval'].shift() == 24, \
        df['quantity'].shift() + df['quantity'], df['quantity'])
    df.fillna(0, inplace=True)
    
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    clean_data()
