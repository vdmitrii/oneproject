import pandas as pd
import numpy as np
import click


@click.command()
@click.argument("input_path", type=click.Path())
@click.argument("output_path", type=click.Path())
def add_features(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    # df.set_index('date', drop=True, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.weekday
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    df['day_of_year'] = df['date'].dt.dayofyear
    df['is_month_start'] = df['date'].dt.is_month_start
    df['is_month_end'] = df['date'].dt.is_month_end
    df['is_quarter_start'] = df['date'].dt.is_quarter_start
    df['is_quarter_end'] = df['date'].dt.is_quarter_end
    df['is_year_start'] = df['date'].dt.is_year_start
    df['is_year_end'] = df['date'].dt.is_year_end
    df['is_weekend'] = df['weekday'].isin([5, 6])
    df['is_friday'] = df['weekday'] == 4
    df['year_month'] = df['date'].dt.year.astype(str) + df['date'].dt.strftime('%m')
    df['is_month_start'] = df['is_month_start'].astype(int)
    df['is_month_end'] = df['is_month_end'].astype(int)
    df['is_quarter_start'] = df['is_quarter_start'].astype(int)
    df['is_quarter_end'] = df['is_quarter_end'].astype(int)
    df['is_year_start'] = df['is_year_start'].astype(int)
    df['is_year_end'] = df['is_year_end'].astype(int)
    df['is_weekend'] = df['is_weekend'].astype(int)
    df['is_friday'] = df['is_friday'].astype(int)
    
    df.to_csv(output_path)


if __name__ == "__main__":
    add_features()
