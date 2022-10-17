import sys
from PyQt5.QtWidgets import QApplication
from src.vista.Interfaz_CuentasClaras import App_CuentasClaras
# from src.logica.Logica_mock import Logica_mock
from src.logica.cuentas_claras import CuentasClaras

if __name__ == '__main__':
    #Punto inicial de la aplicación

    # logica = Logica_mock()
    logica = CuentasClaras()

    app = App_CuentasClaras(sys.argv, logica)
    sys.exit(app.exec_())