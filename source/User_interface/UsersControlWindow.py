from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QComboBox, QMessageBox,
    QCheckBox,QMenu
)
from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtCore import Qt
import sqlite3, bcrypt
from source.database.db_manager import (db_creation, añadir_usuario, update_usuario, borrar_usuario, fetch_usuario)
from source.User_interface.add_usuario import AddUserDialog

class UserControlWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Usuarios")
        self.setGeometry(100, 100, 600, 400)

        # Configurar la tabla de usuarios
        self.user_table = QtWidgets.QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["Usuario", "Contraseña", "Rol", "Opciones"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        # Botones de control
        self.add_user_button = QtWidgets.QPushButton("Agregar Usuario")
        self.edit_user_button = QtWidgets.QPushButton("Editar Usuario")
        self.delete_user_button = QtWidgets.QPushButton("Eliminar Usuario")
        self.save_changes_button = QtWidgets.QPushButton("Guardar Cambios")

        # Configurar el layout principal
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_user_button)
        button_layout.addWidget(self.edit_user_button)
        button_layout.addWidget(self.delete_user_button)
        button_layout.addWidget(self.save_changes_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.user_table)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Conectar las acciones de los botones
        self.add_user_button.clicked.connect(self.open_add_user_dialog)
        self.cargar_usuarios()

    def update_user_table(self):
        """Fetches user data and updates the table."""
        rows = self.fetch_all_users()
        self.table_widget.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
        # Update user information in each table row
            role_bytes = row[2]  # Assuming role data is in row[2]
            self.table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(row[0]))  # Usuario
            self.table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(role_bytes))  # Rol
            self.table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(row[1]))  #password
            # ... (update other columns)
        # Add the action button
        action_button = QtWidgets.QPushButton('Acciones')
        action_button.clicked.connect(lambda checked, row=row_index: self.show_actions_menu(action_button.geometry().bottomLeft()))
        self.table_widget.setCellWidget(row_index, 3, action_button)

    def filter_users(self, search_term):
        """
        Filtra los usuarios de la tabla según el término de búsqueda ingresado.

        Args:
            search_term (str): El término a buscar en los nombres de usuario.
    """
        # Obtener todos los usuarios de la base de datos
        all_users = self.fetch_all_users()  # Suponiendo que tienes una función para obtener todos los usuarios

        # Filtrar los usuarios según el término de búsqueda (caso insensible)
        filtered_users = [user for user in all_users if search_term.lower() in user[0].lower()]

        # Limpiar la tabla y cargar los usuarios filtrados
        self.table_widget.setRowCount(0)
        for row_index, user in enumerate(filtered_users):
            self.table_widget.insertRow(row_index)
            self.table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(user[0]))  # Usuario
            self.table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(user[1]))  # Contraseña
            # ... (resto de las columnas)

            # Agregar el botón de acciones a cada fila
            action_button = QtWidgets.QPushButton('Acciones')
            action_button.clicked.connect(lambda checked, row=row_index: self.show_actions_menu(row))
            self.table_widget.setCellWidget(row_index, 4, action_button)
            self.update_user_table()

    def fetch_all_users(self):
        """
        Obtiene todos los usuarios de la base de datos.

        Returns:
            list: Una lista de tuplas, donde cada tupla representa un usuario.
        """
        rows=fetch_usuario()
        return rows

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)
#Agregamos un usuario nuevo desde los campos del formulario
    def add_user(self):
        dialog = AddUserDialog(self)
        dialog.user_table_updated.connect(self.update_user_table)
        dialog.exec_()
        username=dialog.username_edit.text()
        password=dialog.password_edit.text()
        role=dialog.role_combo.currentText()
         # Hashea la contraseña antes de guardarla
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            # Inserta los datos en la base de datos
            añadir_usuario(username,password,role)
            # Limpia los campos del formulario
            self.username_input.clear()
            self.password_input.clear()

            # Actualiza la tabla inmediatamente
            self.cargar_usuarios()

            # Muestra un mensaje de éxito
            QtWidgets.QMessageBox.information(self, "Éxito", f"Usuario '{username}' añadido correctamente.")

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al añadir el usuario: {e}")
            print(f"Error: {e}")  # Esto te dará más pistas del problema
        self.update_user_table()

    def cargar_usuarios(self):
        users = fetch_usuario()
        self.user_table.setRowCount(len(users))

        for row, user in enumerate(users):
            username_item = QtWidgets.QTableWidgetItem(user[0])
        
            # Decodificar contraseña
            password_item = QtWidgets.QTableWidgetItem(user[1])
        
            role_item = QtWidgets.QTableWidgetItem(user[2])

            # Crear un botón de acciones
            action_button = QtWidgets.QPushButton("Acciones")
            #action_button.setStyleSheet("background-color: pink;")

            self.user_table.setItem(row, 0, username_item)
            self.user_table.setItem(row, 1, password_item)
            self.user_table.setItem(row, 2, role_item)
            self.user_table.setCellWidget(row, 3, action_button)

    def open_add_user_dialog(self):
        """Abre la ventana para agregar un nuevo usuario."""
        dialog = AddUserDialog(self)
        dialog.user_table_updated.connect(self.load_users)
        dialog.exec_()
    
    def show_actions_menu(self, pos):
        # Mostrar un menú contextual con opciones para editar y eliminar
        menu = QMenu(self)
        menu.exec_(self.mapToGlobal(pos))
        edit_user_action = menu.addAction("Editar Usuario")
        delete_user_action = menu.addAction("Eliminar Usuario")

        selected_row = self.table_widget.currentRow()
        if selected_row != -1:  # Only enable actions if a row is selected
            edit_user_action.setEnabled(True)
            delete_user_action.setEnabled(True)
            edit_user_action.triggered.connect(lambda: self.edit_user(selected_row))
            delete_user_action.triggered.connect(lambda: self.delete_user(selected_row))
        menu.exec_(self.mapToGlobal(pos))
    #Editamos el usuario seleccionado en la tabla
    def edit_user(self,selected_row):
        selected_row = self.table_widget.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un usuario para editar.")
            return

        username, role, status, password = self.get_user_input(
            current_values={
                "username": self.table_widget.item(selected_row, 0).text() or"",
                "role": self.table_widget.item(selected_row, 1).text() or "",
                "password": self.table_widget.item(selected_row, 2).text()
            }
        )
        # Actualizar el usuario en la base de datos
        update_usuario(username, role, status, password)
        # Actualizar la tabla
        self.update_user_table()
   
    #Eliminamos el usuario seleccionado de la tabla
    def delete_user(self,selected_row):
        selected_row = self.table_widget.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un usuario para eliminar.")
            return

        username = self.table_widget.item(selected_row, 0).text()
        confirmation = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Estás seguro de eliminar el usuario '{username}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            borrar_usuario(username)
            self.cargar_usuarios()
            QMessageBox.information(self, "Éxito", f"Usuario '{username}' eliminado correctamente.")
        self.update_user_table()

    def save_changes(self):
       """Guarda los cambios realizados en los campos del formulario."""
       username = self.username_edit.text()
       password = self.password_edit.text()

       # Cifrar la contraseña
       hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

       # Insertar en la base de datos
       conn = sqlite3.connect('users.db')
       cursor = conn.cursor()
       cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
       conn.commit()
       conn.close()
       QMessageBox.information(self, "Guardar Cambios", "Los cambios se han guardado correctamente.")

    def get_user_input(self, current_values=None):
        """Abre un cuadro de diálogo para recoger los datos del usuario."""
        current_values = current_values or {}

        username = current_values.get("username", "")
        role = current_values.get("role", "Administrador")
        status = current_values.get("status", "Activo")
        password = current_values.get("password", "")

        return username, role, status, password
