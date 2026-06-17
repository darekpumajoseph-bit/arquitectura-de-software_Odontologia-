from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])


@router.get("/", response_model=List[schemas.TratamientoOut])
def get_tratamientos(db: Session = Depends(get_db)):
    return db.query(models.Tratamiento).all()


@router.get("/{id}", response_model=schemas.TratamientoOut)
def get_tratamiento(id: int, db: Session = Depends(get_db)):
    t = db.query(models.Tratamiento).filter(models.Tratamiento.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return t


@router.post("/", response_model=schemas.TratamientoOut, status_code=201)
def create_tratamiento(data: schemas.TratamientoCreate, db: Session = Depends(get_db)):
    nuevo = models.Tratamiento(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id}", response_model=schemas.TratamientoOut)
def update_tratamiento(id: int, data: schemas.TratamientoCreate, db: Session = Depends(get_db)):
    t = db.query(models.Tratamiento).filter(models.Tratamiento.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    for k, v in data.model_dump().items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{id}")
def delete_tratamiento(id: int, db: Session = Depends(get_db)):
    t = db.query(models.Tratamiento).filter(models.Tratamiento.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    db.delete(t)
    db.commit()
    return {"mensaje": "Tratamiento eliminado correctamente"}
