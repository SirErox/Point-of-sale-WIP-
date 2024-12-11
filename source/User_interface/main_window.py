from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
    QPushButton, QWidget, QLabel, QGridLayout,QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from source.User_interface.UsersControlWindow import UserControlWindow

def keyPressEvent(self, event: QKeyEvent):
    """Capturar eventos de teclado para atajos rápidos"""
    if event.key() == Qt.Key_F3:
        self.search_product()
    elif event.key() == Qt.Key_F4:
        self.change_quantity()
    elif event.key() == Qt.Key_F8:
        self.new_sale()
    elif event.key() == Qt.Key_F12:
        self.pay_cash()
    elif event.key() == Qt.Key_Escape:  # Ejemplo: Cancelar orden con ESC
        self.cancel_order()

class MainWindow(QMainWindow):
    def __init__(self,user_role):
        super().__init__()
        self.setWindowTitle("LALA'S TECH AND MORE")
        self.setGeometry(100, 100, 1024, 768)

        # Configurar layout principal
        main_layout = QHBoxLayout()

        # Tabla de productos
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Nombre del producto", "Cantidad", "Precio", "Total"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        #self.table.resizeColumnsToContents()

         # Conectar señal para ajuste dinámico de columnas
        self.table.cellChanged.connect(self.table.resizeColumnsToContents)
        # Layout del panel derecho
        right_panel = QVBoxLayout()

        # Botones de acciones rápidas
        buttons = [
            ("Buscar (F3)", self.search_product),
            ("Cantidad (F4)", self.change_quantity),
            ("Nueva venta (F8)", self.new_sale),
            ("Efectivo (F12)", self.pay_cash),
            ("Anular orden", self.cancel_order)
        ]

        for text, action in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(action)
            right_panel.addWidget(btn)

         # Botón de Control de Usuarios (solo para administradores)
        if user_role=="admin":
            user_control_button=QPushButton("Control de usuarios")
            user_control_button.clicked.connect(self.open_user_control)
            right_panel.addWidget(user_control_button)
            
        # Espaciador
        right_panel.addStretch()

        # Layout inferior
        bottom_layout = QGridLayout()
        bottom_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        self.subtotal_label = QLabel("0.0")
        bottom_layout.addWidget(self.subtotal_label, 0, 1)

        bottom_layout.addWidget(QLabel("Impuestos:"), 1, 0)
        self.tax_label = QLabel("0.0")
        bottom_layout.addWidget(self.tax_label, 1, 1)

        bottom_layout.addWidget(QLabel("TOTAL:"), 2, 0)
        self.total_label = QLabel("0.0")
        bottom_layout.addWidget(self.total_label, 2, 1)

        right_panel.addLayout(bottom_layout)

        # Agregar elementos al layout principal
        main_layout.addWidget(self.table)
        main_layout.addLayout(right_panel)

        # Configurar contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def search_product(self):
        print("Buscar producto")

    def change_quantity(self):
        print("Cambiar cantidad")

    def new_sale(self):
        print("Nueva venta")

    def pay_cash(self):
        print("Pago en efectivo")

    def cancel_order(self):
        print("Orden anulada")

    def open_user_control(self):
         # Almacenar la ventana como un atributo de la clase principal
        self.user_control_window = UserControlWindow()
        self.user_control_window.show()  # Abre la ventana de control de usuarios
