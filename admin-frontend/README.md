# Admin Frontend - Habilidades Sociales

Frontend simplificado para la gestión de Habilidades Sociales en NovaLink.

## Características

- ✅ Autenticación básica (login)
- ✅ Dashboard con estadísticas
- ✅ **Catálogo de habilidades tipo marketplace**
- ✅ **Sistema de "compra" de habilidades**
- ✅ Perfil de usuario
- ✅ Historial de habilidades adquiridas
- ✅ Estado responsivo
- ✅ Datos mockados para demostración

## Estructura

```
admin-frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── LoginForm.jsx
│   │   └── *.css
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Users.jsx
│   │   ├── Skills.jsx
│   │   ├── Orders.jsx
│   │   └── *.css
│   ├── api/
│   │   └── axiosConfig.js
│   ├── data/
│   │   └── mockData.js
│   ├── styles/
│   │   ├── index.css
│   │   └── App.css
│   ├── App.js
│   └── index.js
└── package.json
```

## Instalación

1. **Navega a la carpeta del frontend:**
   ```bash
   cd admin-frontend
   ```

2. **Instala las dependencias:**
   ```bash
   npm install
   ```

3. **Inicia el servidor de desarrollo:**
   ```bash
   npm start
   ```

4. **Accede a la aplicación:**
   Abre [http://localhost:3001](http://localhost:3001) en tu navegador.

## Login

Por defecto, la aplicación acepta cualquier correo y contraseña en modo demo:
- **Email:** cualquier email
- **Contraseña:** cualquier contraseña

## Datos de Demostración

### Usuarios Predeterminados
- Juan García (Estudiante)
- María López (Estudiante)
- Carlos Rodríguez (Instructor)

### Habilidades Disponibles (15)
Empatía, Liderazgo, Comunicación Asertiva, Escucha Activa, Creatividad, Resiliencia, Colaboración, Paciencia, Confianza, Adaptabilidad, Iniciativa, Amistad, Humor, Respeto, Sagacidad.

## Funcionalidades

### Dashboard
- Estadísticas de usuarios, habilidades, pedidos
- Últimos pedidos registrados

### Catálogo de Habilidades
- **Interfaz tipo tienda/marketplace** con tarjetas atractivas
- 15 habilidades sociales disponibles (Empatía, Liderazgo, Creatividad, etc.)
- Sistema de "compra" simple con modal de confirmación
- Indicadores de dificultad por colores
- Puntos de experiencia (XP) por cada habilidad

### Mi Perfil
- Ver y editar información personal
- Contador de habilidades adquiridas

### Mis Habilidades Adquiridas
- Lista de habilidades que has adquirido
- Puntos XP ganados por cada habilidad
- Estado de adquisición (Completado/En progreso)
- Filtro por estado
- Filtrar por estado
- Eliminar pedidos

## Tecnologías

- **React** - Librería de UI
- **React Router** - Enrutamiento
- **Axios** - Cliente HTTP
- **CSS3** - Estilos

## Variables de Entorno

```env
REACT_APP_API_URL=http://localhost:3001/api
```

## Build para Producción

```bash
npm run build
```

Esto creará una carpeta `build/` optimizada lista para desplegar.

## Notas de Desarrollo

- Los datos están mockados en `src/data/mockData.js`
- La configuración de Axios está en `src/api/axiosConfig.js`
- El CSS está modularizado por página/componente
- No incluye Tailwind CSS, usa CSS vanilla para simplicidad

## Próximos Pasos

1. Conectar con APIs reales del backend
2. Agregar autenticación JWT
3. Implementar paginación en tablas
4. Agregar validaciones más robustas
5. Mejorar UX con notificaciones

---

**Creado para el proyecto:** Ecosistema de Servicios RESTful para Gestión de Habilidades Sociales
