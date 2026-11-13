"""FastAPI application factory — DJ Song Request & Queue Management server.

Entrypoint: uvicorn backend.app:app  (or run the combined desktop+server
entrypoint: python main.py)
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from backend.db import init_db
from backend.routers import dj, queue, songs

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
QR_PAGE = FRONTEND_DIR / "qr.html"


def create_app() -> FastAPI:
    app = FastAPI(
        title="EESTEC Karaoke DJ Server",
        description="Song request & queue management API (see issue #3 for the contract)",
        version="0.1.0",
    )

    # Allow the frontends (Components 3 & 4, issues #6/#7) to call the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(songs.router)
    app.include_router(queue.router)
    app.include_router(dj.router)

    @app.on_event("startup")
    def on_startup() -> None:
        try:
            init_db()
        except NotImplementedError:
            # db.py is a stub — Component 2 (issue #5) implements init_db()
            print("WARNING: init_db() not implemented yet (Component 2, issue #5)")

    @app.get("/qr", response_class=HTMLResponse, tags=["pages"])
    def guest_request_page() -> FileResponse:
        """Serve the guest song request form page

        Serves frontend/qr.html — should be built separatly on startup in the future
        """
        return FileResponse(QR_PAGE, media_type="text/html")

    return app


app = create_app()
