# models.py - Versión actualizada con correo

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Time, Numeric, TIMESTAMP, Table
from sqlalchemy.orm import relationship
from database import Base

# ── TABLAS DE RELACIÓN MANY-TO-MANY ──────────────────────────────────────────

usuario_paciente = Table(
    "usuario_paciente",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("id_paciente", Integer, ForeignKey("paciente.id_paciente"), primary_key=True),
    extend_existing=True
)

usuario_tratamiento = Table(
    "usuario_tratamiento",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("id_tratamiento", Integer, ForeignKey("tratamiento.id_tratamiento"), primary_key=True),
    extend_existing=True
)


# ── TABLA: USUARIO ────────────────────────────────────────────────────────────

class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {'extend_existing': True}

    id_usuario = Column(Integer, primary_key=True, index=True)
    correo = Column(String(100), nullable=False, unique=True)  # <-- Cambiado de username a correo
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(30), nullable=False)
    estado = Column(String(20), nullable=False)

    pacientes = relationship("Paciente", secondary=usuario_paciente, back_populates="usuarios")
    tratamientos = relationship("Tratamiento", secondary=usuario_tratamiento, back_populates="usuarios")


# ── TABLA: PACIENTE ────────────────────────────────────────────────────────────

class Paciente(Base):
    __tablename__ = "paciente"
    __table_args__ = {'extend_existing': True}

    id_paciente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    genero = Column(String(20), nullable=True)
    direccion = Column(String(200), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True)  # <-- Este es el correo del paciente
    eps = Column(String(100), nullable=True)
    alergias = Column(Text, nullable=True)

    usuarios = relationship("Usuario", secondary=usuario_paciente, back_populates="pacientes")
    historias = relationship("HistoriaClinica", back_populates="paciente")
    citas = relationship("Cita", back_populates="paciente")


# ── TABLA: CONSULTORIO ────────────────────────────────────────────────────────

class Consultorio(Base):
    __tablename__ = "consultorio"
    __table_args__ = {'extend_existing': True}

    id_consultorio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(150), nullable=True)
    numero_sala = Column(String(20), nullable=True)

    odontologos = relationship("Odontologo", back_populates="consultorio")
    citas = relationship("Cita", back_populates="consultorio")


# ── TABLA: ODONTOLOGO ─────────────────────────────────────────────────────────

class Odontologo(Base):
    __tablename__ = "odontologo"
    __table_args__ = {'extend_existing': True}

    id_odontologo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True)
    especialidad = Column(String(100), nullable=True)
    registro_profesional = Column(String(50), nullable=True)
    horario = Column(String(100), nullable=True)
    id_consultorio = Column(Integer, ForeignKey("consultorio.id_consultorio"), nullable=False)

    consultorio = relationship("Consultorio", back_populates="odontologos")
    citas = relationship("Cita", back_populates="odontologo")


# ── TABLA: HISTORIA CLINICA ──────────────────────────────────────────────────

class HistoriaClinica(Base):
    __tablename__ = "historia_clinica"
    __table_args__ = {'extend_existing': True}

    id_historia = Column(Integer, primary_key=True, index=True)
    fecha_apertura = Column(Date, nullable=False)
    antecedentes = Column(Text, nullable=True)
    diagnostico_general = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)
    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente"), nullable=False)

    paciente = relationship("Paciente", back_populates="historias")


# ── TABLA: CITA ──────────────────────────────────────────────────────────────

class Cita(Base):
    __tablename__ = "cita"
    __table_args__ = {'extend_existing': True}

    id_cita = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    estado = Column(String(30), nullable=True)
    motivo_consulta = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)
    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente"), nullable=False)
    id_odontologo = Column(Integer, ForeignKey("odontologo.id_odontologo"), nullable=False)
    id_consultorio = Column(Integer, ForeignKey("consultorio.id_consultorio"), nullable=False)

    paciente = relationship("Paciente", back_populates="citas")
    odontologo = relationship("Odontologo", back_populates="citas")
    consultorio = relationship("Consultorio", back_populates="citas")
    tratamientos = relationship("Tratamiento", back_populates="cita")
    recordatorios = relationship("Recordatorio", back_populates="cita")
    pagos = relationship("Pago", back_populates="cita")


# ── TABLA: TRATAMIENTO ────────────────────────────────────────────────────────

class Tratamiento(Base):
    __tablename__ = "tratamiento"
    __table_args__ = {'extend_existing': True}

    id_tratamiento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    costo = Column(Numeric(10, 2), nullable=True)
    duracion_estimada = Column(String(100), nullable=True)
    id_cita = Column(Integer, ForeignKey("cita.id_cita"), nullable=False)

    cita = relationship("Cita", back_populates="tratamientos")
    usuarios = relationship("Usuario", secondary=usuario_tratamiento, back_populates="tratamientos")


# ── TABLA: RECORDATORIO ──────────────────────────────────────────────────────

class Recordatorio(Base):
    __tablename__ = "recordatorio"
    __table_args__ = {'extend_existing': True}

    id_recordatorio = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=True)
    fecha_envio = Column(TIMESTAMP, nullable=True)
    estado = Column(String(30), nullable=True)
    id_cita = Column(Integer, ForeignKey("cita.id_cita"), nullable=False)

    cita = relationship("Cita", back_populates="recordatorios")


# ── TABLA: PAGO ──────────────────────────────────────────────────────────────

class Pago(Base):
    __tablename__ = "pago"
    __table_args__ = {'extend_existing': True}

    id_pago = Column(Integer, primary_key=True, index=True)
    fecha_pago = Column(Date, nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(String(50), nullable=True)
    estado_pago = Column(String(30), nullable=True)
    referencia = Column(String(100), nullable=True)
    id_cita = Column(Integer, ForeignKey("cita.id_cita"), nullable=False)

    cita = relationship("Cita", back_populates="pagos")
    factura = relationship("Factura", back_populates="pago", uselist=False)


# ── TABLA: FACTURA ───────────────────────────────────────────────────────────

class Factura(Base):
    __tablename__ = "factura"
    __table_args__ = {'extend_existing': True}

    id_factura = Column(Integer, primary_key=True, index=True)
    fecha_emision = Column(Date, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=True)
    impuesto = Column(Numeric(10, 2), nullable=True)
    total = Column(Numeric(10, 2), nullable=True)
    id_pago = Column(Integer, ForeignKey("pago.id_pago"), unique=True, nullable=False)

    pago = relationship("Pago", back_populates="factura")