import os
import sys
from pathlib import Path

import httpx
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
os.environ.setdefault("DB_PORT", "5436")
os.environ.setdefault("DB_NAME", "orders_db")
os.environ.setdefault("DB_ECHO", "false")
os.environ.setdefault("JWT_SECRET", "SUPER_SECRET_KEY")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("AUTH_SERVICE_URL", "http://localhost:8007/auth/login")
os.environ.setdefault("AUTH_TEST_USER_EMAIL", "test@example.com")
os.environ.setdefault("AUTH_TEST_USER_PASSWORD", "password123")

from app.main import app
from app.database import get_db
from app.persistence.models import Base

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
    # report.when in ('setup','call','teardown')
    if report.when == "call":
        status = report.outcome.upper()
        logger.info("[TEST RESULT] %s -> %s", report.nodeid, status)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Asegura que la base de datos de pruebas refleje el esquema actual.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def auth_token():
    auth_login_url = os.environ["AUTH_SERVICE_URL"]
    credentials = {
        "email": os.environ["AUTH_TEST_USER_EMAIL"],
        "password": os.environ["AUTH_TEST_USER_PASSWORD"],
    }
    try:
        response = httpx.post(auth_login_url, json=credentials, timeout=10.0)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            pytest.skip(
                f"Auth login succeeded but response did not include access_token"
            )
        return token
    except Exception as exc:
        pytest.skip(f"Auth token could not be obtained from {auth_login_url}: {exc}")


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
