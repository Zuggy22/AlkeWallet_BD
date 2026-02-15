import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Crea la conexión a la base de datos MySQL """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Tu host (ej. localhost)
            database='AlkeWallet',   # El nombre de tu BD
            user='root',             # Tu usuario de MySQL
            password='zuggy22'   # Tu contraseña de MySQL
        )
        if connection.is_connected():
            print(" Conexión exitosa a la base de datos MySQL")
    except Error as e:
        print(f" Error al conectar a MySQL: {e}")
    return connection

# --- CONSULTAS SOLICITADAS (Lectura) ---

def obtener_moneda_usuario(user_id):
    """ Consulta para obtener el nombre de la moneda elegida por un usuario específico """
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT DISTINCT m.currency_name 
        FROM Transaccion t
        JOIN Moneda m ON t.currency_id = m.currency_id
        WHERE t.sender_user_id = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        print(f"\n--- Monedas usadas por Usuario {user_id} ---")
        for row in result:
            print(f"Moneda: {row[0]}")
        conn.close()

def obtener_todas_transacciones():
    """ Consulta para obtener todas las transacciones registradas """
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT t.transaction_id, u1.nombre as Emisor, u2.nombre as Receptor, 
               t.importe, m.currency_name, t.transaction_date
        FROM Transaccion t
        JOIN Usuario u1 ON t.sender_user_id = u1.user_id
        JOIN Usuario u2 ON t.receiver_user_id = u2.user_id
        JOIN Moneda m ON t.currency_id = m.currency_id;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        print("\n--- Historial Completo de Transacciones ---")
        for row in result:
            print(f"ID: {row[0]} | De: {row[1]} | Para: {row[2]} | Monto: {row[3]} {row[4]} | Fecha: {row[5]}")
        conn.close()

def obtener_transacciones_usuario(user_id):
    """ Consulta para obtener todas las transacciones de un usuario específico """
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT * FROM Transaccion 
        WHERE sender_user_id = %s OR receiver_user_id = %s;
        """
        # Pasamos user_id dos veces porque hay dos %s en la query
        cursor.execute(query, (user_id, user_id))
        result = cursor.fetchall()
        print(f"\n--- Transacciones del Usuario {user_id} ---")
        for row in result:
            print(row)
        conn.close()

# --- SENTENCIAS DML (Escritura/Modificación) ---

def modificar_email_usuario(user_id, nuevo_email):
    """ Sentencia DML para modificar el correo de un usuario """
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE Usuario SET correo_electronico = %s WHERE user_id = %s"
            cursor.execute(query, (nuevo_email, user_id))
            conn.commit() # ¡Importante! Guarda los cambios en la BD
            print(f"\n Correo actualizado correctamente para el usuario {user_id}")
        except Error as e:
            print(f" Error al actualizar: {e}")
        finally:
            conn.close()

def eliminar_transaccion(transaction_id):
    """ Sentencia para eliminar una transacción completa """
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM Transaccion WHERE transaction_id = %s"
            cursor.execute(query, (transaction_id,))
            conn.commit() # ¡Importante! Guarda los cambios
            print(f"\n Transacción {transaction_id} eliminada correctamente")
        except Error as e:
            print(f" Error al eliminar: {e}")
        finally:
            conn.close()

# --- EJECUCIÓN DEL CÓDIGO ---

if __name__ == "__main__":
    # 1. Ver monedas del usuario 1
    obtener_moneda_usuario(1)

    # 2. Ver todas las transacciones
    obtener_todas_transacciones()

    # 3. Ver transacciones del usuario 1
    obtener_transacciones_usuario(1)

    # 4. Modificar el correo del usuario 1
    modificar_email_usuario(1, "nuevo_juan@alkewallet.com")

    # 5. Eliminar la transacción número 1 (¡Cuidado! Solo ejecutar si existe)
    # eliminar_transaccion(1)