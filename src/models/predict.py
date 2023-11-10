import click
import pandas as pd
import time
from catboost import CatBoostRegressor
import numpy as np
from typing import List
from sklearn.metrics import mean_absolute_error, mean_squared_error


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def predict(input_paths: List[str], output_path: str):
    test_df = pd.read_csv(input_paths[0])

    X_test = test_df.drop(['date', 'quantity'], axis=1)
    y_test = test_df['quantity']

    model = CatBoostRegressor()
    model.load_model(input_paths[1])

    y_predicted = model.predict(X_test)
    
    score = pd.DataFrame(
        dict(
            mae=mean_absolute_error(y_test, y_predicted),
            rmse=mean_squared_error(y_test, y_predicted, squared=False)
        ),
        index=[0],
    )

    score.to_csv(output_path, index=False)


if __name__ == "__main__":
    predict()

