import click
import pandas as pd
import time
from catboost import CatBoostRegressor
import numpy as np
from typing import List
from sklearn.metrics import mean_absolute_error, mean_squared_error
# import mlflow
# from mlflow import MlflowClient
# from mlflow.models import infer_signature
# from mlflow.models.signature import ModelSignature
# from mlflow.types.schema import Schema, ColSpec
from scipy import stats
import os
from datetime import datetime
from dotenv import load_dotenv
import sys    


load_dotenv()

# MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# exp_name = f"Catboost Experiment"
# mlflow.create_experiment(exp_name)

@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def train(input_path: str, output_path: str):
    # mlflow.set_experiment(exp_name)
    # with mlflow.start_run():
    #     mlflow.get_artifact_uri()
        
    # click.echo(mlflow.get_artifact_uri())
    click.echo(f'Разбиваем на train и test')
    df = pd.read_csv(input_path)
    train = df.sample(frac=0.8, random_state=42)
    test = df.drop(train.index)

    X = train.drop(['date', 'quantity'], axis=1)
    y = train['quantity']

    click.echo(f'Случайный поиск лучших параметров')       
    model = CatBoostRegressor(
        iterations=5000,
        random_seed=42,
        thread_count=-1,
        loss_function="MAE",
        eval_metric="MAE",
        verbose=500,
        )

    param_distribution = {
        "one_hot_max_size": stats.bernoulli(p=0.2, loc=2),
        "learning_rate": [0.03, 0.1, 0.3],
        "l2_leaf_reg": [2, 5, 7],
        "depth": stats.binom(n=10, p=0.2),
    }
    randomized_search_result = model.randomized_search(param_distribution, X, y)
    searched_params = randomized_search_result["params"]
    # mlflow.log_params(searched_params)
    
    model = CatBoostRegressor(
        iterations=5000,
        random_seed=42,
        thread_count=-1,
        loss_function="MAE",
        eval_metric="MAE",
        verbose=500,
        **searched_params
    )

    model.fit(
        train.drop(['date', 'quantity'], axis=1),
        train['quantity'],
        verbose=False,
        plot=False)
    
    
    click.echo(f'Предсказываем на test')        
    pred = model.predict(test.drop(['date', 'quantity'], axis=1))
    mae = np.mean(np.abs(pred - test['quantity']))
    bias = np.mean((pred - test['quantity']))
    score = round(mae + abs(bias), 2)
    # mlflow.log_metrics({'MAE_bias': score})


    click.echo(f'Обучаемся на всех данных')
    model = CatBoostRegressor(
        iterations=5000,
        random_seed=42,
        thread_count=-1,
        loss_function="MAE",
        eval_metric="MAE",
        verbose=500,
        **searched_params
    )

    model.fit(
        df.drop(['date', 'quantity'], axis=1),
        df['quantity'],
        verbose=False,
        plot=False)
    model.save_model(output_path, format="cbm")
    
    click.echo(f'Логируем модель')
    # signature = infer_signature(X, y)
    # mlflow.catboost.log_model(cb_model=model,
    #                             artifact_path="model_path",
    #                             registered_model_name="catboost_model",
    #                             signature=signature)

    # mlflow.log_artifact(__file__)
    

if __name__ == "__main__":
    train()

