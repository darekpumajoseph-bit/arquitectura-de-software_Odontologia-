# 🎨 Frontend OdontoSoft — Documentación

![HTML5](https://img.shields.io/badge/HTML5-Semántico-orange) ![CSS3](https://img.shields.io/badge/CSS3-Responsive-blue) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)

Interfaz web moderna, responsiva y dinámica. Comunicación centralizada con backend mediante Fetch API.

---

## 📂 Estructura

```
frontend/
├── html/                    # Vistas
│   ├── index.html          # Landing page
│   ├── login.html          # Autenticación
│   ├── registro.html       # Registro
│   ├── panel.html          # Dashboard principal
│   ├── citas.html          # Agenda
│   ├── pacientes.html      # Pacientes CRUD
│   ├── odontologos.html    # Odontólogos
│   ├── tratamientos.html   # Catálogo
│   ├── pagos.html          # Finanzas
│   └── roles.html          # Control de acceso
│
├── css/                     # Estilos
│   ├── style.css           # Estilos principales
│   ├── auth.css            # Login/registro
│   └── politicas.css       # Documentos legales
│
└── js/                      # Lógica
    ├── api.js              # Cliente HTTP centralizado
    └── auth.js             # Validación formularios
```

---

## 🎨 Componentes

- ✅ **Dashboard responsivo** — Menú lateral + contenido dinámico
- ✅ **Modales nativos** — Crear/editar registros
- ✅ **Tablas dinámicas** — Datos en tiempo real desde BD
- ✅ **Toast notifications** — Alertas flotantes (éxito/error/warning)
- ✅ **Formularios validados** — Email, contraseña, campos requeridos
- ✅ **Iconos Material Symbols** — UI moderna
- ✅ **CSS responsivo** — Mobile, tablet, desktop

---

## 🔌 API Integration (api.js)

Centraliza todos los requests HTTP:

```javascript
const API_BASE = "http://127.0.0.1:8000";

// Autenticación
async function registroUsuario(datos) {
    const resp = await fetch(`${API_BASE}/auth/registro`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    });
    return resp.json();
}

// CRUD Genérico
async function obtenerDatos(endpoint) {
    return (await fetch(`${API_BASE}/${endpoint}`)).json();
}

async function crearDato(endpoint, datos) {
    const resp = await fetch(`${API_BASE}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    });
    return resp.json();
}

async function actualizarDato(endpoint, id, datos) {
    const resp = await fetch(`${API_BASE}/${endpoint}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    });
    return resp.json();
}

async function eliminarDato(endpoint, id) {
    await fetch(`${API_BASE}/${endpoint}/${id}`, { method: "DELETE" });
}
```

---

## 📄 Vistas Principales

| Vista | Contenido |
|-------|----------|
| **index.html** | Landing page inicial |
| **login.html** | Autenticación (correo + contraseña) |
| **registro.html** | Registro (Paciente/Odontólogo) |
| **panel.html** | Dashboard con menú lateral |
| **pacientes.html** | CRUD pacientes (tabla + modal) |
| **citas.html** | Agenda de citas |
| **tratamientos.html** | Catálogo de servicios |
| **pagos.html** | Gestión de pagos y facturas |
| **roles.html** | Control de permisos |

---

## 💬 Sistema de Notificaciones

```javascript
function mostrarToast(mensaje, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    toast.textContent = mensaje;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('mostrar'), 100);
    setTimeout(() => {
        toast.classList.remove('mostrar');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Uso
mostrarToast('✅ Guardado exitosamente', 'success');
mostrarToast('❌ Error al guardar', 'error');
mostrarToast('⚠️ Advertencia', 'warning');
```

---

## 🔐 Autenticación en Frontend

```javascript
// Guardar usuario en localStorage (login exitoso)
localStorage.setItem('usuario', JSON.stringify({
    id_usuario: 1,
    correo: 'usuario@mail.com',
    rol: 'Paciente'
}));

// Recuperar usuario
const usuario = JSON.parse(localStorage.getItem('usuario'));

// Validar sesión (ejecutar en cada página protegida)
function validarSesion() {
    if (!localStorage.getItem('usuario')) {
        window.location.href = 'login.html';
    }
}

// Logout
function logout() {
    localStorage.removeItem('usuario');
    window.location.href = 'login.html';
}
```

---

## 🚀 Ejecución

### Opción 1: Live Server (VS Code) ⭐ RECOMENDADO
```bash
# Abre carpeta en VS Code
code frontend

# Instala extensión "Live Server" (Ritwick Dey)
# Clic derecho en login.html → "Open with Live Server"
# Se abre automáticamente en http://127.0.0.1:5500
```

### Opción 2: Servidor Python
```bash
cd frontend
python -m http.server 5500
# Abre: http://localhost:5500/login.html
```

---

## ⚠️ CORS & Problemas Comunes

### Error: "CORS policy blocked"
**Causa:** Abrir archivo con doble clic (file://)  
**Solución:** Usar Live Server o servidor HTTP local

### Error: "Cannot GET /login.html"
**Causa:** Backend no está corriendo  
**Solución:** `uvicorn main:app --reload` en carpeta backend

### Verificar conexión
```javascript
// En consola (F12)
fetch('http://localhost:8000/health')
    .then(r => r.json())
    .then(d => console.log(d))
    .catch(e => console.error('Backend no disponible'))
```

---

## 📱 Responsividad

```css
/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .sidebar { width: 250px; }
    .contenido { margin-left: 250px; }
}

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
    .sidebar { width: 200px; }
}

/* Mobile (menos de 768px) */
@media (max-width: 767px) {
    .sidebar { position: fixed; transform: translateX(-100%); }
}
```

---

## 🛠️ Tabla Dinámica (Componente Reutilizable)

```javascript
function renderizarTabla(titulo, datos, endpoint) {
    let html = `<h2>${titulo}</h2><table class="tabla"><thead><tr>`;
    
    // Encabezados
    Object.keys(datos[0] || {}).forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '<th>Acciones</th></tr></thead><tbody>';
    
    // Filas
    datos.forEach(fila => {
        html += '<tr>';
        Object.values(fila).forEach(val => html += `<td>${val}</td>`);
        html += `
            <td>
                <button onclick="editarItem(${fila.id}, '${endpoint}')">✏️</button>
                <button onclick="eliminarItem(${fila.id}, '${endpoint}')">🗑️</button>
            </td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    document.getElementById('contenido').innerHTML = html;
}
```

---

## 🔍 Debugging

```javascript
// Console (F12)
console.log('Debug:', datos);
console.error('Error:', error);

// Network tab
// Ver requests/responses HTTP en tiempo real

// Local Storage
localStorage.getItem('usuario')
localStorage.setItem('debug', 'true')
localStorage.clear()
```

---

## 📋 Validación de Formularios

```javascript
// auth.js
function validarEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validarContrasena(pwd) {
    return pwd.length >= 6;
}

// Uso
if (!validarEmail(correo)) {
    mostrarToast('❌ Email inválido', 'error');
}
```

---

## 🎯 Flujo Típico

```
index.html (Landing)
    ↓
login.html (Autenticación)
    ↓ Credenciales válidas
    ↓
panel.html (Dashboard)
    ├─ pacientes.html (CRUD)
    ├─ citas.html (Agenda)
    ├─ tratamientos.html (Catálogo)
    ├─ pagos.html (Finanzas)
    └─ roles.html (Permisos)
    ↓
logout (Volver a login.html)
```

---

## 📈 Mejoras Futuras

- 🔐 JWT tokens en lugar de localStorage
- ⚡ Lazy loading de módulos
- 🎨 Tema oscuro/claro
- 📊 Gráficos (Chart.js)
- 🔔 WebSockets para notificaciones real-time
- 📱 PWA (Progressive Web App)

---

## 📞 URLs Importantes

| Servicio | URL |
|----------|-----|
| **Frontend** | http://localhost:5500/login.html |
| **Backend** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

---

**Versión:** 2.0.0 | **Stack:** HTML5 + CSS3 + JavaScript ES6+ | **API:** Fetch API

Para detalles del backend, consulta `readme, bckend.md`  
Para guía general, consulta `README.md`
