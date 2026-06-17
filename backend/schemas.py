from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── ROLES ──────────────────────────────────────────────────────────────────────

class RolBase(BaseModel):
    nombre:      str
    descripcion: Optional[str] = None
    permisos:    Optional[str] = None

class RolCreate(RolBase):
    pass

class RolOut(RolBase):
    id: int
    class Config:
        from_attributes = True


# ── USUARIOS ───────────────────────────────────────────────────────────────────

class UsuarioBase(BaseModel):
    nombre:         str
    correo:         EmailStr
    identificacion: str
    estado:         Optional[str] = "Activo"
    rol_id:         int

class UsuarioCreate(UsuarioBase):
    password: str          # Texto plano → se hashea en la ruta

class UsuarioOut(UsuarioBase):
    id:        int
    creado_en: Optional[datetime]
    rol:       Optional[RolOut]
    class Config:
        from_attributes = True


# ── TRATAMIENTOS ───────────────────────────────────────────────────────────────

class TratamientoBase(BaseModel):
    nombre:      str
    descripcion: Optional[str] = None
    precio_base: Optional[int] = 0

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoOut(TratamientoBase):
    id: int
    class Config:
        from_attributes = True


# ── CITAS ──────────────────────────────────────────────────────────────────────

class CitaBase(BaseModel):
    paciente_id:    int
    odontologo_id:  int
    tratamiento_id: Optional[int] = None
    fecha_hora:     str
    estado:         Optional[str] = "En Espera"
    notas:          Optional[str] = None

class CitaCreate(CitaBase):
    pass

class CitaOut(CitaBase):
    id:        int
    creado_en: Optional[datetime]
    class Config:
        from_attributes = True


# ── SERVICIOS ──────────────────────────────────────────────────────────────────

class ServicioBase(BaseModel):
    paciente_id:    int
    tratamiento_id: int
    odontologo_id:  Optional[int] = None
    proxima_cita:   Optional[str] = None
    estado_cuenta:  Optional[str] = "Saldo Pendiente"

class ServicioCreate(ServicioBase):
    pass

class ServicioOut(ServicioBase):
    id:        int
    creado_en: Optional[datetime]
    class Config:
        from_attributes = True


# ── PROVEEDORES ────────────────────────────────────────────────────────────────

class ProveedorBase(BaseModel):
    empresa:         str
    contacto_asesor: Optional[str] = None
    telefono:        Optional[str] = None
    suministro:      Optional[str] = None
    estado_convenio: Optional[str] = "Vigente"

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorOut(ProveedorBase):
    id:        int
    creado_en: Optional[datetime]
    class Config:
        from_attributes = True
