from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QComboBox, QMessageBox,
    QCheckBox,QMenu
)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import sqlite3, bcrypt
from source.database.db_manager import (db_creation, añadir_usuario, update_usuario, borrar_usuario, fetch_usuario)
from source.User_interface.add_usuario import AddUserDialog

class UserControlWindow(QtWidgets.QMainWindow):
    user_table_updated=QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Usuarios")
        self.setGeometry(200, 200, 800, 600)
        #empezamos con la importacion de la base de datos
        db_creation()
        # Layout principal
        main_layout = QVBoxLayout()

        #barra de busqueda  
        self.search_bar=QLineEdit()
        self.search_bar.setPlaceholderText("Buscar usuario")
        self.search_bar.textChanged.connect(self.filter_users)
        main_layout.addWidget(self.search_bar)
        self.add_user_button=QtWidgets.QPushButton("Agregar usuario")
        self.add_user_button.clicked.connect(self.add_user)
        main_layout.addWidget(self.add_user_button)
        # Tabla para mostrar usuarios   
        self.table_widget=QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Usuario", "Contraseña", "Rol","Opciones"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_actions_menu)
        
        # Crear los elementos de la interfaz
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.show_password_checkbox = QCheckBox("Mostrar contraseña")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
 
        # Agregar elementos al layout principal
        main_layout.addWidget(self.table_widget)
        #main_layout.addLayout(button_layout)

        # Configurar contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.add_user_dialog=AddUserDialog(self)
        self.add_user_dialog.user_table_updated.connect(self.cargar_usuarios)

        self.cargar_usuarios()

    def update_user_table(self):
        """Fetches user data and updates the table."""
        rows = self.fetch_all_users()
        self.table_widget.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
        # Update user information in each table row
            self.table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(row[1]))  # Usuario
            self.table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row[2]))  # Rol
            self.table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(row[3]))  #password
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
        if dialog.exec_():
            try:
                añadir_usuario(dialog.username_edit.text(), dialog.password_edit.text(), dialog.role_combo.currentText())
                self.update_user_table()  # Actualizar la tabla inmediatamente
                QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar el usuario: {str(e)}")
        self.update_user_table()

    def cargar_usuarios(self):
        connect=sqlite3.connect("source/database/POS_database.db")
        cursor=connect.cursor()
        cursor.execute('SELECT * FROM USERS')
        rows=cursor.fetchall()
        connect.close()
        self.table_widget.clearContents()
        #cargamos los usuarios a la tabla
        self.table_widget.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            self.table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(row[1]))  # Usuario
            self.table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row[2]))  # Rol
            self.table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(row[3]))  # Password (should be masked)

            # Agregar un botón de acciones en la última columna
            action_button = QtWidgets.QPushButton('Acciones')
            action_button.clicked.connect(lambda checked, row=row_index: self.show_actions_menu(action_button.geometry().bottomLeft()))
            self.table_widget.setCellWidget(row_index, 3, action_button)

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
