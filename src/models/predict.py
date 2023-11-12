import click
import pandas as pd
import time
from catboost import CatBoostRegressor
import numpy as np
from typing import List
from sklearn.metrics import mean_absolute_error, mean_squared_error
import holidays
import mlflow
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from features.add_features import add_features


def add_features(df):
    df.fillna(0, inplace=True)
    ru_holidays = holidays.country_holidays("RU")
    df['date'] = pd.to_datetime(df['date'])
    df['is_holiday'] = df['date'].map(lambda x: x in ru_holidays)
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
    df = df.drop('date', axis=1)
    # Приводим boolean к 0/1
    df = df.astype(float)

    return df

@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def predict(input_paths: List[str], output_path: str):
    df = pd.read_csv(input_paths[0], usecols=['date', 'time_interval'])
    df = add_features(df)
 
    model = CatBoostRegressor()
    model.load_model(input_paths[1])
    predics = model.predict(df.values)

    # logged_model = 'runs:/d981dd2939c748fe9c7142dde9c832a8/model'
    # loaded_model = mlflow.catboost.load_model(logged_model)
    # loaded_model.predict(pd.DataFrame(data_test))
    
    predics_df = pd.DataFrame(predics)
    predics_df.to_csv(output_path, index=False)
    
    mlflow.log_artifact(output_path)

if __name__ == "__main__":
    predict()

