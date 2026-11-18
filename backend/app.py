"""FastAPI application factory — DJ Song Request & Queue Management server.

Entrypoint: uvicorn backend.app:app  (or run the combined desktop+server
entrypoint: python main.py)
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.db import init_db
from backend.routers import dj, queue, songs

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
FRONTEND_DIST = FRONTEND_DIR / "dist"          # output of build_frontend.py
QR_INDEX_HTML = FRONTEND_DIST / "index.html"   # built React app entry point
QR_ASSETS_DIR = FRONTEND_DIST / "assets"       # hashed JS/CSS (base '/qr/')
LEGACY_QR_PAGE = FRONTEND_DIR / "qr.html"      # pre-React placeholder page


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

    # Serve the built React app's hashed bundles (frontend/dist/assets,
    # produced by build_frontend.py) under /qr/assets. Mounted only when the
    # build exists, so a fresh checkout without Node can still run the
    # server — the /qr route then falls back to the legacy placeholder.
    if QR_ASSETS_DIR.is_dir():
        app.mount(
            "/qr/assets", StaticFiles(directory=QR_ASSETS_DIR), name="qr_assets"
        )

    @app.get("/qr", response_class=HTMLResponse, tags=["pages"])
    def guest_request_page() -> FileResponse:
        """Serve the guest song request page.

        Serves the React app built into frontend/dist by build_frontend.py;
        falls back to the static frontend/qr.html placeholder when the build
        has not been run yet.
        """
        if QR_INDEX_HTML.is_file():
            return FileResponse(QR_INDEX_HTML, media_type="text/html")
        print(
            "WARNING: frontend/dist not found — run 'python build_frontend.py' "
            "to build the React QR page; serving the legacy qr.html placeholder."
        )
        return FileResponse(LEGACY_QR_PAGE, media_type="text/html")

    return app


app = create_app()
