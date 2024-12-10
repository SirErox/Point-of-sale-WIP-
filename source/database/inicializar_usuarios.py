from db_manager import añadir_usuario

# Añadir usuarios iniciales
usuarios_iniciales = [
    ("admin", "1234","admin"),  # Usuario administrador
    ("vendedor1", "v123","vendedor"),  # Otro usuario con diferentes credenciales
    ("vendedor2", "v456","vendedor")
]

for username, password, role in usuarios_iniciales:
    try:
        añadir_usuario(username, password, role)
        print(f"Usuario '{username}' añadido correctamente.")
    except Exception as e:
        print(f"Error al añadir usuario '{username}': {e}")
