import logging

from fastapi import FastAPI, Depends
from app.config import get_settings, Settings
from api import predict

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    return application


app = create_application()


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

@app.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    date_string = await crud.post(payload)

    response_object = {
        "time_interval": date_string,
        "quantity": payload.url
    }
    return response_object