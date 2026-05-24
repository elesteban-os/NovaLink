"""HTTP handlers for the skills service.

Template for this service:
- Endpoint input: POST, GET, PUT, DELETE on `/skills`.
- Business logic: validate and delegate to `SkillService`.
- Endpoint output: skill DTOs or HTTP status codes.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.persistence.schemas import SkillCreate, SkillUpdate, SkillResponse
from app.services.skill_service import SkillService
from app.logger import logger

# Configure router
router = APIRouter(prefix="/skills", tags=["skills"])
service = SkillService()


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear skill",
    responses={
        400: {"description": "Datos inválidos"},
        500: {"description": "Error interno"}
    }
)
def create_skill(
    obj_in: SkillCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new skill.
    
    - **skill_name**: Skill name (required)
    - **difficulty_level**: Difficulty between 0 and 10
    - **stock**: Available stock
    """
    try:
        return service.create_skill(db, obj_in)
    except ValueError as e:
        logger.error(f"Error validación: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error creando skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get(
    "",
    response_model=List[SkillResponse],
    summary="Listar skills"
)
def get_skills(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List skills with pagination."""
    try:
        return service.get_skills(db, skip=skip, limit=limit)
    except Exception as e:
        logger.exception(f"Error listando skills: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Obtener skill por ID",
    responses={
        404: {"description": "Skill no encontrado"}
    }
)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """Get skill details by ID."""
    try:
        return service.get_skill(db, skill_id)
    except ValueError as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error obteniendo skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Actualizar skill",
    responses={
        404: {"description": "Skill no encontrado"}
    }
)
def update_skill(
    skill_id: int,
    obj_in: SkillUpdate,
    db: Session = Depends(get_db)
):
    """Update skill details."""
    try:
        return service.update_skill(db, skill_id, obj_in)
    except ValueError as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error actualizando skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar skill",
    responses={
        404: {"description": "Skill no encontrado"}
    }
)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """Delete skill by ID."""
    try:
        success = service.delete_skill(db, skill_id)
        if not success:
            raise ValueError(f"Skill {skill_id} no encontrado")
    except ValueError as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error eliminando skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
