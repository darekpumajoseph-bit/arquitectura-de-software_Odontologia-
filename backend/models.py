from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# ── ENUMERACIONES ──────────────────────────────────────────────────────────────

class RolEnum(str, enum.Enum):
    administrador = "Administrador"
    odontologo    = "Odontólogo"
    paciente      = "Paciente"

class EstadoCitaEnum(str, enum.Enum):
    en_espera  = "En Espera"
    en_proceso = "En Consulta"
    finalizado = "Finalizado"

class EstadoCuentaEnum(str, enum.Enum):
    pendiente = "Saldo Pendiente"
    pagado    = "Pagado"

class EstadoConvenioEnum(str, enum.Enum):
    vigente  = "Vigente"
    vencido  = "Vencido"
    suspendido = "Suspendido"


# ── TABLA: ROLES ───────────────────────────────────────────────────────────────

class Rol(Base):
    __tablename__ = "roles"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    permisos    = Column(String(100), nullable=True)   # Ej: "FULL ACCESS", "READ / UPDATE"

    # Relación inversa
    usuarios = relationship("Usuario", back_populates="rol")


# ── TABLA: USUARIOS ────────────────────────────────────────────────────────────

class Usuario(Base):
    __tablename__ = "usuarios"

    id             = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String(120), nullable=False)
    correo         = Column(String(120), unique=True, nullable=False)
    identificacion = Column(String(20),  unique=True, nullable=False)
    password_hash  = Column(String(255), nullable=False)
    estado         = Column(String(20), default="Activo")
    rol_id         = Column(Integer, ForeignKey("roles.id"), nullable=False)
    creado_en      = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    rol       = relationship("Rol",      back_populates="usuarios")
    citas_dr  = relationship("Cita",     back_populates="odontologo",
                             foreign_keys="Cita.odontologo_id")
    citas_pac = relationship("Cita",     back_populates="paciente",
                             foreign_keys="Cita.paciente_id")
    servicios = relationship("Servicio", back_populates="paciente")


# ── TABLA: TRATAMIENTOS ────────────────────────────────────────────────────────

class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(120), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_base = Column(Integer, default=0)       # En pesos colombianos

    # Relación inversa
    citas    = relationship("Cita",     back_populates="tratamiento")
    servicios = relationship("Servicio", back_populates="tratamiento")


# ── TABLA: CITAS ───────────────────────────────────────────────────────────────

class Cita(Base):
    __tablename__ = "citas"

    id             = Column(Integer, primary_key=True, index=True)
    paciente_id    = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    odontologo_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tratamiento_id = Column(Integer, ForeignKey("tratamientos.id"), nullable=True)
    fecha_hora     = Column(String(50), nullable=False)   # ISO 8601 como string
    estado         = Column(String(30), default=EstadoCitaEnum.en_espera)
    notas          = Column(Text, nullable=True)
    creado_en      = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    paciente    = relationship("Usuario",     back_populates="citas_pac",
                               foreign_keys=[paciente_id])
    odontologo  = relationship("Usuario",     back_populates="citas_dr",
                               foreign_keys=[odontologo_id])
    tratamiento = relationship("Tratamiento", back_populates="citas")


# ── TABLA: SERVICIOS ADQUIRIDOS (historial del paciente) ───────────────────────

class Servicio(Base):
    __tablename__ = "servicios"

    id              = Column(Integer, primary_key=True, index=True)
    paciente_id     = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tratamiento_id  = Column(Integer, ForeignKey("tratamientos.id"), nullable=False)
    odontologo_id   = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    proxima_cita    = Column(String(80), nullable=True)
    estado_cuenta   = Column(String(30), default=EstadoCuentaEnum.pendiente)
    creado_en       = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    paciente    = relationship("Usuario",     back_populates="servicios",
                               foreign_keys=[paciente_id])
    tratamiento = relationship("Tratamiento", back_populates="servicios")


# ── TABLA: PROVEEDORES ─────────────────────────────────────────────────────────

class Proveedor(Base):
    __tablename__ = "proveedores"

    id               = Column(Integer, primary_key=True, index=True)
    empresa          = Column(String(150), nullable=False)
    contacto_asesor  = Column(String(120), nullable=True)
    telefono         = Column(String(30),  nullable=True)
    suministro       = Column(String(200), nullable=True)
    estado_convenio  = Column(String(30),  default=EstadoConvenioEnum.vigente)
    creado_en        = Column(DateTime(timezone=True), server_default=func.now())
