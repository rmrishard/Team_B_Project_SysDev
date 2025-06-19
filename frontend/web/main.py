from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import os
from pathlib import Path

app = FastAPI(
    root_path="",
    version="1",
    openapi_url=None,
    docs_url=None,
    redoc_url=None)

# Setup origins that may be triggered by local testing
origins = [
    "http://localhost:8777",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="9kTqAH54CmOTdH208Jg04npHb4zB3LMv/CcSqNinHvo",
    same_site='strict',
    https_only=False
)

@app.get("/{file_path:path}")
def read_root(request: Request, file_path: str):
    WEB_DIR = Path("./app/static")

    if not file_path or file_path=="/":
        file_path = "index.html"

    if file_path.startswith("."):
        raise HTTPException(status_code=404, detail="File not found")

    # Resolve the full path and ensure it's within the web directory
    full_path = (WEB_DIR / file_path).resolve()


    # Security check: ensure the resolved path is within WEB_DIR
    try:
        full_path.relative_to(WEB_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=404, detail="File not found")

    print(request.session)

    # Check if file exists
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path)