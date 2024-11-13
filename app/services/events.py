import asyncio
import logging
from asyncio import Queue
from contextlib import asynccontextmanager
from typing import Dict, Set

logger = logging.getLogger(__name__)


class EventManager:
    def __init__(self):
        self._subscribers: Dict[str, Set[Queue]] = {}

    async def subscribe(self, task_id: str) -> Queue:
        if task_id not in self._subscribers:
            self._subscribers[task_id] = set()

        queue = Queue()
        self._subscribers[task_id].add(queue)
        return queue

    async def unsubscribe(self, task_id: str, queue: Queue):
        if task_id in self._subscribers:
            self._subscribers[task_id].discard(queue)
            if not self._subscribers[task_id]:
                del self._subscribers[task_id]

    async def publish(self, task_id: str, data: dict):
        if task_id not in self._subscribers:
            return

        for queue in self._subscribers[task_id]:
            await queue.put(data)


event_manager = EventManager()
