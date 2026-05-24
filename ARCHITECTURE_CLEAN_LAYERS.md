# Arquitectura en Capas Limpias - Opción 2

Estructura de carpetas recomendada para `services/orders` y `services/notifications` usando arquitectura limpia simplificada.

## Estructura de directorios

```
services/orders/app/
├── __init__.py
├── main.py              # Punto de entrada FastAPI
├── config.py            # Configuración y Settings
├── logger.py            # Logger del servicio
│
├── handlers/            # Capa de presentación (HTTP/Controllers)
│   ├── __init__.py
│   └── order_handler.py # Endpoints POST, GET, DELETE
│
├── services/            # Capa de aplicación (orquestación de negocio)
│   ├── __init__.py
│   └── order_service.py # Lógica de casos de uso
│
├── domain/              # Capa de dominio (lógica pura sin dependencias)
│   ├── __init__.py
│   ├── entities.py      # Entidades del negocio (Order, etc)
│   └── exceptions.py    # Excepciones de dominio
│
├── repositories/        # Abstracción de acceso a datos
│   ├── __init__.py
│   └── order_repository.py # Interfaz/contrato de persistencia
│
└── persistence/         # Implementación de acceso a datos
    ├── __init__.py
    ├── models.py        # SQLAlchemy ORM
    ├── schemas.py       # Pydantic para validación
    └── repository_impl.py # Implementación concreta del repositorio
```

## Responsabilidad de cada capa

| Capa | Carpeta | Contenido | Responsabilidad |
|------|---------|----------|-----------------|
| **Presentación** | `handlers/` | Routers FastAPI, endpoints | Recibir requests HTTP, validar entrada, retornar respuestas |
| **Aplicación** | `services/` | Lógica de casos de uso | Orquestar operaciones, aplicar reglas de negocio, coordinar repositorios |
| **Dominio** | `domain/` | Entidades, excepciones | Lógica pura sin dependencias externas, reglas de negocio críticas |
| **Persistencia** | `persistence/` + `repositories/` | ORM, Pydantic, implementación | Mapeo BD, serialización, implementación de contratos |

---

## Flujo de datos (ejemplo: crear orden)

```
Cliente HTTP Request
        ↓
┌─────────────────────────────────┐
│  handlers/order_handler.py      │ ← Recibe POST /orders
│  (validate_token, schema check) │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│  services/order_service.py      │ ← Ejecuta lógica de negocio
│  (create_order)                 │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│  domain/entities.py             │ ← Valida reglas de dominio
│  (Order entity validation)      │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│  repositories/                  │ ← Abstracción de datos
│  order_repository.py            │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│  persistence/repository_impl.py │ ← Implementación concreta
│  (INSERT en base de datos)      │
└────────────┬────────────────────┘
             ↓
        Order guardada
             ↓
      HTTP 201 Response
```

---

## Ventajas de esta arquitectura

✅ **Desacoplamiento**: Cambiar BD solo afecta `persistence/`  
✅ **Testabilidad**: Mock de repositorios sin tocar la BD  
✅ **Lógica limpia**: `domain/` puro sin dependencias externas  
✅ **Escalabilidad**: Fácil agregar nuevos handlers, servicios o repositorios  
✅ **Mantenibilidad**: Cada carpeta tiene una responsabilidad clara  
✅ **Reutilización**: `services/` puede usarse desde diferentes interfaces (HTTP, CLI, eventos)

---

## Ejemplo de código por capa

### 1. `domain/entities.py`
```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Order:
    """Entidad de dominio - Orden pura sin dependencias externas."""
    id: Optional[int] = None
    user_id: int = None
    skill_name: str = None
    quantity: int = None
    issued_by: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def validate(self) -> None:
        """Valida reglas de negocio del dominio."""
        if self.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if not self.skill_name or len(self.skill_name) > 255:
            raise ValueError("skill_name debe tener 1-255 caracteres")
```

### 2. `repositories/order_repository.py`
```python
from abc import ABC, abstractmethod
from typing import Optional, List
from ..domain.entities import Order

class OrderRepository(ABC):
    """Contrato/interfaz de acceso a datos."""
    
    @abstractmethod
    def create(self, order: Order) -> Order:
        """Crear una orden en la BD."""
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Obtener orden por ID."""
        pass
    
    @abstractmethod
    def list_by_user(self, user_id: int, skip: int = 0, limit: int = None) -> List[Order]:
        """Listar órdenes de un usuario."""
        pass
```

### 3. `services/order_service.py`
```python
from sqlalchemy.orm import Session
from ..domain.entities import Order
from ..repositories.order_repository import OrderRepository
from ..logger import logger

def create_order(
    repository: OrderRepository,
    user_id: int,
    skill_name: str,
    quantity: int
) -> Order:
    """Caso de uso: crear una orden."""
    
    # Crear entidad de dominio
    order = Order(
        user_id=user_id,
        skill_name=skill_name,
        quantity=quantity,
        issued_by="auth-service"
    )
    
    # Validar reglas de negocio
    order.validate()
    
    # Persistir usando repositorio
    created_order = repository.create(order)
    
    logger.info(
        "Orden creada: id=%s user_id=%s skill_name=%s",
        created_order.id,
        created_order.user_id,
        created_order.skill_name
    )
    
    return created_order
```

### 4. `persistence/repository_impl.py`
```python
from sqlalchemy.orm import Session
from ..repositories.order_repository import OrderRepository
from ..domain.entities import Order
from .models import Order as OrderModel
from .schemas import OrderCreate

class OrderRepositoryImpl(OrderRepository):
    """Implementación concreta del repositorio."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, order: Order) -> Order:
        """Crear orden en PostgreSQL."""
        db_order = OrderModel(
            user_id=order.user_id,
            skill_name=order.skill_name,
            quantity=order.quantity,
            issued_by=order.issued_by
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return self._to_entity(db_order)
    
    def _to_entity(self, model: OrderModel) -> Order:
        """Convierte modelo ORM a entidad de dominio."""
        return Order(
            id=model.id,
            user_id=model.user_id,
            skill_name=model.skill_name,
            quantity=model.quantity,
            issued_by=model.issued_by,
            created_at=model.created_at
        )
```

### 5. `handlers/order_handler.py`
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import order_service
from ..persistence.repository_impl import OrderRepositoryImpl
from ..persistence.schemas import OrderCreate, OrderResponse

router = APIRouter(tags=["Órdenes"])

@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """Endpoint para crear una orden."""
    
    # Inyectar dependencias
    repository = OrderRepositoryImpl(db)
    
    # Llamar al caso de uso
    created_order = order_service.create_order(
        repository=repository,
        user_id=order.user_id,
        skill_name=order.skill_name,
        quantity=order.quantity
    )
    
    return created_order
```

---

## Aplicar en ambos servicios

### Para `services/orders`:
- Carpetas: `handlers/`, `services/`, `domain/`, `repositories/`, `persistence/`
- Entidades: `Order` con campos (id, user_id, skill_name, quantity, created_at)

### Para `services/notifications`:
- Carpetas: `handlers/`, `services/`, `domain/`, `repositories/`, `persistence/`
- Entidades: `Notification` con campos (id, user_id, order_id, title, description, created_at)
- Extras: `services/` también contiene `email_service.py` para envío de correos

---

## Testing con esta arquitectura

```python
# tests/services/test_order_service.py
from unittest.mock import Mock
from services.order_service import create_order
from domain.entities import Order

def test_create_order():
    """Test del caso de uso sin tocar la BD."""
    
    # Mock del repositorio
    mock_repo = Mock()
    mock_repo.create.return_value = Order(
        id=1,
        user_id=5,
        skill_name="Liderazgo",
        quantity=2,
        issued_by="auth-service"
    )
    
    # Ejecutar caso de uso
    result = create_order(
        repository=mock_repo,
        user_id=5,
        skill_name="Liderazgo",
        quantity=2
    )
    
    # Verificar
    assert result.id == 1
    assert result.user_id == 5
    mock_repo.create.assert_called_once()
```

---

## Resumen

Esta arquitectura en capas limpias:
- Mantiene la **lógica de negocio independiente** de frameworks y BD
- Facilita **testing unitario** sin dependencias externas
- Permite **cambiar de BD fácilmente** (de PostgreSQL a MongoDB)
- Sigue patrones de **software limpio** y **SOLID**
- Es **práctica y escalable** para FastAPI
