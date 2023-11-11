import click
import pandas as pd
import time
from catboost import CatBoostRegressor
import numpy as np
from typing import List
from sklearn.metrics import mean_absolute_error, mean_squared_error
import mlflow
from mlflow import MlflowClient
from mlflow.models.signature import infer_signature
import os
from dotenv import load_dotenv


load_dotenv()
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Forecaster")

@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def train(input_path: str, output_path: str):
    with mlflow.start_run():
        mlflow.get_artifact_uri()

        train_df = pd.read_csv(input_path)

        X_train = train_df.drop(['date', 'quantity'], axis=1)
        y_train = train_df['quantity']
    
        clf = CatBoostRegressor(thread_count=-1,
                                loss_function='MAE',
                                random_seed=42)

        clf.fit(
            X_train,
            y_train,
            # eval_set=(X_test, y_test),
            verbose=200,
            # use_best_model=True,
            plot=False,
            early_stopping_rounds=100,
        )

        params = {
            'l2_leaf_reg': 2, 
            'depth': 6.0,
            'one_hot_max_size': 2.0, 
            'learning_rate': 0.1}
        
        # clf.save_model(output_path, format="cbm")

        signature = infer_signature(x_holdout, y_predicted)

        mlflow.log_params(params)
        mlflow.log_metrics(score)
        mlflow.lightgbm.log_model(lgb_model=gbm,
                                  artifact_path="catboost_model",
                                  registered_model_name="forecast_catboost",
                                  signature=signature)
        
        client = mlflow.MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
        experiment = dict(mlflow.get_experiment_by_name('Forecaster'))
        experiment_id = experiment['experiment_id']
        df = mlflow.search_runs([experiment_id])
        best_run_id = df.loc[0, 'run_id']
        
        path = client.download_artifacts(run_id=RUN_ID, path='dict_vectorizer.bin')
        


if __name__ == "__main__":
    train()

