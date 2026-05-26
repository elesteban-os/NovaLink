# Índice de Contenidos Completo

## 📑 Estructura de Documentación

```
events-broker/agents-doc/
├── README.md                        [PUNTO DE ENTRADA - Empieza aquí]
├── INDEX.md                         [Este archivo - Tabla de contenidos]
├── 01-API_SPECIFICATION.md          [Especificación técnica del API]
├── 02-INTEGRATION_PLAN.md           [Plan detallado de integración]
├── 03-SERVICE_TEMPLATES.md          [Código copy-paste por servicio]
├── 04-QUICK_REFERENCE.md            [Diagramas y tablas de referencia]
└── 05-GUIDE_FOR_AGENTS.md           [Instrucciones para agentes de IA]
```

---

## 🗺️ Mapa de Navegación

### Busco... → Documento → Sección

#### Entender el Concepto
- **"¿Cómo funciona RabbitMQ en NovaLink?"** → 01-API_SPECIFICATION → "Overview"
- **"¿Qué es un Exchange y Routing Key?"** → 01-API_SPECIFICATION → "Topología de Mensajería"
- **"¿Cuál es el flujo de mensajes?"** → 04-QUICK_REFERENCE → "Flujo de Eventos - Diagrama"
- **"¿Cómo se configura la conexión?"** → 01-API_SPECIFICATION → "Configuración de Conexión"

#### Planificar la Integración
- **"¿Cuál es el plan general?"** → 02-INTEGRATION_PLAN → "Plan Paso a Paso"
- **"¿Cuántas fases hay?"** → 02-INTEGRATION_PLAN → "Fase 1-7"
- **"¿Cuál es el orden recomendado?"** → 05-GUIDE_FOR_AGENTS → "Orden Recomendado de Implementación"
- **"¿Qué servicios necesito modificar?"** → 02-INTEGRATION_PLAN → "Arquitectura"

#### Implementar un Servicio
- **"¿Qué debo hacer para Orders?"** → 05-GUIDE_FOR_AGENTS → "Para ORDERS"
- **"¿Qué debo hacer para Skills?"** → 05-GUIDE_FOR_AGENTS → "Para SKILLS"
- **"¿Qué debo hacer para Users?"** → 05-GUIDE_FOR_AGENTS → "Para USERS"
- **"¿Qué debo hacer para Notifications?"** → 05-GUIDE_FOR_AGENTS → "Para NOTIFICATIONS"
- **"Necesito código copy-paste"** → 03-SERVICE_TEMPLATES → "Template 1-4"

#### Resolver Problemas
- **"El consumer no recibe mensajes"** → 04-QUICK_REFERENCE → "Señales de Error Comunes"
- **"No puedo conectarme a RabbitMQ"** → 05-GUIDE_FOR_AGENTS → "Troubleshooting para Agentes"
- **"¿Cómo manejo excepciones?"** → 04-QUICK_REFERENCE → "Checklist de Configuración"
- **"¿Qué hacer si algo no funciona?"** → README → "Troubleshooting"

#### Referencia Rápida
- **"¿Cuál es el nombre del exchange?"** → 04-QUICK_REFERENCE → "Matriz de Conexiones"
- **"¿Cuál es el payload de cada evento?"** → 04-QUICK_REFERENCE → "Estructura de Datos"
- **"¿Qué funciones debo usar?"** → 01-API_SPECIFICATION → "API de Publicación/Consumo"
- **"Necesito un checklist"** → 04-QUICK_REFERENCE → "Checklist de Configuración"

---

## 📊 Documentos por Rol

### 🤖 Agente de IA / Desarrollador Automatizado

**Lectura obligatoria (orden):**
1. [README.md](README.md) - Overview general (2 min)
2. [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) - Guía completa (20 min)
3. [03-SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) - Código para tu servicio (10 min)
4. [04-QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) - Referencia según necesites (5 min)

**Referencia rápida:**
- Árbol de decisión en [05-GUIDE_FOR_AGENTS.md#-árbol-de-decisión](05-GUIDE_FOR_AGENTS.md)
- Checklists en [04-QUICK_REFERENCE.md#-checklist-de-configuración-por-servicio](04-QUICK_REFERENCE.md)

**Documentos opcionales:**
- [01-API_SPECIFICATION.md](01-API_SPECIFICATION.md) - Para entender detalles
- [02-INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) - Para contexto estratégico

---

### 👨‍💼 Tech Lead / Arquitecto

**Lectura obligatoria (orden):**
1. [README.md](README.md) - Overview (2 min)
2. [02-INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) - Plan completo (20 min)
3. [01-API_SPECIFICATION.md](01-API_SPECIFICATION.md) - Detalles técnicos (15 min)
4. [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) - Decisiones de diseño (10 min)

**Referencia rápida:**
- Checklist de implementación en [02-INTEGRATION_PLAN.md#checklist-de-implementación](02-INTEGRATION_PLAN.md)
- Diagrama en [04-QUICK_REFERENCE.md#-flujo-de-eventos---diagrama](04-QUICK_REFERENCE.md)

**Documentos opcionales:**
- [03-SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) - Para code review
- [04-QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) - Para referencia rápida

---

### 👨‍💻 Desarrollador Manual

**Lectura obligatoria (orden):**
1. [README.md](README.md) - Overview (2 min)
2. [01-API_SPECIFICATION.md](01-API_SPECIFICATION.md) - API details (15 min)
3. [03-SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) - Código (15 min)
4. [04-QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) - Referencia (5 min)

**Referencia rápida:**
- Tabla de servicios en [04-QUICK_REFERENCE.md#-tabla-de-referencia-rápida-por-servicio](04-QUICK_REFERENCE.md)
- Configuración en [01-API_SPECIFICATION.md#configuración-de-conexión](01-API_SPECIFICATION.md)

**Documentos opcionales:**
- [02-INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) - Para contexto
- [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) - Para troubleshooting

---

### ✅ QA / Tester

**Lectura obligatoria (orden):**
1. [README.md](README.md) - Overview (2 min)
2. [04-QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) - Testing checklist (10 min)
3. [02-INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) - Sección "Pruebas" (10 min)

**Referencia rápida:**
- Checklist en [04-QUICK_REFERENCE.md#-testing-checklist](04-QUICK_REFERENCE.md)
- Señales de error en [04-QUICK_REFERENCE.md#-señales-de-error-comunes](04-QUICK_REFERENCE.md)

**Documentos opcionales:**
- [01-API_SPECIFICATION.md](01-API_SPECIFICATION.md) - Para entender errores
- [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) - Para validación de éxito

---

## 🔍 Búsqueda por Tema

### Temas Técnicos

#### RabbitMQ y Exchange
- Configuración → [01-API_SPECIFICATION.md#configuración-de-conexión](01-API_SPECIFICATION.md)
- Topología → [01-API_SPECIFICATION.md#topología-de-mensajería](01-API_SPECIFICATION.md)
- Diagrama → [04-QUICK_REFERENCE.md#-flujo-de-eventos---diagrama](04-QUICK_REFERENCE.md)

#### API Functions
- publish_event() → [01-API_SPECIFICATION.md#-publish_eventrouting_key-str-payload-dict](01-API_SPECIFICATION.md)
- consume_forever() → [01-API_SPECIFICATION.md#-consume_foreverqueue_name-routing_key-handler](01-API_SPECIFICATION.md)
- consume_once() → [01-API_SPECIFICATION.md#-consume_oncequeue_name-routing_key-handler](01-API_SPECIFICATION.md)

#### Payloads
- pedido.creado → [04-QUICK_REFERENCE.md#event-pedidocreado](04-QUICK_REFERENCE.md)
- inventario.confirmado → [04-QUICK_REFERENCE.md#event-inventarioconfirmado](04-QUICK_REFERENCE.md)
- usuario.actualizado → [04-QUICK_REFERENCE.md#event-usuarioactualizado](04-QUICK_REFERENCE.md)

### Temas de Implementación

#### Orders Service
- Plan → [02-INTEGRATION_PLAN.md#fase-2-servicio-orders-productor-inicial](02-INTEGRATION_PLAN.md)
- Guía → [05-GUIDE_FOR_AGENTS.md#para-orders](05-GUIDE_FOR_AGENTS.md)
- Código → [03-SERVICE_TEMPLATES.md#template-1-orders-service-productor](03-SERVICE_TEMPLATES.md)
- Referencia → [04-QUICK_REFERENCE.md#orders-service](04-QUICK_REFERENCE.md)

#### Skills Service
- Plan → [02-INTEGRATION_PLAN.md#fase-3-servicio-skills-consumidor--productor](02-INTEGRATION_PLAN.md)
- Guía → [05-GUIDE_FOR_AGENTS.md#para-skills](05-GUIDE_FOR_AGENTS.md)
- Código → [03-SERVICE_TEMPLATES.md#template-2-skills-service-consumidor--productor](03-SERVICE_TEMPLATES.md)
- Referencia → [04-QUICK_REFERENCE.md#skills-service](04-QUICK_REFERENCE.md)

#### Users Service
- Plan → [02-INTEGRATION_PLAN.md#fase-4-servicio-users-consumidor--productor](02-INTEGRATION_PLAN.md)
- Guía → [05-GUIDE_FOR_AGENTS.md#para-users](05-GUIDE_FOR_AGENTS.md)
- Código → [03-SERVICE_TEMPLATES.md#template-3-users-service-consumidor--productor](03-SERVICE_TEMPLATES.md)
- Referencia → [04-QUICK_REFERENCE.md#users-service](04-QUICK_REFERENCE.md)

#### Notifications Service
- Plan → [02-INTEGRATION_PLAN.md#fase-5-servicio-notifications-consumidor](02-INTEGRATION_PLAN.md)
- Guía → [05-GUIDE_FOR_AGENTS.md#para-notifications](05-GUIDE_FOR_AGENTS.md)
- Código → [03-SERVICE_TEMPLATES.md#template-4-notifications-service-consumidor](03-SERVICE_TEMPLATES.md)
- Referencia → [04-QUICK_REFERENCE.md#notifications-service](04-QUICK_REFERENCE.md)

### Temas de Configuración

#### Docker Compose
- Plan → [02-INTEGRATION_PLAN.md#fase-6-configuración-de-docker-compose](02-INTEGRATION_PLAN.md)
- Ejemplo → [02-INTEGRATION_PLAN.md#61-agregar-rabbitmq-al-docker-compose](02-INTEGRATION_PLAN.md)

#### Variables de Entorno
- Configuración → [01-API_SPECIFICATION.md#variables-de-entorno](01-API_SPECIFICATION.md)
- Matriz → [04-QUICK_REFERENCE.md#-configuración-de-conexión---variables](04-QUICK_REFERENCE.md)

#### Requirements.txt
- Qué agregar → [02-INTEGRATION_PLAN.md#11-instalar-dependencia](02-INTEGRATION_PLAN.md)
- Rápido → [03-SERVICE_TEMPLATES.md#1-agregar-pika-a-requirementstxt](03-SERVICE_TEMPLATES.md)

### Temas de Testing

#### Flujo Completo
- Testing → [02-INTEGRATION_PLAN.md#pruebas](02-INTEGRATION_PLAN.md)
- Checklist → [04-QUICK_REFERENCE.md#-testing-checklist](04-QUICK_REFERENCE.md)

#### Troubleshooting
- Errores comunes → [04-QUICK_REFERENCE.md#-señales-de-error-comunes](04-QUICK_REFERENCE.md)
- Problemas → [05-GUIDE_FOR_AGENTS.md#-troubleshooting-para-agentes](05-GUIDE_FOR_AGENTS.md)
- General → [README.md#-troubleshooting](README.md)

---

## 📈 Progreso de Lectura

### Si tienes 5 minutos
→ Lee [README.md](README.md) completo

### Si tienes 15 minutos
→ Lee [README.md](README.md) + [04-QUICK_REFERENCE.md#-flujo-de-eventos---diagrama](04-QUICK_REFERENCE.md) (solo diagrama)

### Si tienes 30 minutos
→ Lee [README.md](README.md) + [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md)

### Si tienes 1 hora
→ Lee [README.md](README.md) + [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) + [03-SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md)

### Si tienes 2 horas
→ Lee todo menos [02-INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) (detalles por fase)

### Si tienes tiempo ilimitado
→ Lee todo en orden: README → 05 → 03 → 04 → 02 → 01

---

## 🎯 Decisiones Rápidas

### ¿Por dónde empiezo?
→ [README.md](README.md) → Encuentra tu rol en "Flujo de Lectura Recomendado"

### ¿Cuál es mi siguiente documento?
→ Este INDEX.md

### ¿Necesito código?
→ [03-SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md)

### ¿Necesito entender la arquitectura?
→ [02-INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md)

### ¿Necesito detalles técnicos?
→ [01-API_SPECIFICATION.md](01-API_SPECIFICATION.md)

### ¿Necesito referencia rápida?
→ [04-QUICK_REFERENCE.md](04-QUICK_REFERENCE.md)

### ¿Soy un agente de IA?
→ [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md)

---

## 📝 Resumen de Archivos

| Archivo | Tamaño | Público | Tiempo |
|---------|--------|--------|--------|
| [README.md](README.md) | Medio | Todos | 5 min |
| [01-API_SPECIFICATION.md](01-API_SPECIFICATION.md) | Grande | Técnico | 15 min |
| [02-INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) | Muy Grande | Tech Lead | 25 min |
| [03-SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) | Muy Grande | Desarrollador | 10-30 min* |
| [04-QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) | Grande | Todos | 10 min |
| [05-GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) | Grande | Agentes/Dev | 20 min |

*Depende de cuántos servicios implementes

---

## 🔗 Enlaces Cruzados

### Desde README
- → [GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) (Recomendado para agentes)
- → [SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) (Código)
- → [QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) (Tablas)

### Desde GUIDE_FOR_AGENTS
- → [SERVICE_TEMPLATES.md](03-SERVICE_TEMPLATES.md) (Código específico)
- → [QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) (Validación)
- → [API_SPECIFICATION.md](01-API_SPECIFICATION.md) (Detalles)

### Desde SERVICE_TEMPLATES
- → [QUICK_REFERENCE.md](04-QUICK_REFERENCE.md) (Payloads)
- → [API_SPECIFICATION.md](01-API_SPECIFICATION.md) (Funciones)
- → [GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) (Troubleshooting)

### Desde QUICK_REFERENCE
- → [API_SPECIFICATION.md](01-API_SPECIFICATION.md) (Detalles)
- → [INTEGRATION_PLAN.md](02-INTEGRATION_PLAN.md) (Testing)
- → [GUIDE_FOR_AGENTS.md](05-GUIDE_FOR_AGENTS.md) (Troubleshooting)

---

## ✅ Checklist: ¿Leí lo que necesitaba?

- [ ] Leí un documento de introducción (README)
- [ ] Leí un documento para mi rol específico
- [ ] Tengo código copy-paste disponible (SERVICE_TEMPLATES)
- [ ] Tengo tablas de referencia (QUICK_REFERENCE)
- [ ] Sé dónde encontrar información técnica (API_SPECIFICATION)
- [ ] Sé dónde encontrar el plan completo (INTEGRATION_PLAN)
- [ ] Sé a dónde volver si tengo dudas (Este INDEX)

---

**Última actualización:** 24 de mayo de 2026
