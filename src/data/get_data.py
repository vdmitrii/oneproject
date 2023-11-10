import pandas as pd
import click


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def get_data(input_path: str, output_path: str):
    df = pd.read_excel(input_path, usecols=['date', 'time_interval', 'quantity'])
    click.echo(f'Selected {len(df)} samples.')
    
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    get_data()

