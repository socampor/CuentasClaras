from PyQt5.QtWidgets import QApplication
from .Vista_lista_actividades import Vista_lista_actividades
from .Vista_lista_viajeros import Vista_lista_viajeros
from .Vista_actividad import Vista_actividad
from .Vista_reporte_compensacion import Vista_reporte_compensacion
from .Vista_reporte_gastos import Vista_reporte_gastos_viajero


class App_CuentasClaras(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_CuentasClaras, self).__init__(sys_argv)

        self.logica = logica
        self.mostrar_vista_lista_actividades()

    def mostrar_vista_lista_actividades(self):
        """
        Esta función inicializa la ventana de la lista de actividades
        """
        self.vista_lista_actividades = Vista_lista_actividades(self)
        self.vista_lista_actividades.mostrar_actividades(
            self.logica.actividades)

    def insertar_actividad(self, nombre):
        """
        Esta función inserta una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.crear_actividad(nombre)
        actividad = self.logica.dar_actividad(nombre)
        self.logica.actividades.append(actividad)
        self.vista_lista_actividades.mostrar_actividades(
            self.logica.actividades)

    def editar_actividad(self, indice_actividad, nombre):
        """
        Esta función editar una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.editar_actividad(self.logica.actividades[indice_actividad].nombre, nombre)
        self.vista_lista_actividades.mostrar_actividades(
            self.logica.actividades)

    def eliminar_actividad(self, indice_actividad):
        """
        Esta función elimina una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.actividades.pop(indice_actividad)
        self.vista_lista_actividades.mostrar_actividades(
            self.logica.actividades)

    def mostrar_viajeros(self):
        """
        Esta función muestra la ventana de la lista de viajeros
        """
        self.vista_lista_viajeros = Vista_lista_viajeros(self)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def mostrar_viajero(self, viajId):
        return self.logica.dar_viajero_id(viajId)

    def insertar_viajero(self, identificacion, nombre):
        """
        Esta función inserta un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.crear_viajero(nombre, identificacion)
        viajero = self.logica.dar_viajero(nombre)
        self.logica.viajeros.append(viajero)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def editar_viajero(self, indice_viajero, nombre, apellido):
        """
        Esta función edita un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros[indice_viajero] = {
            "Nombre": nombre, "Apellido": apellido}
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def eliminar_viajero(self, indice_viajero):
        """
        Esta función elimina un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros.pop(indice_viajero)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def mostrar_actividad(self, indice_actividad=-1):
        """
        Esta función muestra la ventana detallada de una actividad
        """
        if indice_actividad != -1:
            self.actividad_actual = indice_actividad
        actividad = self.logica.actividades[self.actividad_actual]
        self.vista_actividad = Vista_actividad(self, actividad.nombre)
        self.vista_actividad.mostrar_gastos_por_actividad(actividad)

    def insertar_gasto(self, concepto, valor, fecha, viajero_nombre, nombreActividad):
        self.logica.agregar_gasto_actividad(concepto, int(valor), fecha, viajero_nombre, nombreActividad)
        self.vista_actividad.mostrar_gastos_por_actividad(self.logica.actividades[self.actividad_actual])

    def editar_gasto(self, idGasto, concepto, valor, fecha, viajero_nombre, nombreActividad):
        self.logica.editar_gasto_actividad(idGasto, concepto, int(float(valor)), fecha, viajero_nombre, nombreActividad)
        self.vista_actividad.mostrar_gastos_por_actividad(self.logica.actividades[self.actividad_actual])

    def eliminar_gasto(self, indice):
        """
        Esta función elimina un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.pop(indice)
        self.vista_actividad.mostrar_gastos_por_actividad(
            self.logica.actividades[self.actividad_actual], self.logica.gastos)

    def mostrar_reporte_compensacion(self):
        """
        Esta función muestra la ventana del reporte de compensación
        """
        self.vista_reporte_comensacion = Vista_reporte_compensacion(self)
        self.vista_reporte_comensacion.mostrar_reporte_compensacion(
            self.logica.dar_reporte_comp_act(self.logica.actividades[self.actividad_actual].nombre))

    def mostrar_reporte_gastos_viajero(self, nombreActividad, concepto):
        """
        Esta función muestra el reporte de gastos consolidados
        """
        gastosViajero = self.logica.dar_reporte_gastos_viaj_act(nombreActividad, concepto)
        self.vista_reporte_gastos = Vista_reporte_gastos_viajero(self)
        self.vista_reporte_gastos.mostar_reporte_gastos(gastosViajero)

    def actualizar_viajeros(self, n_viajeros_en_actividad, nombreActividad):
        for viaj in n_viajeros_en_actividad:
            self.logica.agregar_viajero_actividad(viaj.identificacion, nombreActividad)

    def dar_viajeros(self):
        """
        Esta función pasa la lista de viajeros (debe implementarse como una lista de diccionarios o str)
        """
        return self.logica.viajeros

    def dar_viajeros_en_actividad(self):
        """
        Esta función pasa los viajeros de una actividad (debe implementarse como una lista de diccionarios o str)
        """
        return self.logica.viajeros_en_actividad

    def terminar_actividad(self, indice):
        """
        Esta función permite terminar una actividad (debe implementarse)
        """
        pass
