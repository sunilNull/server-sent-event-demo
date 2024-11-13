import logging
from datetime import datetime

from sqlalchemy.orm import Session

from ..models.task import Task
from ..schemas.task import TaskStatus
from .events import event_manager

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    async def update_status(self, task_id: str, status_update: TaskStatus) -> Task:
        task = self.db.query(Task).filter(Task.id == task_id).first()

        if task:
            task.status = status_update.status
            task.updated_at = datetime.utcnow()
            task.version += 1
        else:
            task = Task(
                id=task_id,
                status=status_update.status,
            )
            self.db.add(task)

        try:
            self.db.commit()
            await event_manager.publish(
                task_id, {"status": task.status, "timestamp": task.updated_at.isoformat(), "version": task.version}
            )
            return task
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating task status: {e}")
            raise
