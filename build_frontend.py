#!/usr/bin/env python3
"""Build the React QR frontend into frontend/dist.

The FastAPI backend serves the result through the existing GET /qr endpoint
(see backend/app.py):

    frontend/dist/index.html  ->  GET /qr            (FileResponse)
    frontend/dist/assets/*    ->  GET /qr/assets/*    (StaticFiles mount)

Usage:
    python build_frontend.py                 # npm install + npm run build
    python build_frontend.py --skip-install  # skip 'npm install'

Requires Node.js >= 18 and npm on PATH.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"


def find_npm() -> str:
    npm = shutil.which("npm")
    if npm is None:
        sys.exit("ERROR: npm was not found on PATH — install Node.js >= 18 first.")
    return npm


def run(cmd: list) -> None:
    print(f"+ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=FRONTEND_DIR, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the React QR frontend.")
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="skip 'npm install' and reuse the existing node_modules",
    )
    args = parser.parse_args()

    npm = find_npm()

    if not args.skip_install:
        run([npm, "install"])

    run([npm, "run", "build"])

    index_html = DIST_DIR / "index.html"
    if not index_html.is_file():
        sys.exit(f"ERROR: build did not produce {index_html}")

    print(
        f"\nOK: frontend built into {DIST_DIR} — "
        "the /qr endpoint now serves the React app."
    )


if __name__ == "__main__":
    main()
