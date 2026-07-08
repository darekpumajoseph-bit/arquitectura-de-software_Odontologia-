# 🎨 Frontend OdontoSoft — Documentación

![HTML5](https://img.shields.io/badge/HTML5-Semántico-orange) ![CSS3](https://img.shields.io/badge/CSS3-Responsive-blue) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)

Interfaz web moderna y responsiva para OdontoSoft. Comunicación centralizada con API REST mediante Fetch API.

---

## 📂 Estructura

```
frontend/
├── html/                        # Vistas
│   ├── index.html               # Landing page
│   ├── login.html               # Autenticación
│   ├── registro.html            # Registro de usuarios
│   ├── panel.html               # Dashboard administrador
│   ├── panel_cliente.html       # Autogestión pacientes
│   ├── citas.html               # Agendamiento
│   ├── pacientes.html           # Directorio pacientes
│   ├── odontologos.html         # Directorio odontólogos
│   ├── tratamientos.html        # Catálogo servicios
│   ├── roles.html               # Gestión de permisos
│   ├── proveedores.html         # Convenios
│   ├── contacto.html            # Soporte
│   └── politicas/               # Legal
│       ├── politica-privacidad.html
│       ├── proteccion-datos.html
│       └── uso-sistema.html
│
├── css/                         # Estilos
│   ├── style.css                # Estilos principales (dashboard, modales, tablas)
│   ├── auth.css                 # Login/registro responsive
│   └── politicas.css            # Documentos legales
│
└── js/                          # Lógica JavaScript
    ├── api.js                   # Cliente HTTP centralizado → Fetch API
    └── auth.js                  # Validación formularios
```

---

## 🎨 Diseño & Componentes

### Características UI
- ✅ **Layout responsivo** — Grid + Flexbox
- ✅ **Dashboard moderno** — Menú lateral, contenido dinámico
- ✅ **Modales nativos** — Creación/edición de registros
- ✅ **Tablas dinámicas** — Datos desde BD en tiempo real
- ✅ **Toast notifications** — Alertas flotantes (éxito/error)
- ✅ **Iconos Material** — Material Symbols Outlined
- ✅ **Tipografía Poppins** — Limpia y profesional

### CSS - Variables Globales
```css
:root {
    --primary-color: #2196F3;        /* Azul */
    --secondary-color: #FF9800;      /* Naranja */
    --success-color: #4CAF50;        /* Verde */
    --danger-color: #F44336;         /* Rojo */
    --dark-bg: #1a1a1a;
    --light-bg: #f5f5f5;
    --text-dark: #333;
    --text-light: #666;
}
```

---

## 🔌 API Integration (js/api.js)

**Centraliza todos los requests HTTP hacia el backend:**

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

async function loginUsuario(correo, contrasena) {
    const resp = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, contrasena })
    });
    return resp.json();
}

// CRUD Genérico
async function obtenerDatos(endpoint) {
    const resp = await fetch(`${API_BASE}/${endpoint}`);
    return resp.json();
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
    const resp = await fetch(`${API_BASE}/${endpoint}/${id}`, {
        method: "DELETE"
    });
    return resp.status === 204;
}
```

---

## 📄 Vistas Principales

### index.html
- Landing page informativa
- Introducción a OdontoSoft
- Botones de login/registro

### login.html
```html
<!-- Formulario login -->
<form id="loginForm">
    <input type="email" id="correo" placeholder="Correo" required>
    <input type="password" id="contrasena" placeholder="Contraseña" required>
    <button type="submit">Iniciar Sesión</button>
    <a href="registro.html">¿No tienes cuenta? Regístrate</a>
</form>

<script>
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const correo = document.getElementById('correo').value;
    const contrasena = document.getElementById('contrasena').value;
    
    try {
        const respuesta = await loginUsuario(correo, contrasena);
        if (respuesta.id_usuario) {
            localStorage.setItem('usuario', JSON.stringify(respuesta));
            mostrarToast('✅ Inicio de sesión exitoso', 'success');
            window.location.href = 'panel.html';
        } else {
            mostrarToast('❌ Credenciales inválidas', 'error');
        }
    } catch (error) {
        mostrarToast('❌ Error al iniciar sesión', 'error');
    }
});
</script>
```

### registro.html
- Formulario de registro (Paciente/Odontólogo)
- Validación de campos
- Cifrado de contraseña antes de enviar

### panel.html (Dashboard)
```html
<!-- Menú lateral -->
<aside class="sidebar">
    <nav>
        <a href="#" onclick="mostrarSeccion('usuarios')">👥 Usuarios</a>
        <a href="#" onclick="mostrarSeccion('pacientes')">🦷 Pacientes</a>
        <a href="#" onclick="mostrarSeccion('citas')">📅 Citas</a>
        <a href="#" onclick="mostrarSeccion('tratamientos')">💊 Tratamientos</a>
        <a href="#" onclick="mostrarSeccion('pagos')">💰 Pagos</a>
    </nav>
</aside>

<!-- Contenido dinámico -->
<main class="contenido" id="contenido">
    <!-- Se llena con JavaScript según sección seleccionada -->
</main>

<script>
async function mostrarSeccion(seccion) {
    let endpoint = '';
    let titulo = '';
    
    if (seccion === 'pacientes') {
        endpoint = 'pacientes';
        titulo = '🦷 Pacientes';
    } else if (seccion === 'citas') {
        endpoint = 'citas';
        titulo = '📅 Citas';
    }
    // ... más secciones
    
    const datos = await obtenerDatos(endpoint);
    renderizarTabla(titulo, datos, endpoint);
}

function renderizarTabla(titulo, datos, endpoint) {
    let html = `<h2>${titulo}</h2>`;
    html += '<table class="tabla"><thead><tr>';
    
    // Encabezados dinámicos
    if (datos.length > 0) {
        Object.keys(datos[0]).forEach(col => {
            html += `<th>${col}</th>`;
        });
        html += '<th>Acciones</th></tr></thead><tbody>';
        
        // Filas de datos
        datos.forEach(fila => {
            html += '<tr>';
            Object.values(fila).forEach(val => {
                html += `<td>${val}</td>`;
            });
            html += `
                <td>
                    <button onclick="editarItem(${fila.id}, '${endpoint}')">✏️ Editar</button>
                    <button onclick="eliminarItem(${fila.id}, '${endpoint}')">🗑️ Eliminar</button>
                </td>
            </tr>`;
        });
        html += '</tbody></table>';
    }
    
    document.getElementById('contenido').innerHTML = html;
}
</script>
```

### citas.html
- Calendario/agenda
- Agendamiento de citas
- Filtros por paciente/odontólogo
- Estado de citas (Pendiente, Confirmada, Completada)

### pacientes.html
- Listado con búsqueda
- CRUD completo
- Modal para crear/editar
- Campos: nombre, documento, EPS, alergias

---

## 💬 Toast Notifications

Sistema de alertas flotantes:

```javascript
function mostrarToast(mensaje, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    toast.textContent = mensaje;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('mostrar');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('mostrar');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Uso
mostrarToast('✅ Usuario registrado exitosamente', 'success');
mostrarToast('❌ Error al guardar datos', 'error');
mostrarToast('⚠️ Campo requerido', 'warning');
```

---

## 🔐 Autenticación en Frontend

```javascript
// Guardar usuario en localStorage
localStorage.setItem('usuario', JSON.stringify({
    id_usuario: 1,
    correo: 'usuario@mail.com',
    rol: 'Paciente',
    estado: 'Activo'
}));

// Recuperar usuario
const usuario = JSON.parse(localStorage.getItem('usuario'));

// Logout
function logout() {
    localStorage.removeItem('usuario');
    window.location.href = 'login.html';
}

// Validar sesión
function validarSesion() {
    if (!localStorage.getItem('usuario')) {
        window.location.href = 'login.html';
    }
}

// Ejecutar en cada página protegida
validarSesion();
```

---

## 🚀 Ejecución

### Opción 1: Live Server (VS Code) ⭐ RECOMENDADO
```bash
# Abre carpeta frontend en VS Code
code .

# Instala extensión "Live Server" (Ritwick Dey)
# Clic derecho en login.html → "Open with Live Server"
# Se abre en http://127.0.0.1:5500 automáticamente
```

### Opción 2: Servidor Python
```bash
cd frontend
python -m http.server 5500
# Luego: http://localhost:5500/login.html
```

### Opción 3: Live.js (sin herramientas)
```html
<!-- En el <head> de cada archivo -->
<script type="module" src="js/api.js"></script>
<!-- Los cambios se reflejan automáticamente -->
```

---

## ⚠️ CORS & SEGURIDAD

### Problema: CORS error
```
Access to XMLHttpRequest at 'http://localhost:8000/...' 
from origin 'http://localhost:5500' has been blocked by CORS policy
```

### Soluciones:
1. ✅ Backend debe tener CORS configurado (ver `main.py`)
2. ✅ NO abrir archivos con doble clic (file://)
3. ✅ SÍ usar servidor local (Live Server o Python)

### Headers esperados en requests
```javascript
fetch(URL, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
        // ⚠️ NO agregar 'Authorization' sin JWT
    },
    body: JSON.stringify(datos)
})
```

---

## 📱 Responsividad

### Breakpoints CSS
```css
/* Desktop */
@media (min-width: 1024px) {
    .sidebar { width: 250px; }
    .contenido { margin-left: 250px; }
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) {
    .sidebar { width: 200px; }
}

/* Mobile */
@media (max-width: 767px) {
    .sidebar { position: fixed; transform: translateX(-100%); }
    .menu-toggle { display: block; }
}
```

---

## 🎯 Flujo Típico de Usuario

```
1. index.html (Landing) 
   ↓
2. login.html (Autenticación)
   ↓ Credenciales válidas
   ↓
3. panel.html (Dashboard principal)
   ├─ Pacientes (CRUD)
   ├─ Citas (Agenda)
   ├─ Tratamientos (Catálogo)
   ├─ Pagos (Finanzas)
   └─ Roles (Administración)
   ↓
4. logout (localStorage.removeItem + redirect login.html)
```

---

## 🛠️ Validación de Formularios

```javascript
// auth.js
function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validarContrasena(pwd) {
    return pwd.length >= 6;
}

function validarFormulario(formData) {
    if (!validarEmail(formData.correo)) {
        mostrarToast('❌ Email inválido', 'error');
        return false;
    }
    if (!validarContrasena(formData.contrasena)) {
        mostrarToast('❌ Contraseña mínimo 6 caracteres', 'error');
        return false;
    }
    return true;
}
```

---

## 📊 Componentes Reutilizables

### Modal Genérico
```html
<div id="miModal" class="modal">
    <div class="modal-contenido">
        <span class="cerrar" onclick="cerrarModal()">&times;</span>
        <h2>Crear Paciente</h2>
        <form id="formulario">
            <input type="text" name="nombre" required>
            <button type="submit">Guardar</button>
        </form>
    </div>
</div>

<script>
function abrirModal() {
    document.getElementById('miModal').style.display = 'block';
}
function cerrarModal() {
    document.getElementById('miModal').style.display = 'none';
}
</script>
```

### Tabla Dinámica
```javascript
function crearTabla(datos, columnas) {
    let html = '<table class="tabla"><thead><tr>';
    columnas.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    datos.forEach(fila => {
        html += '<tr>';
        columnas.forEach(col => {
            html += `<td>${fila[col]}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    return html;
}
```

---

## 🔍 Debugging en Navegador

```javascript
// Console
console.log('Datos:', datos);
console.error('Error:', error);

// Network tab (F12)
// Verifica requests/responses HTTP

// Local Storage
localStorage.getItem('usuario')
localStorage.setItem('debug', 'true')
localStorage.clear()
```

---

## 📈 Mejoras Futuras

- 🔐 JWT tokens en lugar de localStorage
- ⚡ Lazy loading de módulos
- 🎨 Theme oscuro/claro
- 📊 Gráficos con Chart.js
- 🔔 WebSockets para notificaciones real-time
- 📱 PWA (Progressive Web App)
- ♿ Mejoras accesibilidad (WCAG)

---

## 📞 Soporte

**Si hay errores en consola (F12):**
1. Verifica que Backend esté corriendo en http://localhost:8000
2. Revisa Network tab para ver requests fallidos
3. Comprueba que `api.js` apunta a URL correcta
4. Abre DevTools: F12 → Console → busca errores

**URLs importantes:**
- Frontend: http://localhost:5500/login.html
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

**Versión:** 2.0.0 | **Stack:** HTML5 + CSS3 + JavaScript ES6+ | **Comunicación:** Fetch API

Para detalles del backend, consulta `readme, bckend.md`
