import logging
from io import StringIO

from fastapi import FastAPI, Depends, File, UploadFile
from app.config import get_settings, Settings
from models import PredictionInput, PredictionOutput, ForecastModel
from catboost import CatBoostRegressor

# import mlflow

logged_model = f's3://mlflow-models-alexey/1/{RUN_ID}/artifacts/model'
# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)

log = logging.getLogger("uvicorn")
# memory = joblib.Memory(location="cache.joblib")

def create_application() -> FastAPI:
    application = FastAPI()
    return application


app = create_application()
# app = FastAPI()
# @app.post("/files")
# async def upload_file(file: UploadFile = File(...)):
#     return {"file_name": file.filename, "content_type": file.content_type}

# @app.post("/receive_df")
# def receive_df(df_in: str):
#     df = pd.DataFrame.read_json(df_in)

# #jupyter
# payload={"df_in":df.to_json()}
# requests.post("localhost:8000/receive_df", data=payload)


# @memory.cache(ignore=["model"])
@app.post("/prediction", data_file: str, status_code=201)
async def predict(data_file):
    df = pd.read_csv(StringIO(str(data_file.file.read(), 'utf-16')), encoding='utf-16')

    response_object = {
        "time_interval": date_string,
        "quantity": payload.url
    }
    return response_object

@app.on_event("startup")
async def startup_event():
    log.info("На старт...")
    # init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Поработали и хватит...")


@app.get("/ping")
def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }

