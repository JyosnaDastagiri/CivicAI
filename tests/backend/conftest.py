import os
import sys
import pytest
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

os.environ["USE_SQLITE"] = "true"
os.environ["SQLITE_PATH"] = str(BACKEND_DIR / "test_civicai.db")
os.environ["AI_MODE"] = "demo"

db_path = BACKEND_DIR / "test_civicai.db"
if db_path.exists():
    db_path.unlink()

from fastapi.testclient import TestClient  # noqa: E402
from app.core.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402  (import triggers Base.metadata.create_all on a clean file)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
    if db_path.exists():
        db_path.unlink()


@pytest.fixture()
def client():
    return TestClient(app)


