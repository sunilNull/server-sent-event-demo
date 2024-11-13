import logging
import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.endpoints import task
from app.config import get_settings

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

APP_ROOT = Path(__file__).parent.parent


templates = Jinja2Templates(directory="templates")


def get_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files and templates
    app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

    # Include routers
    app.include_router(task.router, prefix="/api/v1")

    def init_db():
        conn = sqlite3.connect("tasks.db")
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks
            (id TEXT PRIMARY KEY, 
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            version INTEGER default 1)
        """
        )
        conn.commit()
        conn.close()

    # Initialize database
    init_db()

    return app
