import os
from typing import List, Optional
from catboost import CatBoostRegressor
import numpy as np
import pandas as pd

from pydantic import BaseModel


class PredictionInput(BaseModel):
    date_string: List[str]


class PredictionOutput(BaseModel):
    quantity: pd.Series | None


class ForecastModel:
    model: CatBoostRegressor

    def load_model(self):
        """Loads the model"""
        model_file = os.path.join(os.path.dirname(__file__), "catboost_model.cbm")
        model = CatBoostRegressor()      # parameters not required.
        model.load_model(model_file)
        
        loaded_model: bytes = c.load(model_file)
        model, targets = loaded_model
        self.model = loaded_model


    async def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model:
            raise RuntimeError("Модель не загружена")
        
        prediction = self.model.predict([input])
        return PredictionOutput(quantity=prediction)