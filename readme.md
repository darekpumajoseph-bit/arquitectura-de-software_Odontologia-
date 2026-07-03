1. Archivo para el Backend (backend/README.md)
Markdown
# OdontoSoft API — Backend

Este es el backend oficial de **OdontoSoft**, un sistema RESTful de gestión para clínicas y consultorios odontológicos. Está desarrollado utilizando **FastAPI**, **SQLAlchemy ORM** y **PostgreSQL** como motor de base de datos relacional.

---

## 🚀 Tecnologías Utilizadas

* **Python 3.11+**
* **FastAPI**: Framework web de alto rendimiento para la construcción de APIs.
* **SQLAlchemy**: Mapeador de objetos relacionales (ORM) para la interacción con la base de datos.
* **PostgreSQL**: Sistema de gestión de bases de datos relacionales.
* **Pydantic v2**: Validación de datos y gestión de configuraciones.
* **Python-dotenv**: Gestión de variables de entorno para la configuración segura del sistema.
* **Uvicorn**: Servidor ASGI ultrarrápido para la ejecución de la aplicación.
* **Hashlib**: Lógica interna de cifrado utilizando SHA-256 para la seguridad de credenciales.

---

## 📂 Arquitectura y Descripción de Archivos

El backend está estructurado de forma modular para separar las responsabilidades:

### ⚙️ Archivos Core (Raíz)
* **`main.py`**: Es el corazón del backend. Inicializa FastAPI, configura CORS, establece el middleware para registrar peticiones y unifica todos los "routers" del sistema.
* **`database.py`**: Gestiona la comunicación con PostgreSQL. Lee las credenciales del archivo `.env`, crea el "Engine" de conexión y proporciona la sesión (`get_db`).
* **`models.py`**: Define la estructura de las tablas usando SQLAlchemy (ORM). Aquí se programan las relaciones (ej. un paciente tiene muchas citas) y las tablas intermedias.
* **`schemas.py`**: Contiene los modelos de Pydantic. Su función es asegurar que los datos enviados por el frontend tengan el formato correcto antes de guardarlos.
* **`test_connection.py`**: Script de diagnóstico para probar de forma aislada que el backend logra conectarse a la base de datos `ProyectoApi`.
* **`requirements.txt`**: El manifiesto de dependencias. Contiene la lista exacta de librerías y versiones necesarias.
* **`.env`**: Archivo de configuración local que almacena las claves de seguridad y credenciales de acceso a la base de datos.

### 🛣️ Módulos de Rutas (`/routers/`)
Contiene la lógica de negocio (CRUD) dividida por entidad:
* **`usuarios.py`**: Registro de usuarios, cifrado de contraseñas (SHA-256).
* **`pacientes.py`**: Fichas de pacientes, datos de contacto, EPS y alergias.
* **`odontologos.py`**: Perfil del personal médico y especialidades.
* **`citas.py`**: Módulo central que cruza pacientes, odontólogos y tratamientos.
* **`historias_clinicas.py`**: Registro confidencial de antecedentes y diagnósticos.
* **`tratamientos.py`**: Catálogo de procedimientos odontológicos y precios base.
* **`consultorios.py`**: Gestión de los espacios físicos (sedes, número de sala).
* **`pagos.py` & `facturas.py`**: Módulos financieros y de facturación.
* **`proveedores.py` & `servicios.py`**: Gestión administrativa (convenios, compra de insumos).
* **`recordatorios.py`**: Notificaciones y alertas preventivas sobre citas.
* **`roles.py`**: Perfiles de acceso y permisos del sistema.

---

## 🛠️ Guía Completa de Instalación y Ejecución

Sigue estos pasos estrictamente para levantar el backend en tu computadora local.

### Paso 1: Acceder al directorio
Abre tu terminal (Símbolo del sistema o PowerShell) y navega a la carpeta del backend:
```bash
cd C:\Users\SENA\Downloads\pollardo\backend
Paso 2: Crear el Entorno Virtual
Es obligatorio usar un entorno virtual para aislar las dependencias de este proyecto del resto de tu sistema.

Bash
python -m venv env
(Esto creará una carpeta llamada env con la instalación limpia de Python).

Paso 3: Activar el Entorno Virtual
Dependiendo de tu sistema operativo, ejecuta:

En Windows (CMD/PowerShell):

Bash
.\env\Scripts\activate
En Mac/Linux:

Bash
source env/bin/activate
(Sabrás que funcionó porque verás (env) al inicio de la línea en tu terminal).

Paso 4: Instalar las Dependencias
Con el entorno activado, instala todas las librerías requeridas (FastAPI, SQLAlchemy, etc.):

Bash
pip install -r requirements.txt
Paso 5: Configurar la Base de Datos (Variables de Entorno)
Crea un archivo nuevo llamado exactamente .env en la raíz de la carpeta backend/ y pega lo siguiente (ajusta la contraseña si es distinta):

Plaintext
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ProyectoApi
Paso 6: Base de Datos en PostgreSQL
Asegúrate de abrir PostgreSQL (pgAdmin o DBeaver), crea una base de datos llamada ProyectoApi y ejecuta el script SQL con las sentencias CREATE TABLE para que el sistema tenga dónde guardar los datos.

Paso 7: Levantar el Servidor
Finalmente, inicia el servidor de desarrollo (sólo funcionará si el entorno virtual está activado):

Bash
uvicorn main:app --reload
¡Listo! La API estará corriendo en: http://127.0.0.1:8000
