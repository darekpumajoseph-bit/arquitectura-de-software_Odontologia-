from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import hashlib
import models, schemas
from database import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def hash_password(password: str) -> str:
    """Hash simple SHA-256. En producción usa bcrypt o passlib."""
    return hashlib.sha256(password.encode()).hexdigest()


@router.get("/", response_model=List[schemas.UsuarioOut])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


@router.get("/{id}", response_model=schemas.UsuarioOut)
def get_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=schemas.UsuarioOut, status_code=201)
def create_usuario(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar correo duplicado
    if db.query(models.Usuario).filter(models.Usuario.correo == data.correo).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    # Verificar identificación duplicada
    if db.query(models.Usuario).filter(models.Usuario.identificacion == data.identificacion).first():
        raise HTTPException(status_code=400, detail="La identificación ya está registrada")

    nuevo = models.Usuario(
        nombre=data.nombre,
        correo=data.correo,
        identificacion=data.identificacion,
        estado=data.estado,
        rol_id=data.rol_id,
        password_hash=hash_password(data.password)
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id}", response_model=schemas.UsuarioOut)
def update_usuario(id: int, data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre         = data.nombre
    usuario.correo         = data.correo
    usuario.identificacion = data.identificacion
    usuario.estado         = data.estado
    usuario.rol_id         = data.rol_id
    usuario.password_hash  = hash_password(data.password)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id}")
def delete_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}
