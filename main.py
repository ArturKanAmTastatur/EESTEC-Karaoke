"""EESTEC Karaoke — server entrypoint.

Starts the FastAPI DJ song request & queue management server.

Run from the project root:
    python main.py [--host HOST] [--port PORT]

The PyQt desktop control panel (desktop/main.py) reuses start_server()
from this module to embed the server as a background thread.
"""

import argparse
import threading

import uvicorn

from backend.app import create_app


def start_server(host: str = "0.0.0.0", port: int = 8000) -> threading.Thread:
    """Start the FastAPI DJ request server in a background (daemon) thread."""
    server_app = create_app()
    thread = threading.Thread(
        target=uvicorn.run,
        args=(server_app,),
        kwargs={"host": host, "port": port, "log_level": "info"},
        daemon=True,
    )
    thread.start()
    print(f"DJ request server running at http://{host}:{port} (guest page: /qr)")
    return thread


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="EESTEC Karaoke — DJ request server entrypoint"
    )
    parser.add_argument("--host", default="0.0.0.0", help="server bind address")
    parser.add_argument("--port", type=int, default=8000, help="server port")
    args = parser.parse_args()

    # When run as a script, keep uvicorn in the foreground so the process
    # stays alive (Ctrl+C stops the server).
    uvicorn.run(create_app(), host=args.host, port=args.port, log_level="info")
