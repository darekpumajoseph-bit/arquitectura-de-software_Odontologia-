from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from database import engine
import models

from routers import (
    usuarios, pacientes, odontologos, consultorios,
    historias_clinicas, citas, tratamientos,
    recordatorios, pagos, facturas,
    auth  # <-- Importar auth
)

app = FastAPI(
    title="OdontoSoft API",
    description="Sistema de Gestión Odontológica — Backend REST con FastAPI + PostgreSQL",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de log
@app.middleware("http")
async def registrar_peticiones(request: Request, call_next):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# Routers
app.include_router(usuarios.router)
app.include_router(pacientes.router)
app.include_router(odontologos.router)
app.include_router(consultorios.router)
app.include_router(historias_clinicas.router)
app.include_router(citas.router)
app.include_router(tratamientos.router)
app.include_router(recordatorios.router)
app.include_router(pagos.router)
app.include_router(facturas.router)
app.include_router(auth.router)  # <-- Registrar auth

@app.get("/", tags=["Root"])
def root():
    return {
        "sistema": "OdontoSoft API",
        "version": "2.0.0",
        "documentacion": "/docs",
        "estado": "Activo",
        "base_datos": "PostgreSQL - ProyectoApi"
    }