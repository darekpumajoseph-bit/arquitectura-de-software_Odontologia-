from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import models
from database import get_db
from utils import hash_password, verificar_password  # <-- Importar ambas

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# ── Modelos Pydantic ──────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class LoginResponse(BaseModel):
    id_usuario: int
    correo: str
    rol: str
    estado: str
    mensaje: str

# ── Endpoint de login ─────────────────────────────────────────────────────────

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autenticar usuario con correo y contraseña.
    """
    # 1. Buscar usuario por correo
    usuario = db.query(models.Usuario).filter(
        models.Usuario.correo == data.correo
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Correo no registrado"
        )
    
    # ── LOGS DE DEPURACIÓN MEJORADOS ──────────────────────────────────────
    print("=" * 70)
    print(f"🔍 Usuario encontrado: {usuario.correo}")
    print(f"🔑 Hash almacenado en BD: {usuario.contrasena}")
    print(f"🔑 Hash calculado para '{data.contrasena}': {hash_password(data.contrasena)}")
    print(f"📏 Longitud de la contraseña ingresada: {len(data.contrasena)}")
    print(f"✅ ¿Coinciden? {verificar_password(data.contrasena, usuario.contrasena)}")
    print("=" * 70)
    # ─────────────────────────────────────────────────────────────────────

    # 2. Verificar contraseña usando la función unificada
    if not verificar_password(data.contrasena, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )
    
    # 3. Verificar que el usuario esté activo
    if usuario.estado != "Activo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador."
        )
    
    # 4. Login exitoso
    return LoginResponse(
        id_usuario=usuario.id_usuario,
        correo=usuario.correo,
        rol=usuario.rol,
        estado=usuario.estado,
        mensaje="Login exitoso"
    )