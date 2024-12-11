from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

from source.database import db_manager

class UserControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Usuarios")
        self.setGeometry(200, 200, 800, 600)

        # Lista interna de usuarios
        self.users = []  # Cada usuario será un diccionario con 'username', 'role' y 'status'

        # Layout principal
        main_layout = QVBoxLayout()

        # Tabla para mostrar usuarios
        self.user_table = QTableWidget(0, 3)
        self.user_table.setHorizontalHeaderLabels(["Usuario", "Rol", "Estado"])
        self.user_table.horizontalHeader().setStretchLastSection(True)

        # Botones de acciones
        button_layout = QHBoxLayout()

        add_user_button = QPushButton("Agregar Usuario")
        add_user_button.clicked.connect(self.add_user)
        button_layout.addWidget(add_user_button)

        edit_user_button = QPushButton("Editar Usuario")
        edit_user_button.clicked.connect(self.edit_user)
        button_layout.addWidget(edit_user_button)

        delete_user_button = QPushButton("Eliminar Usuario")
        delete_user_button.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_user_button)

        # Formulario para agregar/editar usuarios
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Usuario:"), 0, 0)
        self.username_input = QLineEdit()
        form_layout.addWidget(self.username_input, 0, 1)

        form_layout.addWidget(QLabel("Rol:"), 1, 0)
        self.role_input = QComboBox()
        self.role_input.addItems(["Administrador", "Empleado"])
        form_layout.addWidget(self.role_input, 1, 1)

        form_layout.addWidget(QLabel("Estado:"), 2, 0)
        self.status_input = QComboBox()
        self.status_input.addItems(["Activo", "Inactivo"])
        form_layout.addWidget(self.status_input, 2, 1)

        save_button = QPushButton("Guardar Cambios")
        save_button.clicked.connect(self.save_changes)
        form_layout.addWidget(save_button, 3, 0, 1, 2)

        # Label para mensajes de estado
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.message_label, 4, 0, 1, 2)

        # Agregar elementos al layout principal
        main_layout.addWidget(self.user_table)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(form_layout)

        # Configurar contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
#Agregamos un usuario nuevo desde los campos del formulario
    def add_user(self):
        """Agrega un usuario nuevo desde los campos del formulario."""
        username = self.username_input.text()
        role = self.role_input.currentText()
        status = self.status_input.currentText()

        # Validar campos
        if not username:
            QMessageBox.warning(self, "Error", "El nombre de usuario no puede estar vacío.")
            return

        # Agregar usuario a la lista interna
        self.users.append({"username": username, "role": role, "status": status})

        # Actualizar la tabla
        self.refresh_table()

        # Limpiar campos del formulario
        self.username_input.clear()
        self.role_input.setCurrentIndex(0)
        self.status_input.setCurrentIndex(0)

        # Mostrar mensaje de éxito
        QMessageBox.information(self, "Éxito", f"Usuario '{username}' agregado correctamente.")
    #Actualizamos la tabla para mostrar los usuarios actuales
    def refresh_table(self):
        self.user_table.setRowCount(0)  # Limpia la tabla

        for user in self.users:
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)

            self.user_table.setItem(row_position, 0, QTableWidgetItem(user["username"]))
            self.user_table.setItem(row_position, 1, QTableWidgetItem(user["role"]))
            self.user_table.setItem(row_position, 2, QTableWidgetItem(user["status"]))
    #Editamos el usuario seleccionado en la tabla
    def edit_user(self):
        selected_row = self.user_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un usuario para editar.")
            return

        # Obtener datos del usuario seleccionado
        username = self.user_table.item(selected_row, 0).text()
        role = self.user_table.item(selected_row, 1).text()
        status = self.user_table.item(selected_row, 2).text()

        # Rellenar los campos del formulario con los datos seleccionados
        self.username_input.setText(username)
        self.role_input.setCurrentText(role)
        self.status_input.setCurrentText(status)

        # Eliminar el usuario de la lista interna
        del self.users[selected_row]

        # Actualizar la tabla
        self.refresh_table()
    #Eliminamos el usuario seleccionado de la tabla
    def delete_user(self):
        """Elimina el usuario seleccionado en la tabla."""
        selected_row = self.user_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un usuario para eliminar.")
            return

        # Confirmar eliminación
        username = self.user_table.item(selected_row, 0).text()
        confirmation = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Estás seguro de eliminar el usuario '{username}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            # Eliminar el usuario de la lista interna
            del self.users[selected_row]

            # Actualizar la tabla
            self.refresh_table()
            QMessageBox.information(self, "Éxito", f"Usuario '{username}' eliminado correctamente.")

    def save_changes(self):
        username = self.username_input.text()
        role = self.role_input.currentText()
        status = self.status_input.currentText()

        # Validar campos
        is_valid = True

        if not username:
            self.username_input.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.username_input.setStyleSheet("")

        if is_valid:
            # Aquí puedes agregar la lógica para guardar los cambios en la base de datos o archivo
            print(f"Guardado: {username}, {role}, {status}")

            # Limpiar campos
            self.username_input.clear()
            self.role_input.setCurrentIndex(0)
            self.status_input.setCurrentIndex(0)

            # Mostrar mensaje de éxito
            self.message_label.setText("Usuario guardado exitosamente.")
            self.message_label.setStyleSheet("color: green;")
        else:
            self.message_label.setText("Por favor, corrige los campos marcados en rojo.")
            self.message_label.setStyleSheet("color: red;")
