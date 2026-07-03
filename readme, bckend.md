### 2. Archivo para el Frontend (`frontend/README.md`)

```markdown
# OdontoSoft — Frontend UI

Este es el frontend oficial de **OdontoSoft**, una interfaz web moderna, limpia y responsiva diseñada para interactuar con la API del backend. Permite una administración intuitiva para administradores, personal médico y pacientes.

---

## 🎨 Características e Interfaz

* **Diseño Profesional**: Desarrollado con HTML5 semántico y CSS3 (variables globales), tipografía `Poppins` e íconos `Material Symbols Outlined`.
* **Componentes Dinámicos**: Control de Modales nativos para creación/edición y tablas que se renderizan consumiendo la base de datos.
* **Feedback en Tiempo Real**: Sistema de alertas tipo `Toast` flotantes (Éxito, Error).
* **Cumplimiento de Políticas**: Vistas obligatorias de Política de Privacidad y Protección de Datos.

---

## 📂 Arquitectura y Descripción de Archivos

### 🎨 Capa de Estilos (`/css/`)
* **`style.css`**: Hoja maestra. Define layout del dashboard, menú lateral, colores globales, tablas y modales unificados.
* **`auth.css`**: Optimiza la apariencia responsiva de las pantallas de `login.html` y `registro.html`.
* **`politicas.css`**: Garantiza la legibilidad de textos legales (alineación, tipografía limpia, espaciados).

### ⚙️ Capa Lógica (`/js/`)
* **`api.js`**: El cerebro de la comunicación. Centraliza todas las peticiones HTTP (`fetch`) hacia el backend (FastAPI). Exporta cada endpoint como una función.
* **`auth.js`**: Lógica visual de los formularios de acceso (mostrar/ocultar contraseñas, validar que coincidan al registrarse).

### 🖥️ Vistas (Interfaces HTML)
* **`index.html`**: Landing Page informativa.
* **`login.html` & `registro.html`**: Pantallas de autenticación y alta de usuarios.
* **`panel.html`**: Dashboard principal, actualmente gestiona a los **Usuarios**.
* **`roles.html`**: Administra la matriz de permisos y perfiles de acceso.
* **`pacientes.html` & `odontologos.html`**: Directorios del personal médico y clientes.
* **`citas.html`**: Núcleo operativo. Conecta pacientes, médicos y tratamientos en la agenda.
* **`tratamientos.html`**: Gestión del catálogo de servicios y precios base.
* **`proveedores.html`**: Control logístico y convenios de insumos.
* **`panel_cliente.html`**: Autogestión donde el paciente puede agendar citas.
* **`contacto.html`**: Canales de soporte y atención.
* **`politica-privacidad.html`, `proteccion-datos.html`, `uso-sistema.html`**: Documentación legal requerida (Ley 1581 de protección de datos).

---

## 🛠️ Guía de Ejecución y Conexión

Toda la comunicación con el backend se encuentra centralizada en `js/api.js`. Apunta por defecto a:
```javascript
const API_BASE = "[http://127.0.0.1:8000](http://127.0.0.1:8000)";
⚠️ AVISO IMPORTANTE DE SEGURIDAD (CORS)
Debido a que el código JavaScript utiliza Módulos ES (type="module"), los navegadores bloquean la ejecución si abres los archivos con doble clic (ruta file:///).
Es obligatorio usar un servidor web local para que el frontend funcione.

Opción 1: Ejecutar con Visual Studio Code (Recomendada)
Esta es la forma más fácil y rápida:

Abre la carpeta frontend/ en Visual Studio Code.

Ve a Extensiones e instala Live Server (por Ritwick Dey).

Abre el archivo login.html o index.html.

Haz clic derecho en el código y selecciona "Open with Live Server".

Tu navegador se abrirá en http://127.0.0.1:5500/ y funcionará perfectamente.

Opción 2: Ejecutar con Python (Desde la terminal)
Si no usas VS Code, puedes usar Python para levantar un servidor nativo:

Abre una nueva ventana de terminal (no cierres la terminal donde está corriendo el backend).

Navega a la carpeta del frontend:

Bash
cd C:\Users\SENA\Downloads\pollardo\frontend
Ejecuta el servidor HTTP:

Bash
python -m http.server 5500
Abre tu navegador web y escribe manualmente la dirección:
👉 http://localhost:5500/login.html

🔒 Flujo de Prueba Exitoso
Asegúrate de que tu Backend (uvicorn) está encendido.

Abre el Frontend (con Live Server o Python).

Entra a roles.html y crea un rol nuevo; deberías ver el Toast verde ("Rol creado") y cómo la tabla se actualiza leyendo los datos de tu PostgreSQL en tiempo re
