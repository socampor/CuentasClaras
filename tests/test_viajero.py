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
      self.cuentasClarasViajero = CuentasClaras()

      '''Abre la sesión'''
      self.sessionViajero = Session()

      '''Crea una instancia de Faker'''
      self.data_factory_viajero = Faker()

      '''Se programa para que Faker cree los mismos datos cuando se ejecuta'''
      Faker.seed(1000)

      '''Crea los objetos'''
      self.dataActividadesViajero = []
      self.dataViajerosViajero = []
      self.dataGastosViajero = []
      self.actividades_viajero = []
      self.viajerosViajero = []
      self.gastosViajero = []

      for i in range(0, 10):
          self.dataActividadesViajero.append(
              (
                  'Actividad ' + self.data_factory_viajero.unique.first_name_nonbinary(),
                  self.data_factory_viajero.boolean()
              )
          )
          self.actividades_viajero.append(
              Actividad(
                  nombre=self.dataActividadesViajero[-1][0],
                  terminada=self.dataActividadesViajero[-1][1],
                  viajeros=[],
                  gastos=[]
              )
          )

          self.dataViajerosViajero.append(
              (
                  self.data_factory_viajero.unique.name(),
                  self.data_factory_viajero.unique.random_int(1000000000, 2000000000)
              )
          )
          self.viajerosViajero.append(
              Viajero(
                  nombre=self.dataViajerosViajero[-1][0],
                  identificacion=self.dataViajerosViajero[-1][1],
                  gastos=[]
              )
          )

          self.sessionViajero.add(self.actividades_viajero[-1])
          self.sessionViajero.add(self.viajerosViajero[-1])

      '''Persiste los objetos'''
      self.sessionViajero.commit()

      for i in range(0, 30):
          self.dataGastosViajero.append(
              (
                  'Gasto ' + self.data_factory_viajero.unique.first_name_nonbinary(),
                  self.data_factory_viajero.random_int(1, 1000000),
                  self.data_factory_viajero.date_between()
              )
          )
          self.gastosViajero.append(
              Gasto(
                  concepto=self.dataGastosViajero[-1][0],
                  valor=self.dataGastosViajero[-1][1],
                  fecha=self.dataGastosViajero[-1][2]
              )
          )

      '''Relaciones'''
      cant_actividades = self.data_factory_viajero.random_int(2, 5)
      actividades_viajero = random.sample(self.actividades_viajero, cant_actividades)
      gastos_reg = []

      for actividad in actividades_viajero:
          cant_viajeros = self.data_factory_viajero.random_int(2, 5)
          viajeros_viajero = random.sample(self.viajerosViajero, cant_viajeros)
          actividad.viajeros = viajeros_viajero

          for viajero in actividad.viajeros:
              gasto = None
              while gasto == None:
                  choice = random.choice(self.gastosViajero)
                  if choice not in gastos_reg:
                      gasto = choice
              gastos_reg.append(gasto)
              viajero.gastos.append(gasto)
              actividad.gastos.append(gasto)

      '''Persiste los objetos y cierra la sesión'''
      self.sessionViajero.commit()
      '''En este setUp no se cierra la sesión para usar los datos en las pruebas'''
      # self.sessionViajero.close()

      self.actividadToTest = random.choice(actividades_viajero)

  def tearDown(self):
      '''Abre la sesión'''
      self.sessionViajero = Session()

      '''Consulta todos los álbumes'''
      busq_acti = self.sessionViajero.query(Actividad).all()
      busq_viaj = self.sessionViajero.query(Viajero).all()

      '''Borra todos los álbumes'''
      for actividad in busq_acti:
          self.sessionViajero.delete(actividad)

      '''Borra todos los álbumes'''
      for viajero in busq_viaj:
          self.sessionViajero.delete(viajero)

      self.sessionViajero.commit()
      self.sessionViajero.close()

  def test_constructor(self):
      for actividad, dato in zip(self.actividades_viajero, self.dataActividadesViajero):
          self.assertEqual(actividad.nombre, dato[0])
          self.assertEqual(actividad.terminada, dato[1])

      for viajero, dato in zip(self.viajerosViajero, self.dataViajerosViajero):
          self.assertEqual(viajero.nombre, dato[0])
          self.assertEqual(viajero.identificacion, dato[1])

      for gasto, dato in zip(self.gastosViajero, self.dataGastosViajero):
          self.assertEqual(gasto.concepto, dato[0])
          self.assertEqual(gasto.valor, dato[1])
          self.assertEqual(gasto.fecha, dato[2])

  def test_crear_viajero(self):
      nombre = self.data_factory_viajero.unique.name()
      identificacion = self.data_factory_viajero.unique.random_int(
          1000000000, 2000000000)
      nuevo_viajero = self.cuentasClarasViajero.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevo_viajero, True)

  def test_crear_viajero_sin_nombre(self):
      nombre = ""
      identificacion = self.data_factory_viajero.unique.random_int(
          1000000000, 2000000000)
      nuevo_viajero = self.cuentasClarasViajero.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevo_viajero, False)

  def test_crear_viajero_sin_identificacion(self):
      nombre = self.data_factory_viajero.unique.name()
      identificacion = ""
      nuevo_viajero = self.cuentasClarasViajero.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevo_viajero, False)

  def test_crear_viajero_id_repetido(self):
      nombre = self.data_factory_viajero.unique.name()
      identificacion = self.dataViajerosViajero[-1][1]
      nuevo_viajero = self.cuentasClarasViajero.crear_viajero(nombre, identificacion)
      self.assertEqual(nuevo_viajero, False)
