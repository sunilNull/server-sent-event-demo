import uvicorn

from app.config import get_settings

settings = get_settings()


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        app="app.application:get_app",
        reload=True,
        workers=2,
        port=8000,
        host="0.0.0.0",
    )


if __name__ == "__main__":
    main()
