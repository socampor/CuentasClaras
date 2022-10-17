import unittest
import random
from unittest import result
from src.logica.cuentas_claras import CuentasClaras
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.declarative_base import Session
from faker import Faker

class ActividadTestCase(unittest.TestCase):

  def setUp(self):
    '''Crea una cuenta clara para hacer las pruebas'''
    self.cuentasClaras = CuentasClaras()

    '''Abre la sesión'''
    self.session = Session()

    '''Crea una instancia de Faker'''
    self.data_factory = Faker()

    '''Se programa para que Faker cree los mismos datos cuando se ejecuta'''
    Faker.seed(1000)

    '''Crea los objetos'''
    self.dataActividades = []
    self.dataViajeros = []
    self.dataGastos = []
    self.actividades = []
    self.viajeros = []
    self.gastos = []

    for i in range(0,10):
      self.dataActividades.append(
        (
          'Actividad ' + self.data_factory.unique.first_name_nonbinary(),
          self.data_factory.boolean()
        )
      )
      self.actividades.append(
        Actividad(
          nombre = self.dataActividades[-1][0],
          terminada = self.dataActividades[-1][1],
          viajeros = [],
          gastos = []
        )
      )

      self.dataViajeros.append(
        (
          self.data_factory.unique.name(),
          self.data_factory.unique.random_int(1000000000,2000000000)
        )
      )
      self.viajeros.append(
        Viajero(
          nombre = self.dataViajeros[-1][0],
          identificacion = self.dataViajeros[-1][1],
          gastos = []
        )
      )

      self.session.add(self.actividades[-1])
      self.session.add(self.viajeros[-1])

    '''Persiste los objetos'''
    self.session.commit()

    for i in range(0,30):
      self.dataGastos.append(
        (
          'Gasto ' + self.data_factory.unique.first_name_nonbinary(),
          self.data_factory.random_int(1,1000000),
          self.data_factory.date_between()
        )
      )
      self.gastos.append(
        Gasto(
          concepto = self.dataGastos[-1][0],
          valor = self.dataGastos[-1][1],
          fecha = self.dataGastos[-1][2]
        )
      )

    '''Relaciones'''
    cantActividades = self.data_factory.random_int(2,5)
    actividades = random.sample(self.actividades, cantActividades)
    gastosReg = []

    for actividad in actividades:
      cantViajeros = self.data_factory.random_int(2,5)
      viajeros = random.sample(self.viajeros, cantViajeros)
      actividad.viajeros = viajeros

      for viajero in actividad.viajeros:
        gasto = None
        while gasto == None:
          choice = random.choice(self.gastos)
          if choice not in gastosReg:
            gasto = choice
        gastosReg.append(gasto)
        viajero.gastos.append(gasto)
        actividad.gastos.append(gasto)

    '''Persiste los objetos y cierra la sesión'''
    self.session.commit()
    '''En este setUp no se cierra la sesión para usar los datos en las pruebas'''
    # self.session.close()

    self.actividadToTest = random.choice(actividades)

  def tearDown(self):
    '''Abre la sesión'''
    self.session = Session()

    '''Consulta todos los álbumes'''
    busqActi = self.session.query(Actividad).all()
    busqViaj = self.session.query(Viajero).all()

    '''Borra todos los álbumes'''
    for actividad in busqActi:
        self.session.delete(actividad)

    '''Borra todos los álbumes'''
    for viajero in busqViaj:
        self.session.delete(viajero)

    self.session.commit()
    self.session.close()

  def test_constructor(self):
    for actividad, dato in zip(self.actividades, self.dataActividades):
      self.assertEqual(actividad.nombre, dato[0])
      self.assertEqual(actividad.terminada, dato[1])

    for viajero, dato in zip(self.viajeros, self.dataViajeros):
      self.assertEqual(viajero.nombre, dato[0])
      self.assertEqual(viajero.identificacion, dato[1])

    for gasto, dato in zip(self.gastos, self.dataGastos):
      self.assertEqual(gasto.concepto, dato[0])
      self.assertEqual(gasto.valor, dato[1])
      self.assertEqual(gasto.fecha, dato[2])

  def test_dar_actividades(self):
    consulta1=self.cuentasClaras.dar_actividades()
    nuevaActividad= Actividad(nombre = "Actividad 4", terminada = False, viajeros = [], gastos = [])

    '''Adiciona los objetos a la sesión'''
    self.session.add(nuevaActividad)

    '''Persiste los objetos y cierra la sesión'''
    self.session.commit()
    self.session.close()

    consulta2=self.cuentasClaras.dar_actividades()
    self.assertGreaterEqual(len(consulta2), len(consulta1))

  def test_dar_gastos_actividad(self):
    consulta = self.cuentasClaras.dar_gasto_act(self.actividadToTest.nombre)
    self.assertEqual(len(self.actividadToTest.gastos), len(consulta))

  def test_dar_reporte_comp(self):
    reporte = self.cuentasClaras.dar_reporte_comp_act(self.actividadToTest.nombre)
    self.assertEqual(len(self.actividadToTest.viajeros) + 1, len(reporte))

  def test_crear_actividad(self):
    resultado = self.cuentasClaras.crear_actividad('Actividad ' + self.data_factory.unique.first_name_nonbinary())
    self.assertEqual(resultado, True)

  def test_crear_actividad_existente(self):
    resultado = self.cuentasClaras.crear_actividad(self.actividades[-1].nombre)
    self.assertEqual(resultado, False)

  def test_crear_actividad_vacia(self):
    resultado = self.cuentasClaras.crear_actividad('')
    self.assertEqual(resultado, False)

  def test_dar_reporte_gastos_viaj_act(self):
    reporte = self.cuentasClaras.dar_reporte_gastos_viaj_act(self.actividadToTest.nombre, 'Gastos consolidados')
    self.assertEqual(len(self.actividadToTest.viajeros), len(reporte))

  def test_dar_reporte_gastos_viaj_act_ord(self):
    gastViajAct = []
    for viajero in self.actividadToTest.viajeros:
      totalViaj = sum(g.valor for g in viajero.gastos)
      gastViajAct.append(totalViaj)
    gastViajAct.sort(reverse=True)
    reporte = self.cuentasClaras.dar_reporte_gastos_viaj_act(self.actividadToTest.nombre, 'Gastos consolidados')
    self.assertEqual(gastViajAct[-1], reporte[-1].valor)

  def test_agregar_viajero_actividad(self):
    nombreNuevaActividad='Nueva Actividad ' + self.data_factory.unique.first_name_nonbinary()
    self.cuentasClaras.crear_actividad(nombreNuevaActividad)
    viajeroSelec=random.choice(self.dataViajeros)
    identificacion=viajeroSelec[1]
    self.cuentasClaras.agregar_viajero_actividad(identificacion,nombreNuevaActividad)
    identificacionViajeroNuevaActividad = self.session.query(Actividad).filter(Actividad.nombre==nombreNuevaActividad).first().viajeros[-1].identificacion
    self.assertEqual(identificacionViajeroNuevaActividad,identificacion)

  def test_agregar_viajero_repetido_actividad(self):
    nombreActividad=self.actividadToTest.nombre
    identificacion=self.session.query(Actividad).filter(Actividad.nombre==nombreActividad).first().viajeros[-1].identificacion
    resultado=self.cuentasClaras.agregar_viajero_actividad(identificacion,nombreActividad)
    self.assertEqual(resultado,False)

  def test_agregar_gasto_actividad(self):
    viajero = random.choice(self.actividadToTest.viajeros)
    consulta0=self.cuentasClaras.dar_gasto_act(self.actividadToTest.nombre)
    resultado = self.cuentasClaras.agregar_gasto_actividad('Gasto ' + self.data_factory.unique.first_name_nonbinary(), self.data_factory.random_int(1,1000000), self.data_factory.date_between().strftime("%d-%m-%Y"), viajero.nombre, self.actividadToTest.nombre)
    consulta = self.cuentasClaras.dar_gasto_act(self.actividadToTest.nombre)
    self.assertEqual(resultado, True)
    self.assertNotEqual(len(consulta0), len(consulta))

  def test_agregar_gasto_actividad_repetido(self):
    viajero = random.choice(self.actividadToTest.viajeros)
    gasto = self.actividadToTest.gastos[-1]
    resultado = self.cuentasClaras.agregar_gasto_actividad(gasto.concepto, gasto.valor, gasto.fecha.strftime("%d-%m-%Y"), viajero.nombre, self.actividadToTest.nombre)
    self.assertEqual(resultado, False)

  def test_editar_actividad(self):
    actividad=self.actividadToTest
    oldNombre=actividad.nombre
    actividad_id=actividad.id
    newNombre='Nuevo Nombre ' + self.data_factory.unique.first_name_nonbinary()
    self.cuentasClaras.editar_actividad(oldNombre,newNombre)
    consulta_id=self.cuentasClaras.dar_actividad(newNombre).id
    self.assertEqual(actividad_id,consulta_id)

  def test_editar_actividad_vacio(self):
    actividad=self.actividadToTest
    oldNombre=actividad.nombre
    newNombre=""
    consulta=self.cuentasClaras.editar_actividad(oldNombre,newNombre)
    self.assertFalse(consulta)

  def test_editar_actividad_nombre_repetido(self):
    actividad=self.actividadToTest
    oldNombre=actividad.nombre
    newNombre="Nombre repetido"
    self.cuentasClaras.crear_actividad(newNombre)
    consulta=self.cuentasClaras.editar_actividad(oldNombre,newNombre)
    self.assertFalse(consulta)

  def test_editar_gasto(self):
    gasto = self.actividadToTest.gastos[-1]
    viajero = self.cuentasClaras.dar_viajero_id(gasto.viajero)
    nuevoConcepto = 'Nuevo concepto ' + self.data_factory.unique.first_name_nonbinary()
    nuevoValor = self.data_factory.random_int(1,1000000)
    nuevaFecha = self.data_factory.date_between().strftime("%d-%m-%Y")
    resultado = self.cuentasClaras.editar_gasto_actividad(gasto.id, nuevoConcepto, nuevoValor, nuevaFecha, viajero.nombre, self.actividadToTest.nombre)
    actividad = self.cuentasClaras.dar_actividad(self.actividadToTest.nombre)
    gastoEditado = False
    for gasto_act in actividad.gastos:
      if gasto_act.id == gasto.id:
        gastoEditado = ((gasto_act.concepto != gasto.concepto) and (gasto_act.valor != gasto.valor) and (gasto_act.fecha != gasto.fecha))
    self.assertEqual(resultado, True)
    self.assertEqual(gastoEditado, True)

  def test_editar_gasto_cambio_viajero(self):
    gasto = self.actividadToTest.gastos[-1]
    viajero = random.choice(self.actividadToTest.viajeros)
    while viajero.id == gasto.viajero:
      viajero = random.choice(self.actividadToTest.viajeros)
    cantGastos = len(viajero.gastos)
    nuevoConcepto = 'Nuevo concepto ' + self.data_factory.unique.first_name_nonbinary()
    nuevoValor = self.data_factory.random_int(1,1000000)
    nuevaFecha = self.data_factory.date_between().strftime("%d-%m-%Y")
    resultado = self.cuentasClaras.editar_gasto_actividad(gasto.id, nuevoConcepto, nuevoValor, nuevaFecha, viajero.nombre, self.actividadToTest.nombre)
    consulta = self.cuentasClaras.dar_viajero_id(viajero.id)
    self.assertEqual(resultado, True)
    self.assertNotEqual(cantGastos, len(consulta.gastos))

  def test_editar_gasto_repetido(self):
    gasto = self.actividadToTest.gastos[-1]
    viajero = self.cuentasClaras.dar_viajero_id(gasto.viajero)
    resultado = self.cuentasClaras.editar_gasto_actividad(gasto.id, gasto.concepto, gasto.valor, gasto.fecha.strftime("%d-%m-%Y"), viajero.nombre, self.actividadToTest.nombre)
    self.assertEqual(resultado, False)

  def test_editar_gasto_vacio(self):
    gasto = self.actividadToTest.gastos[-1]
    viajero = self.cuentasClaras.dar_viajero_id(gasto.viajero)
    resultado = self.cuentasClaras.editar_gasto_actividad(gasto.id, "", gasto.valor, gasto.fecha.strftime("%d-%m-%Y"), viajero.nombre, self.actividadToTest.nombre)
    self.assertEqual(resultado, False)