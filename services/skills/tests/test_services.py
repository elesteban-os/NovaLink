import pytest

from app.persistence import crud
from app.persistence.models import Skill
from app.persistence.schemas import SkillCreate
from app.services.skill_service import SkillService

service = SkillService()


def test_create_skill_rejects_duplicate(db_session):
    first_payload = SkillCreate(
        skill_name="test_liderazgo_unique", difficulty_level=7, stock=100
    )
    crud.create_skill(db_session, first_payload)

    duplicate_payload = SkillCreate(
        skill_name="test_liderazgo_unique", difficulty_level=8, stock=80
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_skill(db_session, duplicate_payload)

    assert "ya existe" in str(exc_info.value)


def test_get_skill_raises_when_missing(db_session):
    with pytest.raises(ValueError) as exc_info:
        service.get_skill(db_session, skill_id=999)

    assert "no encontrado" in str(exc_info.value)


def test_reserve_stock_reduces_quantity(db_session):
    payload = SkillCreate(
        skill_name="test_creatividad_unique", difficulty_level=5, stock=100
    )
    created = crud.create_skill(db_session, payload)

    reserved = service.reserve_stock(
        db_session, skill_name="test_creatividad_unique", quantity=5
    )

    assert reserved.skill_id == created.skill_id
    assert reserved.stock == 95


def test_reserve_stock_raises_when_insufficient(db_session):
    payload = SkillCreate(
        skill_name="test_comunicacion_unique", difficulty_level=3, stock=2
    )
    crud.create_skill(db_session, payload)

    with pytest.raises(ValueError) as exc_info:
        service.reserve_stock(
            db_session, skill_name="test_comunicacion_unique", quantity=5
        )

    assert "Stock insuficiente" in str(exc_info.value)
