# ADR-0006: Estrategia de versionado de imagenes y redeploy

- Status: Accepted

## Context

En entorno Kubernetes local, usar siempre :latest puede provocar redeploy ambiguo y mensajes de "unchanged" al aplicar manifiestos sin cambios de spec.

## Decision

Adoptar tags unicos para imagenes de frontend en cada redeploy y automatizar el flujo con script PowerShell.

Flujo recomendado:
1. Build con tag unico (por fecha/hora).
2. Actualizar Deployment con el tag nuevo.
3. Importar imagen al runtime del nodo local cuando aplique.
4. Ejecutar rollout status y validar pod ready.
5. Persistir tag activo en manifiesto de k8s.
