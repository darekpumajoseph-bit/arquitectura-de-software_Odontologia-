from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr, Field
import models
import schemas
from database import get_db
from utils import hash_password, validar_correo, generar_documento_unico

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# ── Modelo para el registro ──────────────────────────────────────────────────
class RegistroRequest(BaseModel):
    correo: EmailStr = Field(..., description="Correo electrónico del usuario")
    contrasena: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    nombre: str = Field(..., min_length=1, description="Nombre del paciente")
    apellido: str = Field(..., min_length=1, description="Apellido del paciente")
    telefono: str = Field(..., min_length=1, description="Teléfono del paciente")

# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[schemas.UsuarioOut])
def get_usuarios(db: Session = Depends(get_db)):
    """Obtener todos los usuarios"""
    return db.query(models.Usuario).all()


@router.get("/{id}", response_model=schemas.UsuarioOut)
def get_usuario(id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.get("/correo/{correo}", response_model=schemas.UsuarioOut)
def get_usuario_by_correo(correo: str, db: Session = Depends(get_db)):
    """Obtener un usuario por correo electrónico"""
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.post("/", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_usuario(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario (solo usuario, sin paciente asociado)
    """
    if not validar_correo(data.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico no tiene un formato válido"
        )
    
    existing_user = db.query(models.Usuario).filter(
        models.Usuario.correo == data.correo
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    if len(data.contrasena) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    roles_validos = ["Administrador", "Odontologo", "Paciente"]
    if data.rol not in roles_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol inválido. Debe ser uno de: {', '.join(roles_validos)}"
        )
    
    nuevo_usuario = models.Usuario(
        correo=data.correo,
        contrasena=hash_password(data.contrasena),
        rol=data.rol,
        estado=data.estado if hasattr(data, 'estado') else "Activo"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put("/{id}", response_model=schemas.UsuarioOut)
def update_usuario(id: int, data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Actualizar un usuario existente"""
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if not validar_correo(data.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico no tiene un formato válido"
        )
    
    otro = db.query(models.Usuario).filter(
        models.Usuario.correo == data.correo,
        models.Usuario.id_usuario != id
    ).first()
    if otro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado por otro usuario"
        )
    
    if len(data.contrasena) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    usuario.correo = data.correo
    usuario.contrasena = hash_password(data.contrasena)
    usuario.rol = data.rol
    usuario.estado = data.estado
    db.commit()
    db.refresh(usuario)
    return usuario


@router.patch("/{id}/estado")
def update_estado_usuario(id: int, estado: str, db: Session = Depends(get_db)):
    """Actualizar solo el estado de un usuario (Activo/Inactivo)"""
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if estado not in ["Activo", "Inactivo"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estado debe ser 'Activo' o 'Inactivo'"
        )
    
    usuario.estado = estado
    db.commit()
    return {
        "mensaje": f"Estado del usuario actualizado a '{estado}'",
        "id_usuario": usuario.id_usuario,
        "correo": usuario.correo,
        "estado": usuario.estado
    }


# ── DELETE EN CASCADA (ELIMINA USUARIO + PACIENTE ASOCIADO) ──────────────────
@router.delete("/{id}")
def delete_usuario(id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario y su paciente asociado (si existe)"""
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    try:
        # 1. Buscar pacientes asociados a este usuario
        pacientes = db.query(models.Paciente).join(
            models.usuario_paciente,
            models.usuario_paciente.c.id_paciente == models.Paciente.id_paciente
        ).filter(
            models.usuario_paciente.c.id_usuario == id
        ).all()
        
        # 2. Eliminar las relaciones usuario-paciente
        db.execute(
            models.usuario_paciente.delete().where(
                models.usuario_paciente.c.id_usuario == id
            )
        )
        
        # 3. Eliminar todos los pacientes asociados
        for paciente in pacientes:
            db.delete(paciente)
        
        # 4. Eliminar el usuario
        db.delete(usuario)
        
        db.commit()
        
        return {
            "mensaje": "Usuario eliminado correctamente",
            "pacientes_eliminados": len(pacientes),
            "id_usuario": id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar: {str(e)}"
        )


# ── Endpoint de registro completo (usuario + paciente) ─────────────────────
@router.post("/registro", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def registro_usuario(data: RegistroRequest, db: Session = Depends(get_db)):
    """
    Endpoint específico para registro desde el frontend.
    Recibe un JSON con correo, contrasena, nombre, apellido y telefono.
    Crea un usuario con rol 'Paciente' y también crea un paciente asociado.
    """
    if not validar_correo(data.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico no tiene un formato válido"
        )
    
    existing_user = db.query(models.Usuario).filter(
        models.Usuario.correo == data.correo
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    if len(data.contrasena) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    # 4. Crear el usuario (rol = Paciente)
    nuevo_usuario = models.Usuario(
        correo=data.correo,
        contrasena=hash_password(data.contrasena),
        rol="Paciente",
        estado="Activo"
    )
    db.add(nuevo_usuario)
    db.flush()
    
    # 5. Generar un documento único para el paciente
    documento = generar_documento_unico(db)
    
    # 6. Crear el paciente asociado
    nuevo_paciente = models.Paciente(
        nombre=data.nombre,
        apellido=data.apellido,
        documento=documento,
        telefono=data.telefono,
        correo=data.correo
    )
    db.add(nuevo_paciente)
    db.flush()
    
    # 7. Crear la relación usuario-paciente
    from models import usuario_paciente
    stmt = usuario_paciente.insert().values(
        id_usuario=nuevo_usuario.id_usuario,
        id_paciente=nuevo_paciente.id_paciente
    )
    db.execute(stmt)
    
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario