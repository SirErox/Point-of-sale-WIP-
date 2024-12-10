import sqlite3
import bcrypt

db_name="POS_database.db"

#funcion para la creacion de la base de datos, si existe se conecta
def db_creation():
    #conexion para base de datos
    connection=sqlite3.connect(db_name)
    
    #cursor para poder poner comandos en la base de datos
    cursor=connection.cursor()
    
    # Crear la tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

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