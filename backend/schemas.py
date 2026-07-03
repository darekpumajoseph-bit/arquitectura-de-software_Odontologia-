from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, time, datetime
from decimal import Decimal


# ── USUARIO ───────────────────────────────────────────────────────────────────

class UsuarioBase(BaseModel):
    correo: EmailStr
    rol: str
    estado: str = "Activo"

class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=6, description="Mínimo 6 caracteres")

class UsuarioOut(UsuarioBase):
    id_usuario: int
    class Config:
        from_attributes = True


# ── PACIENTE ──────────────────────────────────────────────────────────────────

class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    documento: str
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    eps: Optional[str] = None
    alergias: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteOut(PacienteBase):
    id_paciente: int
    class Config:
        from_attributes = True


# ── REGISTRO (para el frontend) ──────────────────────────────────────────────
# ── REGISTRO DE USUARIO (con datos de paciente) ──────────────────────────────

class RegistroUsuario(BaseModel):
    correo: EmailStr
    contrasena: str
    nombre: str
    apellido: str
    telefono: str
    
class RegistroRequest(BaseModel):
    correo: EmailStr
    contrasena: str = Field(..., min_length=6)
    nombre: str
    apellido: str
    telefono: str

class RegistroResponse(BaseModel):
    mensaje: str
    id_usuario: int
    id_paciente: int
    correo: str
    rol: str



# ── CONSULTORIO ──────────────────────────────────────────────────────────────

class ConsultorioBase(BaseModel):
    nombre: str
    ubicacion: Optional[str] = None
    numero_sala: Optional[str] = None

class ConsultorioCreate(ConsultorioBase):
    pass

class ConsultorioOut(ConsultorioBase):
    id_consultorio: int
    class Config:
        from_attributes = True


# ── ODONTOLOGO ───────────────────────────────────────────────────────────────

class OdontologoBase(BaseModel):
    nombre: str
    apellido: str
    documento: str
    telefono: Optional[str] = None
    correo: Optional[str] = None
    especialidad: Optional[str] = None
    registro_profesional: Optional[str] = None
    horario: Optional[str] = None
    id_consultorio: int

class OdontologoCreate(OdontologoBase):
    pass

class OdontologoOut(OdontologoBase):
    id_odontologo: int
    class Config:
        from_attributes = True


# ── HISTORIA CLINICA ─────────────────────────────────────────────────────────

class HistoriaClinicaBase(BaseModel):
    fecha_apertura: date
    antecedentes: Optional[str] = None
    diagnostico_general: Optional[str] = None
    observaciones: Optional[str] = None
    id_paciente: int

class HistoriaClinicaCreate(HistoriaClinicaBase):
    pass

class HistoriaClinicaOut(HistoriaClinicaBase):
    id_historia: int
    class Config:
        from_attributes = True


# ── CITA ─────────────────────────────────────────────────────────────────────

class CitaBase(BaseModel):
    fecha: date
    hora: time
    estado: Optional[str] = None
    motivo_consulta: Optional[str] = None
    observaciones: Optional[str] = None
    id_paciente: int
    id_odontologo: int
    id_consultorio: int

class CitaCreate(CitaBase):
    pass

class CitaOut(CitaBase):
    id_cita: int
    class Config:
        from_attributes = True


# ── TRATAMIENTO ──────────────────────────────────────────────────────────────

class TratamientoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    costo: Optional[Decimal] = None
    duracion_estimada: Optional[str] = None
    id_cita: int

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoOut(TratamientoBase):
    id_tratamiento: int
    class Config:
        from_attributes = True


# ── RECORDATORIO ─────────────────────────────────────────────────────────────

class RecordatorioBase(BaseModel):
    tipo: Optional[str] = None
    fecha_envio: Optional[datetime] = None
    estado: Optional[str] = None
    id_cita: int

class RecordatorioCreate(RecordatorioBase):
    pass

class RecordatorioOut(RecordatorioBase):
    id_recordatorio: int
    class Config:
        from_attributes = True


# ── PAGO ─────────────────────────────────────────────────────────────────────

class PagoBase(BaseModel):
    fecha_pago: date
    monto: Decimal
    metodo_pago: Optional[str] = None
    estado_pago: Optional[str] = None
    referencia: Optional[str] = None
    id_cita: int

class PagoCreate(PagoBase):
    pass

class PagoOut(PagoBase):
    id_pago: int
    class Config:
        from_attributes = True


# ── FACTURA ──────────────────────────────────────────────────────────────────

class FacturaBase(BaseModel):
    fecha_emision: date
    subtotal: Optional[Decimal] = None
    impuesto: Optional[Decimal] = None
    total: Optional[Decimal] = None
    id_pago: int

class FacturaCreate(FacturaBase):
    pass

class FacturaOut(FacturaBase):
    id_factura: int
    class Config:
        from_attributes = True