from src.modelo.actividad import Actividad, ViajeroActividad
from src.modelo.gasto import Gasto
from src.modelo.gastos_viaj_act import GastosViajeroActividad
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import engine, Base, session
from datetime import datetime, date
import numpy as np

class CuentasClaras():

  def __init__(self) -> None:
    Base.metadata.create_all(engine)
    self.actividades = self.dar_actividades()
    self.viajeros = self.dar_viajeros()

  def dar_actividad(self, nombreActividad):
    actividad = session.query(Actividad).filter_by(nombre = nombreActividad).first()
    return actividad

  def dar_actividades(self):
    actividades = [elem for elem in session.query(Actividad).order_by(Actividad.nombre).all()]
    return actividades

  def dar_viajero(self, nombreViajero):
    viajero = session.query(Viajero).filter_by(nombre = nombreViajero).first()
    return viajero

  def dar_viajero_id(self, idViajero):
    viajero = session.query(Viajero).filter_by(id = idViajero).first()
    return viajero

  def dar_viajeros(self):
    viajeros = [elem for elem in session.query(Viajero).order_by(Viajero.nombre).all()]
    return viajeros

  def dar_gasto_act(self, nombreActividad):
    actividad = session.query(Actividad).filter_by(nombre = nombreActividad).first()
    return actividad.gastos

  def dar_reporte_comp_act(self, nombreActividad):
    actividad = session.query(Actividad).filter_by(nombre = nombreActividad).first()
    gastosPorViajeros=[]
    nombresViajeros=[""]
    for viajero in actividad.viajeros:
      totalGastoViajero=0
      nombresViajeros.append(viajero.nombre)
      for gasto in viajero.gastos:
        totalGastoViajero += gasto.valor
      gastosPorViajeros.append(totalGastoViajero)
    totalGasto=sum([gasto for gasto in gastosPorViajeros])
    # Numerototal de viajeros en la actividad
    numViajeros=len(actividad.viajeros)
    #Gasto total de total de la actividad reartido equitativamente entre el numero de viajeros
    gastoEqual=totalGasto/numViajeros
    #Array que muestra la diferencia de gastos entre gastosPorViajero y gastoEqual
    #Numeros <0 deben, los numeros >0 aportaron de mas, =0 no deben
    difGastos=[gasto-gastoEqual for gasto in gastosPorViajeros]
    totDeuda=sum([gasto for gasto in difGastos if gasto>=0])
    #Array que calcula el porcentaje que cada  viajero debe en realacion a gastoEqual
    perCompensacion= [(round(gasto/totDeuda,5) if gasto>0 else 0) for gasto in difGastos ]

    difDebe=[(-gasto if gasto<0 else 0)for gasto in difGastos]

    #Matriz diagonal con -1.0
    matVal=np.diag(np.full(len(gastosPorViajeros),-1.0))

    for i in range(len(difDebe)):
      for j in range(len(perCompensacion)):
        if(i!=j):
          matVal[i][j]=round((difDebe[i]*perCompensacion[j]),2)

    #Convierte matVal en tipo list y almacena la data en MatrizData
    matrizData=matVal.tolist()

    #Crea la matriz que se imprime en pantalla
    matriz=[[]]
    for i in range(len(matrizData)):
      matriz.append([0])
      i+=1
    for i in range(0,len(perCompensacion)+1):
      if i == 0:
        matriz[i][:]=nombresViajeros[:]
      else:
        matriz[i][0]=nombresViajeros[i]
        for j in range(0,len(difDebe)):
          matriz[i].append(matrizData[i-1][j])
    return matriz

  def crear_actividad(self, nombreActividad):
    if nombreActividad != '':
      busqueda = session.query(Actividad).filter_by(nombre = nombreActividad).all()
      if len(busqueda) == 0:
          actividad = Actividad(nombre = nombreActividad, terminada = False, viajeros = [], gastos = [])
          session.add(actividad)
          session.commit()
          return True
      else:
          return False
    else:
      return False

  def crear_viajero(self,newNombre,newIdentificacion ):
    if newNombre=="" or newIdentificacion=="":
      return False
    busquedaId = session.query(Viajero).filter_by(identificacion=newIdentificacion).all()
    if len(busquedaId)==0:
        nuevoViajero=Viajero(nombre=newNombre,identificacion=newIdentificacion)
        session.add(nuevoViajero)
        session.commit()
        return True
    else:
        return False

  def dar_reporte_gastos_viaj_act(self, nombreActividad, concepto):
    actividad = session.query(Actividad).filter_by(nombre = nombreActividad).first()
    gastViajAct = []
    for viajero in actividad.viajeros:
      totalViaj = sum(g.valor for g in viajero.gastos)
      gastoViaj = GastosViajeroActividad(viajero.nombre, concepto, totalViaj)
      gastViajAct.append(gastoViaj)
    gastViajAct.sort(key=lambda x: x.valor, reverse=True)
    return gastViajAct

  def agregar_viajero_actividad(self,identificacionViajero,nombreActividad):
    busqueda = session.query(Actividad).filter(Actividad.viajeros.any(Viajero.identificacion.in_([identificacionViajero])),
                                                         Actividad.nombre == nombreActividad).all()
    if len(busqueda)==0:
      actividad=session.query(Actividad).filter_by(nombre=nombreActividad).first()
      viajero=session.query(Viajero).filter_by(identificacion=identificacionViajero).first()
      actividad.viajeros.append(viajero)
      session.commit()
      return True
    else:
      return False

  def agregar_gasto_actividad(self,concepto, valor, fecha, viajero_nombre,nombreActividad):
    actividad=self.dar_actividad(nombreActividad)
    busqueda = session.query(Gasto).filter_by(concepto=concepto,actividad=actividad.id).all()
    if len(busqueda)==0:
      viajero=self.dar_viajero(viajero_nombre)
      day,month,year = fecha.split('-')
      dtmFecha = datetime(int(year), int(month), int(day))
      gasto= Gasto(concepto=concepto,valor=valor,fecha=dtmFecha.date())
      viajero.gastos.append(gasto)
      actividad.gastos.append(gasto)
      session.commit()
      return True
    else:
      return False

  def editar_actividad(self,oldNombre,newNombre):
    if newNombre!="":
      busqueda = session.query(Actividad).filter_by(nombre=newNombre).all()
      if len(busqueda)==0:
        actividad=self.dar_actividad(oldNombre)
        actividad.nombre=newNombre
        session.commit()
        return True
      else:
        return False
    else:
      return False

  def editar_gasto_actividad(self, id, concepto, valor, fecha, nombreViajero, nombreActividad):
    if concepto != "":
      actividad=self.dar_actividad(nombreActividad)
      viajero = self.dar_viajero(nombreViajero)
      day,month,year = fecha.split('-')
      dtmFecha = datetime(int(year), int(month), int(day))
      busqueda = session.query(Gasto).filter_by(fecha=dtmFecha.date(),concepto=concepto,actividad=actividad.id,valor=valor,viajero=viajero.id).all()
      if len(busqueda)==0:
        gasto = session.query(Gasto).filter_by(id = id).first()
        gasto.concepto = concepto
        gasto.valor = valor
        gasto.fecha = dtmFecha
        if viajero.id != gasto.viajero:
          gasto.viajero = viajero.id

        session.commit()
        return True
      else:
        return False
    else:
        return False