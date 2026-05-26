from app.persistence import crud
from app.persistence.models import Skill
from app.persistence.schemas import SkillCreate, SkillUpdate


def test_create_skill_persists(db_session):
    payload = SkillCreate(skill_name="test_curiosidad_unique", difficulty_level=4, stock=120)

    saved = crud.create_skill(db_session, payload)

    assert saved.skill_id is not None
    assert saved.skill_name == "test_curiosidad_unique"
    assert saved.difficulty_level == 4
    assert saved.stock == 120
    assert saved.is_active is True

    fetched = db_session.query(Skill).filter_by(skill_name="test_curiosidad_unique").one()
    assert fetched.skill_id == saved.skill_id
    assert fetched.stock == 120


def test_update_skill_persists_changes(db_session):
    payload = SkillCreate(skill_name="test_adaptabilidad_unique", difficulty_level=5, stock=80)
    saved = crud.create_skill(db_session, payload)

    update_payload = SkillUpdate(difficulty_level=6, stock=90)
    updated = crud.update_skill(db_session, saved, update_payload)

    assert updated.difficulty_level == 6
    assert updated.stock == 90
    assert updated.skill_name == "test_adaptabilidad_unique"


def test_delete_skill_removes_entity(db_session):
    payload = SkillCreate(skill_name="test_paciencia_unique", difficulty_level=2, stock=50)
    saved = crud.create_skill(db_session, payload)

    deleted = crud.delete_skill(db_session, saved.skill_id)
    assert deleted is True

    missing = db_session.query(Skill).filter_by(skill_id=saved.skill_id).first()
    assert missing is None


def test_get_skills_filters_by_active(db_session):
    payload_a = SkillCreate(skill_name="test_humor_unique", difficulty_level=2, stock=40)
    payload_b = SkillCreate(skill_name="test_silencio_unique", difficulty_level=1, stock=10)
    first = crud.create_skill(db_session, payload_a)
    second = crud.create_skill(db_session, payload_b)

    first.is_active = False
    db_session.add(first)
    db_session.commit()

    active_results = crud.get_skills(db_session, skip=0, limit=100)
    assert all(skill.is_active for skill in active_results)
    assert any(skill.skill_id == second.skill_id for skill in active_results)
    assert all(skill.skill_id != first.skill_id for skill in active_results)
