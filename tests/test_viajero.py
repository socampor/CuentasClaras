import unittest
import random
from src.logica.cuentas_claras import CuentasClaras
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.declarative_base import Session
from faker import Faker


class ViajeroTestCase(unittest.TestCase):

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

      for i in range(0, 10):
          self.dataActividades.append(
              (
                  'Actividad ' + self.data_factory.unique.first_name_nonbinary(),
                  self.data_factory.boolean()
              )
          )
          self.actividades.append(
              Actividad(
                  nombre=self.dataActividades[-1][0],
                  terminada=self.dataActividades[-1][1],
                  viajeros=[],
                  gastos=[]
              )
          )

          self.dataViajeros.append(
              (
                  self.data_factory.unique.name(),
                  self.data_factory.unique.random_int(1000000000, 2000000000)
              )
          )
          self.viajeros.append(
              Viajero(
                  nombre=self.dataViajeros[-1][0],
                  identificacion=self.dataViajeros[-1][1],
                  gastos=[]
              )
          )

          self.session.add(self.actividades[-1])
          self.session.add(self.viajeros[-1])

      '''Persiste los objetos'''
      self.session.commit()

      for i in range(0, 30):
          self.dataGastos.append(
              (
                  'Gasto ' + self.data_factory.unique.first_name_nonbinary(),
                  self.data_factory.random_int(1, 1000000),
                  self.data_factory.date_between()
              )
          )
          self.gastos.append(
              Gasto(
                  concepto=self.dataGastos[-1][0],
                  valor=self.dataGastos[-1][1],
                  fecha=self.dataGastos[-1][2]
              )
          )

      '''Relaciones'''
      cantActividades = self.data_factory.random_int(2, 5)
      actividades = random.sample(self.actividades, cantActividades)
      gastosReg = []

      for actividad in actividades:
          cantViajeros = self.data_factory.random_int(2, 5)
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

  def test_crear_viajero(self):
      nombre = self.data_factory.unique.name()
      identificacion = self.data_factory.unique.random_int(
          1000000000, 2000000000)
      nuevoViajero = self.cuentasClaras.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevoViajero, True)

  def test_crear_viajero_sin_nombre(self):
      nombre = ""
      identificacion = self.data_factory.unique.random_int(
          1000000000, 2000000000)
      nuevoViajero = self.cuentasClaras.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevoViajero, False)

  def test_crear_viajero_sin_identificacion(self):
      nombre = self.data_factory.unique.name()
      identificacion = ""
      nuevoViajero = self.cuentasClaras.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevoViajero, False)

  def test_crear_viajero_id_repetido(self):
      nombre = self.data_factory.unique.name()
      identificacion = self.dataViajeros[-1][1]
      nuevoViajero = self.cuentasClaras.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevoViajero, False)
