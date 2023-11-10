import os
from typing import List, Optional, Tuple

from models import 
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sklearn.pipeline import Pipeline





app = FastAPI()
forecast_model = ForecastModel()


@app.post("/prediction")
async def prediction(
    output: PredictionOutput = Depends(forecast_model.predict),
) -> PredictionOutput:
    return output


@app.on_event("startup")
async def startup():
    forecast_model.load_model()
