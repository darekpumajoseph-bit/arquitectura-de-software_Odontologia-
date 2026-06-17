from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base de datos SQLite — el archivo se crea automáticamente en la raíz del backend
DATABASE_URL = "sqlite:///./odontosoft.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependencia reutilizable para inyectar la sesión en cada ruta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
