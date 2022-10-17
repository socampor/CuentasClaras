from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Actividad (Base):
    __tablename__='actividad'

    id=Column(Integer,primary_key=True)
    nombre=Column(String(100),nullable=False,unique=True)
    terminada=Column(Boolean,default=False)
    viajeros=relationship('Viajero',secondary='viajero_actividad')
    gastos=relationship('Gasto', cascade='all, delete, delete-orphan')

class ViajeroActividad(Base):
     __tablename__='viajero_actividad'
    
     actividad_id= Column(
         Integer,
         ForeignKey('actividad.id'),
         primary_key=True)

     viajero_id= Column(
         Integer,
         ForeignKey('viajero.id'),
         primary_key=True)
     