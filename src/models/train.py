import click
import pandas as pd
import time
from catboost import CatBoostRegressor
import numpy as np
from typing import List
from sklearn.metrics import mean_absolute_error, mean_squared_error


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def train(input_path: str, output_path: str):
    train_df = pd.read_csv(input_path)

    X_train = train_df.drop(['date', 'quantity'], axis=1)
    y_train = train_df['quantity']
 
    clf = CatBoostRegressor(thread_count=-1,
                            loss_function='RMSE',
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

    # params = {
    #     'l2_leaf_reg': 2, 
    #     'depth': 6.0,
    #     'one_hot_max_size': 2.0, 
    #     'learning_rate': 0.1}
    
    clf.save_model(output_path, format="cbm")


if __name__ == "__main__":
    train()

