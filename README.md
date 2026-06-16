# 🦷 OdontoSoft — Sistema de Gestión Odontológica

Sistema completo de gestión para clínicas odontológicas, desarrollado con **FastAPI + SQLite** en el backend y **HTML/CSS/JS vanilla** en el frontend.

---

## 📁 Estructura del Proyecto

```
odontosoft/
│
├── backend/                    # API REST con FastAPI
│   ├── main.py                 # Punto de entrada, registro de routers y CORS
│   ├── database.py             # Conexión SQLite con SQLAlchemy
│   ├── models.py               # Modelos ORM (tablas de la BD)
│   ├── schemas.py              # Esquemas Pydantic (validación)
│   ├── requirements.txt        # Dependencias Python
│   └── routers/
│       ├── __init__.py
│       ├── roles.py            # CRUD /roles
│       ├── usuarios.py         # CRUD /usuarios
│       ├── tratamientos.py     # CRUD /tratamientos
│       ├── citas.py            # CRUD /citas
│       ├── servicios.py        # CRUD /servicios
│       └── proveedores.py      # CRUD /proveedores
│
└── frontend/                   # Interfaz de usuario
    ├── html/
    │   ├── login.html          # Inicio de sesión
    │   ├── panel.html          # Gestión de usuarios (admin)
    │   ├── roles.html          # Gestión de roles
    │   ├── tratamientos.html   # Catálogo de tratamientos
    │   ├── citas.html          # Agenda de citas
    │   ├── proveedores.html    # Proveedores médicos
    │   ├── panel_cliente.html  # Portal del paciente
    │   └── contacto.html       # Canales de atención
    ├── css/
    │   └── style.css           # Estilos del dashboard
    └── js/
        └── api.js              # Módulo de llamadas a la API (fetch)
```

---

## 🗄️ Tablas de la Base de Datos

| Tabla          | Descripción                              |
|----------------|------------------------------------------|
| `roles`        | Roles del sistema (Admin, Odontólogo, Paciente) |
| `usuarios`     | Personal y pacientes registrados         |
| `tratamientos` | Catálogo de procedimientos dentales      |
| `citas`        | Agenda de citas médicas                  |
| `servicios`    | Historial de servicios por paciente      |
| `proveedores`  | Proveedores de suministros médicos       |

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias del backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Iniciar el servidor FastAPI

```bash
uvicorn main:app --reload
```

El servidor queda disponible en: **http://127.0.0.1:8000**

### 3. Abrir el frontend

Abre directamente `frontend/html/login.html` en tu navegador.

> **Importante:** El frontend usa `fetch()` apuntando a `http://127.0.0.1:8000`.  
> El backend debe estar corriendo antes de abrir el HTML.

---

## 📡 Endpoints de la API

| Método | Ruta                          | Descripción                     |
|--------|-------------------------------|---------------------------------|
| GET    | `/roles`                      | Listar todos los roles          |
| POST   | `/roles`                      | Crear nuevo rol                 |
| PUT    | `/roles/{id}`                 | Actualizar rol                  |
| DELETE | `/roles/{id}`                 | Eliminar rol                    |
| GET    | `/usuarios`                   | Listar todos los usuarios       |
| POST   | `/usuarios`                   | Crear usuario                   |
| PUT    | `/usuarios/{id}`              | Actualizar usuario              |
| DELETE | `/usuarios/{id}`              | Eliminar usuario                |
| GET    | `/tratamientos`               | Listar tratamientos             |
| POST   | `/tratamientos`               | Crear tratamiento               |
| GET    | `/citas`                      | Listar todas las citas          |
| GET    | `/citas/paciente/{id}`        | Citas de un paciente            |
| GET    | `/citas/odontologo/{id}`      | Citas de un odontólogo          |
| POST   | `/citas`                      | Crear cita                      |
| PATCH  | `/citas/{id}/estado`          | Cambiar estado de cita          |
| DELETE | `/citas/{id}`                 | Eliminar cita                   |
| GET    | `/servicios/paciente/{id}`    | Servicios de un paciente        |
| POST   | `/servicios`                  | Registrar servicio              |
| GET    | `/proveedores`                | Listar proveedores              |
| POST   | `/proveedores`                | Registrar proveedor             |
| PUT    | `/proveedores/{id}`           | Actualizar proveedor            |
| DELETE | `/proveedores/{id}`           | Eliminar proveedor              |

📄 Documentación interactiva automática: **http://127.0.0.1:8000/docs**

---

## 🔧 Orden recomendado para poblar la BD

1. Crear **Roles** (Administrador, Odontólogo, Paciente)
2. Crear **Usuarios** (asignarles rol)
3. Crear **Tratamientos**
4. Registrar **Citas** (vinculando paciente + odontólogo + tratamiento)
5. Registrar **Proveedores**
