import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import logging

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("DB_USER", "novalink_user")
os.environ.setdefault("DB_PASSWORD", "novalink_password")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "users_db")
os.environ.setdefault("DB_ECHO", "false")
os.environ.setdefault("JWT_SECRET", "SUPER_SECRET_KEY")
os.environ.setdefault("JWT_ALGORITHM", "HS256")

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    f"sqlite:///./test_users.db"
)

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.main import app
from app.database import get_db
from app.persistence.models import Base

if TEST_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(TEST_DATABASE_URL, echo=False)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configure test logging
logging.basicConfig()
logger = logging.getLogger("tests")
logger.setLevel(logging.INFO)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def pytest_runtest_logstart(nodeid, location):
    logger.info("[TEST START] %s", nodeid)


def pytest_runtest_logreport(report):
    if report.when == "call":
        status = report.outcome.upper()
        logger.info("[TEST RESULT] %s -> %s", report.nodeid, status)


@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
