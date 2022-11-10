from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial


class Dialogo_crear_viajero(QDialog):
    #Diálogo para crear o editar un viajero

    def create_btns(btn, text, distribuidor, fila, id, action ):
        btn = QPushButton(text)
        distribuidor.addWidget(btn, fila, id)
        btn.clicked.connect(action)

    def create_line_edit(text,entity, distribuidor, fila,):
        text=QLineEdit(entity)
        distribuidor.addWidget(text,fila,0,1,3)
    
    def create_label(etiqueta, text, distribuidor, fila):
        etiqueta=QLabel(text)
        distribuidor.addWidget(etiqueta,fila,0,1,3)      

    def __init__(self,viajero):
        """
        Constructor del diálogo
        """   
        super().__init__()

        
        self.setFixedSize(400, 200)
        self.setWindowIcon(QIcon("src/devcuentasclaras/recursos/smallLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()
        
        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #Si se va a crear un nuevo viajero o se va a editar, usamos el mismo diálogo
        titulo=""
        if(viajero==None):
            titulo="Nuevo Viajero"
        else:
            titulo="Editar Viajero"

        self.setWindowTitle("CuentasClaras - {}".format(titulo))
       
        #Creación de las etiquetas y los campos de texto
        self.create_label(etiqueta_id, "Identificación", distribuidor_dialogo, numero_fila)           
        numero_fila=numero_fila+1

        self.create_line_edit(self.texto_id, self,distribuidor_dialogo,numero_fila)
        numero_fila=numero_fila+1

        self.create_label(etiqueta_nombre, "Nombre", distribuidor_dialogo, numero_fila)             
        numero_fila=numero_fila+1
        
        self.create_line_edit(self.texto_nombre, self,distribuidor_dialogo,numero_fila)
        numero_fila=numero_fila+1

        #Creación de los botones para guardar o cancelar

        self.create_btns(self.btn_guardar, "Guardar", distribuidor_dialogo, numero_fila, 1, self.guardar)

        self.create_btns(self.btn_cancelar, "Cancelar", distribuidor_dialogo, numero_fila, 2, self.cancelar)

        #Si el diálogo se va a usar para editar, se pone la información correspondiente en los campos de texto

        if (viajero!=None):
            self.texto_id.setText(viajero.identificacion)
            self.texto_nombre.setText(viajero.nombre)


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


