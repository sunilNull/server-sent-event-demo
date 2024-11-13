import asyncio
import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from app.dependencies import get_db
from app.schemas.task import TaskStatus, TaskStatusResponse
from app.services.events import event_manager
from app.services.task import TaskService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    from app.application import templates

    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/task/{task_id}/status", response_model=TaskStatusResponse)
async def update_status(task_id: str, status_update: TaskStatus, db: Session = Depends(get_db)):
    try:
        task_service = TaskService(db)
        task = await task_service.update_status(task_id, status_update)
        return task
    except Exception as e:
        logger.error(f"Error updating task status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/task/{task_id}/status/stream")
async def stream_status(task_id: str):
    async def event_generator():
        queue = await event_manager.subscribe(task_id)
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=30)
                    yield {"event": "status_update", "data": json.dumps(data)}
                except asyncio.TimeoutError:
                    yield {"event": "ping", "data": ""}
        except asyncio.CancelledError:
            await event_manager.unsubscribe(task_id, queue)

    return EventSourceResponse(event_generator())
