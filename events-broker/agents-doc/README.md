# Event Broker - Guía de Integración para Agentes

## 📋 Descripción General

Este directorio contiene la documentación completa para integrar el **Event Broker de RabbitMQ** con los servicios reales de NovaLink.

**Situación actual:**
- El directorio `events-broker/` contiene **mockups** de servicios para demostrar el patrón
- Los servicios **reales** están en `services/` (orders, skills, users, notifications)
- Necesitamos conectar los servicios reales al broker sin perder su funcionalidad existente

---

## 📚 Documentos Disponibles

### 0. [🤖 GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) ⭐ EMPIEZA AQUÍ

**Este es el documento para desarrolladores que van a implementar**

- ✅ Árbol de decisión por servicio
- ✅ Proceso paso a paso para cada servicio
- ✅ Adaptaciones comunes y troubleshooting
- ✅ Orden recomendado de implementación
- ✅ Validación de éxito

**Público:** Desarrolladores, Agentes de IA

**Duración de lectura:** 20 minutos

---

### 1. [📖 API_SPECIFICATION.md](01-API_SPECIFICATION.md)

**Lee esto para entender:**
- ✅ Cómo funciona el API del Event Broker
- ✅ Configuración de conexión (variables de entorno)
- ✅ Topología de mensajería (Exchange, Routing Keys, Colas)
- ✅ Funciones de publicación y consumo
- ✅ Estructura de payloads de cada evento
- ✅ Manejo de errores y startup

**Público:** Todos

**Duración de lectura:** 15 minutos

---

### 2. [🛠️ INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md)

**Lee esto para:**
- ✅ Entender la estrategia de integración
- ✅ Ver la arquitectura final de carpetas
- ✅ Seguir paso a paso cómo integrar cada servicio
- ✅ Verificar el checklist de implementación
- ✅ Ejecutar pruebas end-to-end

**Público:** Desarrolladores, Tech Leads

**Duración de lectura:** 20 minutos

**Estructura de secciones:**
1. Contexto del problema
2. Enfoque de integración (no reescribir, inyectar)
3. Arquitectura final
4. Plan paso a paso (7 fases)
5. Checklist
6. Pruebas

---

### 3. [💻 SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md)

**Lee esto para:**
- ✅ Obtener código copy-paste listo para usar
- ✅ Ver las plantillas para cada servicio (Orders, Skills, Users, Notifications)
- ✅ Entender qué modificar en cada archivo
- ✅ Ejecutar instalación rápida

**Público:** Desarrolladores implementadores

**Duración de lectura:** 10 minutos (consulta según necesites)

**Estructura:**
- Template 1: Orders (Productor)
- Template 2: Skills (Consumidor → Productor)
- Template 3: Users (Consumidor → Productor)
- Template 4: Notifications (Consumidor)
- Checklists por servicio
- Instalación rápida

---

### 4. [🔍 QUICK_REFERENCE.md](04-QUICK_REFERENCE.md)

**Lee esto para:**
- ✅ Diagrama visual del flujo de eventos
- ✅ Matriz de decisión rápida
- ✅ Tablas de referencia por servicio
- ✅ Estructura de datos (payloads JSON)
- ✅ Señales de error comunes
- ✅ Checklist de configuración

**Público:** Consultores, QA, Tech Leads

**Duración de lectura:** 10 minutos

---

### 5. [🤖 GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md)

**Lee esto para:**
- ✅ Instrucciones específicas para agentes de IA
- ✅ Árbol de decisión automático
- ✅ Adaptaciones y troubleshooting
- ✅ Validación de éxito

**Público:** Agentes de IA, Desarrolladores

**Duración de lectura:** 15 minutos

---

## 🎯 Flujo de Lectura Recomendado

### 🤖 Rol: Agente de IA / Desarrollador que va a implementar

**EMPIEZA AQUÍ:**
1. Lee: [GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) - Completo (20 min)
2. Elige: Tu servicio usando el árbol de decisión
3. Lee: [SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) - Template para tu servicio (10 min)
4. Consulta: [QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) - Según necesites (5 min)
5. Implementa: Usa el código de plantilla y adapta
6. Valida: Sigue checklist de "Validación de Éxito"

**Tiempo total:** 1-2 horas para completar integración de 1 servicio

---

### 👨‍💼 Rol: Tech Lead / Planificador

1. Lee: [INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) - Completo (20 min)
2. Revisa: Checklist de implementación general
3. Planifica: Fases según capacidad del equipo
4. Asigna: Tareas a desarrolladores
5. Verifica: Progreso con checklist

**Tiempo:** 30 minutos

---

### 👨‍💻 Rol: Desarrollador (Manual, sin IA)

1. Lee: [API_SPECIFICATION.md](01-API_SPECIFICATION.md) - Secciones de API (15 min)
2. Lee: [SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) - Template del servicio (10 min)
3. Lee: [QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) - Tablas de referencia (5 min)
4. Copia: Código de plantilla
5. Modifica: Según tu servicio real
6. Prueba: Localmente con docker-compose

**Tiempo:** 30-45 minutos por servicio

---

### 🏗️ Rol: Architecto / Tech Review

1. Lee: [INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) - Arquitectura (15 min)
2. Lee: [API_SPECIFICATION.md](01-API_SPECIFICATION.md) - Detalles técnicos (15 min)
3. Revisa: Decisiones de diseño en [GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) (10 min)
4. Valida: Cumplimiento de estándares

**Tiempo:** 40 minutos

---

### ✅ Rol: QA / Tester

1. Lee: [QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) - Sección "Testing Checklist" (10 min)
2. Lee: [INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) - Sección "Pruebas" (10 min)
3. Ejecuta: Procedimiento de pruebas end-to-end
4. Verifica: Panel RabbitMQ, logs, flujo completo

**Tiempo:** 20 minutos por ejecución

---

## 🔑 Conceptos Clave

### Exchange (Intercambiador)
```
Nombre: novalink.events
Tipo: direct (enruta por routing key exacta)
Durable: true (sobrevive reinicio del broker)
```

### Routing Keys (Eventos)
```
pedido.creado              → Orders publica, Skills consume
inventario.confirmado      → Skills publica, Users consume
usuario.actualizado        → Users publica, Notifications consume
```

### Colas
```
inventario.pedido.creado           ← consume Skills
usuarios.inventario.confirmado     ← consume Users
notificaciones.usuario.actualizado ← consume Notifications
```

### API Functions
```
publish_event(routing_key, payload)         → Publica un evento
consume_forever(queue, routing_key, handler) → Consume indefinidamente
consume_once(queue, routing_key, handler)   → Consume 1 mensaje si hay
```

---

## ⚡ Quick Start

### 1. Instalar Dependencia
```bash
pip install pika
```

### 2. Levantar RabbitMQ
```bash
docker compose -f events-broker/docker-compose.yml up -d
```

### 3. Verificar Conectividad
```bash
# Panel de control
http://localhost:15672 (guest/guest)
```

### 4. Probar Flujo de Ejemplo
```bash
# Terminal 1
python events-broker/services/skills/skills.py run

# Terminal 2
python events-broker/services/users/users.py run

# Terminal 3
python events-broker/services/notifications/notifications.py run

# Terminal 4
python events-broker/services/orders/orders.py publish
```

**Resultado esperado:**
```
[orders] published pedido.creado: {...}
[inventario] received pedido.creado: {...}
[inventario] published inventario.confirmado: {...}
[usuarios] received inventario.confirmado: {...}
[usuarios] published usuario.actualizado: {...}
[notificaciones] received usuario.actualizado: {...}
[notificaciones] confirmation log: ...
```

---

## 🗺️ Mapa de Archivos

```
events-broker/
├── agents-doc/                    ← TÚ ESTÁS AQUÍ
│   ├── README.md (este archivo)
│   ├── 01-API_SPECIFICATION.md
│   ├── 02-INTEGRATION_PLAN.md
│   └── 03-SERVICE_TEMPLATES.md
│
├──⚡ Guía Rápida: 5 Minutos

### Para Entender Rápido
```bash
# 1. Levantar broker
docker compose -f events-broker/docker-compose.yml up -d

# 2. Probar flujo de mockups
python events-broker/services/skills/skills.py once &
python events-broker/services/users/users.py once &
python events-broker/services/notifications/notifications.py once &
python events-broker/services/orders/orders.py publish

# Verifica en terminal que el flujo completa sin errores
```

### Para Implementar Ahora
1. **Si eres agente de IA:** Lee [GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md)
2. **Si eres desarrollador:** Lee [SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md)
3. **Si necesitas referencia:** Lee [QUICK_REFERENCE.md](04-QUICK_REFERENCE.md)

---

## ✅ Checklist Pre-Integración

Antes de empezar, verifica:

- [ ] RabbitMQ está levantado: `docker compose -f events-broker/docker-compose.yml up -d`
- [ ] Panel accesible: `http://localhost:15672` (guest/guest)
- [ ] Prueba de mockups exitosa: `python events-broker/services/orders/orders.py publish`
- [ ] Tienes acceso a los servicios reales en `services/`
- [ ] Python 3.10+ instalado
- [ ] `pika` disponible: `pip install pika`
- [ ] Leíste la guía para tu rol (ver "Flujo de Lectura Recomendado")
├── requirements.txt
└── docs/
    └── README.md

services/  (SERVICIOS REALES - necesitan integración)
├── orders/
├── skills/
├── users/
└── notifications/
```

---

## ✅ Checklist Pre-Integración

Antes de empezar, verifica:

- [ ] RabbitMQ está levantado: `docker compose -f events-broker/docker-compose.yml up -d`
- [ ] Panel accesible: `http://localhost:15672` (guest/guest)
- [ ] Prueba de mockups exitosa: `python events-broker/services/orders/orders.py publish`
- [ ] Tienes acceso a los servicios reales en `services/`
- [ ] Python 3.10+ instalado
- [ ] `pika` disponible: `pip install pika`

---

## 🐛 Troubleshooting

### Problema: "Could not connect to RabbitMQ"

**Solución:**
```bash
docker compose -f events-broker/docker-compose.yml up -d
```

### Problema: "Missing dependency: install pika"

**Solución:**
```bash
pip install pika
```

### Problema: Mensajes no aparecen en RabbitMQ

**Verificación:**
1. Asegúrate que el publisher está ejecutándose
2. Revisa que el exchange existe: RabbitMQ UI → Exchanges
3. Revisa que la cola está bindada: RabbitMQ UI → Queues
4. Chequea que el routing_key coincide

### Problema: Consumer no recibe mensajes

**Verificación:**
1. El consumer debe estar corriendo ANTES de publicar
2. Verifica el nombre de la cola: `QUEUE_INVENTORY`, `QUEUE_USERS`, `QUEUE_NOTIFICATIONS`
3. Verifica el routing_key: `ROUTING_KEY_ORDER_CREATED`, etc.

---

## 📞 Guía por Servicio

| Servicio | Rol | Documento | Template |
|----------|-----|-----------|----------|
| **orders** | Productor inicial | [INTEGRATION_PLAN.md#Fase 2](02-INTEGRATION_PLAN.md) | [SERVICE_TEMPLATES.md#Template 1](03-SERVICE_TEMPLATES.md) |
| **skills** | Consumidor → Productor | [INTEGRATION_PLAN.md#Fase 3](02-INTEGRATION_PLAN.md) | [SERVICE_TEMPLATES.md#Template 2](03-SERVICE_TEMPLATES.md) |
| **users** | Consumidor → Productor | [INTEGRATION_PLAN.md#Fase 4](02-INTEGRATION_PLAN.md) | [SERVICE_TEMPLATES.md#Template 3](03-SERVICE_TEMPLATES.md) |
| **notifications** | Consumidor final | [INTEGRATION_PLAN.md#Fase 5](02-INTEGRATION_PLAN.md) | [SERVICE_TEMPLATES.md#Template 4](03-SERVICE_TEMPLATES.md) |

---

## 📖 Referencias

### Documentación Oficial
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Pika Python Client](https://pika.readthedocs.io/)

### En este repositorio
- [ADR-0001: Microservices Architecture](../../documentation/adr/ADR-0001-microservices-architecture.md)
- [Event Broker README](../docs/README.md)
- [Mockup Services](../services/)

---

## 🎓 Notas Educativas

### ¿Por qué Direct Exchange?
- Cada servicio consume un routing key específico
- No necesitamos fanout (broadcast)
- Mejor control y predicibilidad

### ¿Por qué durable=true?
- Los mensajes persisten si el broker se reinicia
- Garantiza entrega durante testing local

### ¿Por qué prefetch_count=1?
- Evita que un consumer tome múltiples mensajes
- Permite rebalanceo dinámico si hay múltiples replicas

### ¿Por qué daemon=true en threads?
- Los threads de consumer se cierran cuando FastAPI se detiene
- No bloquea el shutdown del servicio

---

## 🚀 Próximos Pasos

1. **Lee** [API_SPECIFICATION.md](01-API_SPECIFICATION.md)
2. **Revisa** la topología en RabbitMQ UI
3. **Prueba** el flujo de mockups
4. **Sigue** [INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md)
5. **Implementa** usando [SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md)
6. **Verifica** con pruebas end-to-end

---

**Última actualización:** 24 de mayo de 2026

**Mantenimiento:** Este directorio es la fuente única de verdad para integración de Event Broker. Actualiza estos documentos cuando:
- Cambies la topología de mensajería
- Agregues nuevos eventos
- Modifiques el API del broker
- Descubras patrones de error comunes
