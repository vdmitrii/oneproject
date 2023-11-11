import os
from typing import List, Optional
from catboost import CatBoostRegressor
import numpy as np
import pandas as pd

from pydantic import BaseModel


class PredictionInput(BaseModel):
    date_string: file


class PredictionOutput(BaseModel):
    quantity: pd.Series | None


class ForecastModel:
    model: CatBoostRegressor

    def load_model(self):
        """Loads the model"""
        model_file = "models/catboost_model.cbm"
        regr = CatBoostRegressor()
        model = regr.load_model(model_file)
        
        self.model = model


    async def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model:
            raise RuntimeError("Модель не загружена")
        
        prediction = self.model.predict()
        return PredictionOutput(quantity=prediction)