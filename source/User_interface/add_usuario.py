from PyQt5 import QtWidgets,QtCore
from source.database.db_manager import db_creation,añadir_usuario
class AddUserDialog(QtWidgets.QDialog):
    user_table_updated=QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Usuario")
        self.setGeometry(200,200,400,300)
        db_creation()
        # Crear los elementos de la interfaz
        self.role_combo=QtWidgets.QComboBox()
        self.role_combo.addItem("Administrador")
        self.role_combo.addItem("Vendedor")

        self.username_label = QtWidgets.QLabel("Nombre de usuario:")
        self.username_edit = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel("Contraseña:")
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.role_label=QtWidgets.QLabel("Rol")
        # Agregar más campos según sea necesario (e.g., rol, email)

        # Botón para guardar
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_combo)
        # ... agregar más widgets al layout
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def accept(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        role= self.role_combo.currentText()
        # Validación básica
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre de usuario y una contraseña.")
            return

        # Agregar el usuario a la base de datos (reemplaza con tu lógica)
        if añadir_usuario(username, password, role):
            QtWidgets.QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
            self.user_table_updated.emit()
            super().accept()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Error al agregar el usuario.")
        