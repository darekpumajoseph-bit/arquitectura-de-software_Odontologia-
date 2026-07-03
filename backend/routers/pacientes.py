from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.get("/", response_model=List[schemas.PacienteOut])
def get_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@router.get("/{id}", response_model=schemas.PacienteOut)
def get_paciente(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return p

@router.post("/", response_model=schemas.PacienteOut, status_code=201)
def create_paciente(data: schemas.PacienteCreate, db: Session = Depends(get_db)):
    if db.query(models.Paciente).filter(models.Paciente.documento == data.documento).first():
        raise HTTPException(status_code=400, detail="Documento ya registrado")
    nuevo = models.Paciente(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id}", response_model=schemas.PacienteOut)
def update_paciente(id: int, data: schemas.PacienteCreate, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    for k, v in data.model_dump().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{id}")
def delete_paciente(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.delete(p)
    db.commit()
    return {"mensaje": "Paciente eliminado correctamente"}