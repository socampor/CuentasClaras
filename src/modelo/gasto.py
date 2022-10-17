from sqlalchemy import Column, Integer, String, Float,Date, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Gasto (Base):
    __tablename__='gasto'

    id=Column(Integer,primary_key=True)
    concepto=Column(String(250),nullable=False)
    valor=Column(Float,nullable=False)
    fecha=Column(Date)
    
    viajero= Column(Integer,ForeignKey('viajero.id'))    
    actividad = Column(Integer, ForeignKey('actividad.id'))