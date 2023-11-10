from fastapi import APIRouter, Depends
from app.config import Settings, get_settings
import os
from typing import List, Tuple
import joblib
from sklearn.pipeline import Pipeline

# Load the model
model_file = os.path.join(os.path.dirname(__file__), "catboost_model.cbm")
loaded_model: Tuple[Pipeline, List[str]] = joblib.load(model_file)
model, targets = loaded_model

# Run a prediction
p = model.predict(["computer"])
print(targets[p[0]])
