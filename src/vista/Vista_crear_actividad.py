from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial

class Dialogo_crear_actividad(QDialog):
    #Diálogo para crear una actividad

    def __init__(self,actividad):
        """
        Constructor del diálogo
        """    
        super().__init__()

        self.setFixedSize(300,110)
        
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #El título del diálogo varía si se usa para crear o editar una actividad

        titulo=""
        if actividad is None:
            titulo="Nueva Actividad"
        else:
            titulo="Editar Actividad"
        self.setWindowTitle(titulo)
        
        #Creación de las etiquetas

        etiqueta_nombre=QLabel("Nombre")
        self.add_dialog_label(distribuidor_dialogo, etiqueta_nombre, numero_fila, 0, 1, 3)                
        numero_fila=numero_fila+1

        self.texto_nombre=QLineEdit(self)
        self.add_dialog_label(distribuidor_dialogo, self.texto_nombre, numero_fila, 0, 1, 3)
        numero_fila=numero_fila+1

        #Creación de los botones
        
        self.btn_guardar = self.get_button("Guardar")
        self.add_dialog_button(distribuidor_dialogo, self.btn_guardar, numero_fila, 1)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = self.get_button("Cancelar")
        self.add_dialog_button(distribuidor_dialogo, self.btn_cancelar ,numero_fila, 2)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Si el diálogo se usa para editar, se debe mostrar el nombre de la actividad a editar
        
        if (actividad!=None):
            self.texto_nombre.setText(actividad)

    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """   
        self.resultado=1
        self.close()
        return self.resultado

    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """ 
        self.resultado=0
        self.close()
        return self.resultado

    def get_button(self, label):
        return QPushButton(label)

    def add_dialog_button(self, layout: QGridLayout, button: QWidget, row: int, column: int):
        layout.addWidget(button, row, column)

    def add_dialog_label(self, layout: QGridLayout, label: QWidget, row: int, column: int, row_span: int, column_span: int):
        layout.addWidget(label, row, column, row_span, column_span)
