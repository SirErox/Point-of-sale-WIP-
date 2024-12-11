import os,sys
from PyQt5.QtWidgets import (
    QApplication, 
    QDialog)
from PyQt5.QtCore import Qt
from source.database.db_manager import(
     db_creation)
from source.User_interface.main_window import MainWindow
from source.User_interface.login_window import LoginWindow
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #mandamos a crear la base de datos
    db_creation()
     # Cargar archivo de estilo desde el directorio User_interface
    style_path = os.path.join("source", "User_interface", "styles.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as file:
            app.setStyleSheet(file.read())
    else:
        print("Archivo de estilos no encontrado. Continuando sin estilo.")
        
     # Mostrar ventana de inicio de sesión
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted and login.authenticated:
        # Si las credenciales son correctas, mostrar la ventana principal
        window = MainWindow(login.user_role)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()
