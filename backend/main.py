from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from database import engine
import models

# Crear todas las tablas en la base de datos SQLite
models.Base.metadata.create_all(bind=engine)

# Importar routers
from routers import roles, usuarios, tratamientos, citas, servicios, proveedores

app = FastAPI(
    title="OdontoSoft API",
    description="Sistema de Gestión Odontológica — Backend REST con FastAPI + SQLite",
    version="1.0.0"
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # En producción, limitar al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MIDDLEWARE DE LOG ──────────────────────────────────────────────────────────
@app.middleware("http")
async def registrar_peticiones(request: Request, call_next):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# ── EXCEPCIONES PERSONALIZADAS ─────────────────────────────────────────────────
class RecursoNoEncontrado(Exception):
    def __init__(self, recurso: str):
        self.recurso = recurso

@app.exception_handler(RecursoNoEncontrado)
async def recurso_error(request: Request, exc: RecursoNoEncontrado):
    return JSONResponse(
        status_code=404,
        content={"error": True, "mensaje": f"{exc.recurso} no encontrado", "hora": str(datetime.now())}
    )

# ── ROUTERS ────────────────────────────────────────────────────────────────────
app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(tratamientos.router)
app.include_router(citas.router)
app.include_router(servicios.router)
app.include_router(proveedores.router)

# ── RUTA RAÍZ ──────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "sistema": "OdontoSoft API",
        "version": "1.0.0",
        "documentacion": "/docs",
        "estado": "Activo"
    }
