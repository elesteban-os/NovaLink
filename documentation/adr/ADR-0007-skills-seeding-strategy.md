# ADR-0007: Estrategia de seeding de skills

- Status: Accepted

## Context

El servicio skills requiere datos iniciales para pruebas funcionales inmediatas. El seed previo podia resetear la base completa.

## Decision

Ejecutar seeding en startup del servicio skills con comportamiento idempotente:
- En startup: insertar solo skills faltantes.
- Evitar duplicados por skill_name.
- Mantener opcion de reset explicito solo en ejecucion manual del seeder.

