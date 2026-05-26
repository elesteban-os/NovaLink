import os
import sys
from pathlib import Path
import logging

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Set environment defaults BEFORE importing app modules
os.environ.setdefault("DB_USER", "novalink_user")
os.environ.setdefault("DB_PASSWORD", "novalink_password")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5435")
os.environ.setdefault("DB_NAME", "skills_db")
os.environ.setdefault("DB_ECHO", "false")

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
    f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
)

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
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
