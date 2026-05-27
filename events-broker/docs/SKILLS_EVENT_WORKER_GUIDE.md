# Guía: Autenticación y Prueba del Event Worker de Skills

Esta guía te muestra cómo **obtener un token JWT**, **crear órdenes** y **verificar cómo el event worker de skills procesa los eventos**.

## Credenciales válidas

El servicio `users` incluye un seed con los siguientes usuarios listos para usar:

| Email | Password | Rol |
|-------|----------|-----|
| `juan.perez@admin.com` | `password123` | Admin |
| `ana.garcia@admin.com` | `password123` | Admin |
| `carlos.lopez@user.com` | `password123` | User |
| `maria.rodriguez@user.com` | `password123` | User |

**Usa cualquiera de estos emails en los pasos de autenticación.**

## 1. Preparación: Levantar los servicios

Desde la carpeta raíz `NovaLink`, levanta los servicios necesarios en orden:

### Paso 1a: Levanta RabbitMQ (el broker de mensajes)

```bash
docker compose -f events-broker/docker-compose.yml up -d
```

### Paso 1b: Levanta el servicio de autenticación

```bash
docker compose -f services/auth/docker-compose.yml up -d
```

### Paso 1c: Levanta el servicio de órdenes

```bash
docker compose -f services/orders/docker-compose.yml up -d
```

### Paso 1d: Levanta el servicio de skills (con su API y worker)

```bash
docker compose -f services/skills/docker-compose.yml up -d
```

> **Nota:** Si has hecho cambios en el código, reconstruye las imágenes sin caché:
> 
> ```bash
> docker compose -f services/auth/docker-compose.yml build --no-cache
> docker compose -f services/orders/docker-compose.yml build --no-cache
> docker compose -f services/skills/docker-compose.yml build --no-cache
> ```

## 2. Obtener el token JWT

En PowerShell, ejecuta cada comando en líneas separadas:

### Paso 2a: Solicita un token al servicio de autenticación

```powershell
$body = '{"email":"juan.perez@admin.com","password":"password123"}'
$resp = Invoke-RestMethod -Method Post -Uri 'http://localhost:8007/auth/login' -ContentType 'application/json' -Body $body
```

### Paso 2b: Extrae y guarda el token en una variable

```powershell
$token = $resp.access_token
Write-Output $token
```

**Salida esperada:** Un string largo (JWT token):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiaWF0IjoxNjI3NTkwMzY0fQ...
```

---

## 3. Crear una orden con el token

### Paso 3a: Prepara los headers con el token

```powershell
$headers = @{'Content-Type' = 'application/json'; 'Authorization' = "Bearer $token"}
```

### Paso 3b: Crea la orden enviando el request

```powershell
$body = '{"skill_name":"python","quantity":2}'
$response = Invoke-RestMethod -Method Post -Uri 'http://localhost:8005/orders' -Headers $headers -Body $body
$response | ConvertTo-Json
```

**Salida esperada:**
```json
{
  "pedido_id": "order-123abc",
  "user_id": "user-456def",
  "skill_name": "python",
  "quantity": 2,
  "status": "received"
}
```

---

## 4. Monitorear al Event Worker de Skills

Mientras se procesa la orden, **en otra terminal**, observa los logs del worker de skills:

### Paso 4a: Ve los logs en tiempo real

```bash
docker compose -f services/skills/docker-compose.yml logs -f skills_worker
```

**Salida esperada en los logs:**

1. El worker **recibe** el evento `pedido.creado`:
   ```
   [inventario] received pedido.creado: {"pedido_id":"order-123abc","skill_name":"python","quantity":2,...}
   ```

2. El worker **reserva stock**:
   ```
   [inventario] Stock reservado para: python (cantidad: 2)
   ```

3. El worker **publica** el evento `inventario.confirmado`:
   ```
   [inventario] published inventario.confirmado: {"pedido_id":"order-123abc","skill_name":"python","stock_validado":true,...}
   ```

4. Si la orden tenía `request_id`, publica respuesta al gateway:
   ```
   [inventario] published gateway.skills.response: {"request_id":"...","status":"success","message":"Stock confirmado",...}
   ```

---

## 5. Flujo completo paso a paso

Si quieres ver el flujo **completo**, levanta los workers de todos los servicios:

### Paso 5a: Levanta el worker de usuarios y notificaciones

```bash
docker compose -f services/users/docker-compose.yml up -d
docker compose -f services/notifications/docker-compose.yml up -d
```

### Paso 5b: Crea una orden (como en el paso 3)

```powershell
$headers = @{'Content-Type' = 'application/json'; 'Authorization' = "Bearer $token"}
$body = '{"skill_name":"python","quantity":1}'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8005/orders' -Headers $headers -Body $body
```

### Paso 5c: Observa el flujo en múltiples terminales

Abre 4 terminales y monitorea cada worker:

**Terminal 1: Skills**
```bash
docker compose -f services/skills/docker-compose.yml logs -f skills_worker
```

**Terminal 2: Usuarios**
```bash
docker compose -f services/users/docker-compose.yml logs -f users_worker
```

**Terminal 3: Notificaciones**
```bash
docker compose -f services/notifications/docker-compose.yml logs -f notifications_worker
```

**Terminal 4: Órdenes (opcional, para ver logs de la API)**
```bash
docker compose -f services/orders/docker-compose.yml logs -f orders_api
```

### Resultado esperado:
1. ✅ `orders_api` crea la orden
2. ✅ `skills_worker` recibe `pedido.creado` y publica `inventario.confirmado`
3. ✅ `users_worker` recibe `inventario.confirmado` y publica `usuario.actualizado`
4. ✅ `notifications_worker` recibe `usuario.actualizado` e imprime el log final

---

## 6. Probar diferentes habilidades y cantidades

Puedes cambiar la habilidad y cantidad en cada orden:

```powershell
# Orden de JavaScript
$body = '{"skill_name":"javascript","quantity":3}'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8005/orders' -Headers $headers -Body $body

# Orden de Go
$body = '{"skill_name":"go","quantity":1}'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8005/orders' -Headers $headers -Body $body

# Orden de React
$body = '{"skill_name":"react","quantity":2}'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8005/orders' -Headers $headers -Body $body
```

---

## 7. Listar todas las habilidades disponibles

Puedes ver todas las habilidades que tienen stock:

```powershell
$headers = @{'Content-Type' = 'application/json'; 'Authorization' = "Bearer $token"}
$response = Invoke-RestMethod -Method Get -Uri 'http://localhost:8005/skills' -Headers $headers
$response | ConvertTo-Json
```

**Salida esperada:**
```json
[
  {"id":1,"name":"python","stock":10,"created_at":"2026-05-20T..."},
  {"id":2,"name":"javascript","stock":15,"created_at":"2026-05-20T..."},
  {"id":3,"name":"go","stock":5,"created_at":"2026-05-20T..."}
]
```

---

## 8. Solución de problemas

### El servicio de auth no responde (error de conexión)

Verifica que está levantado:
```bash
docker ps | findstr auth
```

Si no está, levántalo:
```bash
docker compose -f services/auth/docker-compose.yml up -d
```

### Error: "Incorrect email or password" (401 en auth)

**Causa:** Estás usando un email que no existe en el seed de usuarios.

**Solución:** Usa una de las credenciales válidas de la tabla al inicio:

```powershell
# ✅ CORRECTO - email que SÍ existe en el seed
$body = '{"email":"juan.perez@admin.com","password":"password123"}'
$resp = Invoke-RestMethod -Method Post -Uri 'http://localhost:8007/auth/login' -ContentType 'application/json' -Body $body

# ❌ INCORRECTO - email que NO existe
$body = '{"email":"test@example.com","password":"password123"}'
$resp = Invoke-RestMethod -Method Post -Uri 'http://localhost:8007/auth/login' -ContentType 'application/json' -Body $body
```

Verifica que el servicio `users` ejecutó el seed al iniciar. Revisa los logs:
```bash
docker compose -f services/users/docker-compose.yml logs users_api | findstr seed
```

Si ves un error en el seed, reinicia el servicio:
```bash
docker compose -f services/users/docker-compose.yml down
docker compose -f services/users/docker-compose.yml up -d
```

### El token es inválido (401 en la orden)

Asegúrate de que:
1. El token fue extraído correctamente: `Write-Output $token`
2. El token no tiene espacios en blanco extras
3. El token no ha expirado (se genera con TTL de ~1 hora)

Obtén uno nuevo:
```powershell
$body = '{"email":"juan.perez@admin.com","password":"password123"}'
$resp = Invoke-RestMethod -Method Post -Uri 'http://localhost:8007/auth/login' -ContentType 'application/json' -Body $body
$token = $resp.access_token
Write-Output $token
```

### RabbitMQ no está disponible

Verifica que está corriendo:
```bash
docker ps | findstr rabbitmq
```

Levántalo:
```bash
docker compose -f events-broker/docker-compose.yml up -d
```

### El worker de skills no procesa mensajes

Verifica que la red `novalink_network` existe y es compartida:
```bash
docker network ls | findstr novalink
```

Verifica que el worker está vivo:
```bash
docker compose -f services/skills/docker-compose.yml ps
```

Reinicia el worker si es necesario:
```bash
docker compose -f services/skills/docker-compose.yml restart skills_worker
```

### Ver todos los logs consolidados

```bash
docker compose -f services/skills/docker-compose.yml logs --timestamps
docker compose -f services/users/docker-compose.yml logs --timestamps
docker compose -f services/notifications/docker-compose.yml logs --timestamps
```

---

## 9. Cheat Sheet rápido

**Obtener token:**
```powershell
$body = '{"email":"juan.perez@admin.com","password":"password123"}'
$resp = Invoke-RestMethod -Method Post -Uri 'http://localhost:8007/auth/login' -ContentType 'application/json' -Body $body
$token = $resp.access_token
```

**Crear orden:**
```powershell
$headers = @{'Content-Type' = 'application/json'; 'Authorization' = "Bearer $token"}
$body = '{"skill_name":"python","quantity":2}'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8005/orders' -Headers $headers -Body $body
```

**Ver logs del worker de skills:**
```bash
docker compose -f services/skills/docker-compose.yml logs -f skills_worker
```

**Parar todos los servicios:**
```bash
docker compose -f services/auth/docker-compose.yml down
docker compose -f services/orders/docker-compose.yml down
docker compose -f services/skills/docker-compose.yml down
docker compose -f services/users/docker-compose.yml down
docker compose -f services/notifications/docker-compose.yml down
docker compose -f events-broker/docker-compose.yml down
```

---

## 10. Referencia: Estructura del Event Worker de Skills

El event worker de skills (`app/infrastructure/event_worker.py`) implementa:

### Entrada
- **Cola:** `skills_queue`
- **Eventos que consume:**
  - `pedido.creado`: cuando se crea una nueva orden
  - `skills.list`: cuando se pide listar habilidades

### Lógica de negocio
- `reserve_stock()`: valida que hay stock disponible y lo decrementa
- `get_skills()`: retorna todas las habilidades con stock

### Salida
- **`inventario.confirmado`:** si el stock fue validado correctamente
- **`inventario.rechazado`:** si no hay stock suficiente
- **`gateway.skills.response`:** respuesta al gateway si hay `request_id`
- **`gateway.skills.list.response`:** respuesta de listado de habilidades

---

## Referencia: Rutas del evento

```
[Órdenes API] 
    ↓ (POST /orders)
    ↓ publica: pedido.creado
    ↓
[RabbitMQ - Exchange: novalink]
    ↓ routing_key: pedido.creado
    ↓
[Skills Worker]
    ↓ reserva stock
    ↓ publica: inventario.confirmado
    ↓
[Usuarios Worker]
    ↓ asigna habilidad
    ↓ publica: usuario.actualizado
    ↓
[Notificaciones Worker]
    ↓ imprime log final
```
