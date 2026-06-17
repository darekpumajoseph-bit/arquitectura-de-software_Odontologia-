from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.get("/", response_model=List[schemas.CitaOut])
def get_citas(db: Session = Depends(get_db)):
    return db.query(models.Cita).all()


@router.get("/{id}", response_model=schemas.CitaOut)
def get_cita(id: int, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


@router.get("/paciente/{paciente_id}", response_model=List[schemas.CitaOut])
def get_citas_por_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return db.query(models.Cita).filter(models.Cita.paciente_id == paciente_id).all()


@router.get("/odontologo/{odontologo_id}", response_model=List[schemas.CitaOut])
def get_citas_por_odontologo(odontologo_id: int, db: Session = Depends(get_db)):
    return db.query(models.Cita).filter(models.Cita.odontologo_id == odontologo_id).all()


@router.post("/", response_model=schemas.CitaOut, status_code=201)
def create_cita(data: schemas.CitaCreate, db: Session = Depends(get_db)):
    nueva = models.Cita(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{id}", response_model=schemas.CitaOut)
def update_cita(id: int, data: schemas.CitaCreate, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    for k, v in data.model_dump().items():
        setattr(cita, k, v)
    db.commit()
    db.refresh(cita)
    return cita


@router.patch("/{id}/estado")
def update_estado_cita(id: int, estado: str, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita.estado = estado
    db.commit()
    return {"mensaje": f"Estado actualizado a '{estado}'"}


@router.delete("/{id}")
def delete_cita(id: int, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return {"mensaje": "Cita eliminada correctamente"}
