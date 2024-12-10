import sqlite3
import bcrypt

db_name="source/database/POS_database.db"

#funcion para la creacion de la base de datos, si existe se conecta
def db_creation():
   try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Crear tabla de usuarios si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        # Insertar un usuario inicial si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ("admin", "1234", "admin"))
            connection.commit()

        connection.close()
        print("Base de datos inicializada correctamente.")
   except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

def añadir_usuario(username,password,role):
    #funcion para añadir un usuario nuevo con contraseña encriptada
    connection=sqlite3.connect(db_name)
    cursor=connection.cursor()

    #encriptamos la contraseña
    hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    try:
        cursor.execute('INSERT INTO USERS (username,password,role) values(?,?,?)',
                        (username,hashed_password.decode('utf-8'),role))
        connection.commit()
    except sqlite3.IntegrityError:
        print("usuario ya existente en la base de datos")
    finally:
        connection.close()
        
#obtenemos los usuarios registrados de la tabla de usuarios
def fetch_usuario():
    try:
        #abrimos la conexion   
        Connection=sqlite3.connect(db_name)
        #creamos cursor
        cursor=Connection.cursor()
        query="SELECT id, username, password, role FROM USERS"
        cursor.execute(query)
        USERS= cursor.fetchall()
        Connection.close()
        return USERS
    except Exception as e:
        print(f"Error al obtener usuarios:{e}")
        return []

#actualizamos los datos de un usuario
def update_usuario(user_id,username,password,role):
    try:
        connection=sqlite3.connect(db_name)
        cursor=connection.cursor()
        query="""
        UPDATE users 
        SET username = ?, password = ?, role = ? 
        WHERE id = ?
        """
        cursor.execute(query,(username,password,role,user_id))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error al actualizar valores del usuario:{e}")
        return False

#eliminamos usuario de la base de datos
def borrar_usuario(user_id):
    try:
        connection=sqlite3.connect(db_name)
        cursor=connection.cursor()
        query="DELETE FROM users WHERE id= ?"
        cursor.execute(query,(user_id))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error al borrar usuario: {e}")
        return False

#autenticamos al usuario por la contraseña
def autenticar_usuario(username,password):
    #conectamos a la base de datos
    connection = sqlite3.connect(db_name)
    #cursor para insertar comandos en la base de datos
    cursor = connection.cursor()
    #extraemos la contraseña
    cursor.execute('SELECT password, role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    connection.close()
    #hacemos la comprobacion con contraseñas encriptadas
    if result:
        hashed_password, role = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            #damos verificacion regresando el rol del usuario
            return role
    #si no no regresamos nada   
    return None

#flag point
#print("Base de datos conectada y tablas encontradas")