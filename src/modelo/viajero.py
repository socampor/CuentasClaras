from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Viajero(Base):
    __tablename__='viajero'

    id=Column(Integer,primary_key=True)
    nombre=Column(String(250),nullable=False)
    identificacion=Column(Integer,nullable=False, unique=True)
    actividades = relationship('Actividad', secondary='viajero_actividad')
    gastos=relationship('Gasto', cascade='all, delete, delete-orphan')
