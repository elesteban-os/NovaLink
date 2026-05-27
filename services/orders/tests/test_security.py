import jwt
from starlette.requests import Request

from app.config import settings
from app.core.security import verify_token


def build_request(headers: dict[str, str]) -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [
            (name.encode("utf-8"), value.encode("utf-8"))
            for name, value in headers.items()
        ],
    }
    return Request(scope)


def test_verify_token_returns_user_id():
    token = jwt.encode(
        {"user_id": 42}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    request = build_request({"authorization": f"Bearer {token}"})

    user_id = verify_token(request)
    assert user_id == 42


def test_verify_token_raises_for_missing_header():
    request = build_request({})
    try:
        verify_token(request)
        assert False, "verify_token should raise HTTPException for missing header"
    except Exception as exc:
        assert exc.status_code == 401
        assert exc.detail == "Missing or invalid token"


def test_verify_token_raises_for_invalid_token():
    request = build_request({"authorization": "Bearer invalid.token.value"})
    try:
        verify_token(request)
        assert False, "verify_token should raise HTTPException for invalid token"
    except Exception as exc:
        assert exc.status_code == 401
        assert exc.detail == "Invalid token"
