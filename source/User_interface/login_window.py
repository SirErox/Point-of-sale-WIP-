from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog
from PyQt5.QtCore import Qt
from source.database.db_manager import autenticar_usuario

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGIN HUB")
        self.setFixedSize(200, 150)

        # Layout y widgets
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

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
        self.user_role = None
    def check_credentials(self):
        username = self.input_user.text()
        password = self.input_pass.text()
        role=autenticar_usuario(username,password)
        if role:
            self.authenticated = True
            self.user_role=role
            self.accept()  # Cierra el diálogo
        else:
            self.label_user.setText("Credenciales inválidas. Intente de nuevo.")