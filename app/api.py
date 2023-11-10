from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Path

from app.api import crud
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
)

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings





@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:  # type: ignore
    return await crud.get_all()


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int = Path(..., gt=0)) -> SummarySchema:  # type: ignore
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema, background_tasks: BackgroundTasks
) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)
    background_tasks.add_task(generate_summary, summary_id, payload.url)
    response_object = {"id": summary_id, "url": payload.url}
    return response_object
