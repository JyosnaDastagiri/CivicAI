"""
Configurable object storage abstraction (Requirement #34).

STORAGE_PROVIDER=local   -> saves to LOCAL_UPLOAD_DIR, serves via /uploads static mount.
STORAGE_PROVIDER=supabase -> uploads to a Supabase Storage bucket via REST API.

If Supabase credentials are missing while STORAGE_PROVIDER=supabase, the
service automatically falls back to local storage instead of crashing.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path

import httpx

from app.core.config import get_settings

settings = get_settings()

ALLOWED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 8 * 1024 * 1024  # 8 MB


class UnsupportedFileError(Exception):
    pass


def _local_dir() -> Path:
    base = Path(__file__).resolve().parents[3] / "uploads"
    base.mkdir(parents=True, exist_ok=True)
    return base


def validate_file(mime_type: str, size_bytes: int) -> None:
    if mime_type not in ALLOWED_MIME_TYPES:
        raise UnsupportedFileError(f"Unsupported file type: {mime_type}. Allowed: JPG, JPEG, PNG, WEBP.")
    if size_bytes > MAX_FILE_SIZE_BYTES:
        raise UnsupportedFileError("File too large. Maximum size is 8 MB.")


def save_file(content: bytes, original_filename: str, mime_type: str) -> str:
    """Saves the file and returns a public/relative URL."""
    validate_file(mime_type, len(content))
    ext = Path(original_filename).suffix or ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"

    if settings.STORAGE_PROVIDER == "supabase" and settings.SUPABASE_URL and settings.SUPABASE_SERVICE_KEY:
        try:
            url = (
                f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_BUCKET}/{unique_name}"
            )
            headers = {
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
                "Content-Type": mime_type,
            }
            with httpx.Client(timeout=15) as client:
                resp = client.post(url, headers=headers, content=content)
                resp.raise_for_status()
            return f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{unique_name}"
        except Exception:
            pass  # fall through to local storage

    dest = _local_dir() / unique_name
    with open(dest, "wb") as f:
        f.write(content)
    return f"/uploads/{unique_name}"
