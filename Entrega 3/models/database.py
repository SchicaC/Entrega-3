import mysql.connector
from tkinter import messagebox
import os

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'atle'
}

class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_procedure(self, procedure_name, params=None):
        if not self.connection:
            if not self.connect():
                return None

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.callproc(procedure_name, params)
            else:
                cursor.callproc(procedure_name)

            # Para procedimientos que retornan resultados
            for result in cursor.stored_results():
                return result.fetchall()

            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Error de base de datos", f"Error al ejecutar procedimiento: {e}")
            return None
        finally:
            cursor.close()

    def save_image_to_db(self, image_path, table_name, id_field, id_value, image_field):
        """Guarda una imagen en la base de datos"""
        try:
            if not image_path or not os.path.exists(image_path):
                return False

            with open(image_path, 'rb') as file:
                image_data = file.read()

            cursor = self.connection.cursor()
            query = f"UPDATE {table_name} SET {image_field} = %s WHERE {id_field} = %s"
            cursor.execute(query, (image_data, id_value))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar imagen: {e}")
            return False

    def get_image_from_db(self, table_name, id_field, id_value, image_field):
        """Recupera una imagen de la base de datos"""
        try:
            # Verificar si la tabla tiene la columna de imagen
            cursor = self.connection.cursor()
            cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{image_field}'")
            column_exists = cursor.fetchone()

            if not column_exists:
                return None  # La columna no existe

            # CORREGIR: Usar los nombres correctos de las columnas ID
            if table_name == "competiciones":
                query = f"SELECT {image_field} FROM {table_name} WHERE ID_Competiciones = %s"
            elif table_name == "entrenadores":
                query = f"SELECT {image_field} FROM {table_name} WHERE ID_Entrenadores = %s"
            elif table_name == "miembros":
                query = f"SELECT {image_field} FROM {table_name} WHERE ID_Miembros = %s"
            elif table_name == "entrenamientos":
                query = f"SELECT {image_field} FROM {table_name} WHERE ID_Entrenamientos = %s"
            else:
                query = f"SELECT {image_field} FROM {table_name} WHERE ID = %s"

            cursor.execute(query, (id_value,))
            result = cursor.fetchone()
            cursor.close()

            if result and result[0]:
                return result[0]
            return None
        except Exception as e:
            print(f"Error al recuperar imagen: {e}")
            return None