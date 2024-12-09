import os,sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QHBoxLayout

# Clase para la ventana de inicio de sesión
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LALA'S TECH AND MORE LOGIN")
        self.setGeometry(500, 300, 300, 150)

        # Layout y widgets
        layout = QVBoxLayout()

        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()
        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.check_credentials)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Resultado de la autenticación
        self.authenticated = False

    def check_credentials(self):
        username = self.input_user.text()
        password = self.input_pass.text()

        # Credenciales predefinidas (puedes reemplazarlas por una consulta a una base de datos)
        if username == "admin" and password == "1234":
            self.authenticated = True
            self.accept()  # Cierra el diálogo
        else:
            self.label_user.setText("Credenciales inválidas. Intente de nuevo.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LALA'S Inicio de sesion")
        self.setGeometry(100, 100, 800, 600)  # Tamaño de la ventana al iniciar

        # Hacer que la ventana sea redimensionable
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1080, 1920)
        
        # Crear layout y widgets
        layout = QVBoxLayout()

        button1 = QPushButton("Vender")
        button2 = QPushButton("Productos")
        button3 = QPushButton("Reportes")

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        # Contenedor central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
     # Cargar archivo de estilo desde el directorio User_interface
    style_path = os.path.join("User_interface", "styles.qss")
    with open(style_path, "r") as file:
        app.setStyleSheet(file.read())
        
     # Mostrar ventana de inicio de sesión
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted and login.authenticated:
        # Si las credenciales son correctas, mostrar la ventana principal
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()
