import sqlite3
import re


# ##############################################
# MODELO
# ##############################################
class Model:

    def __init__(self):
        self.con = self.conexion()
        self.cursor = self.con.cursor()
        self.crear_tabla()

    def conexion(self):
        try:
            con = sqlite3.connect("mibase.db")
            return con
        except sqlite3.Error as e:
            print(f"Error en conexion: {e}")

    def crear_tabla(self):
        try:
            sql = """CREATE TABLE IF NOT EXISTS productos
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto varchar(20) NOT NULL,
                    cantidad integer,
                    precio real)
            """
            self.cursor.execute(sql)
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def alta(self, producto, cantidad, precio):
        patron = "^[A-Za-záéíóú\s]*$"
        cadena = producto.get()
        try:
            if re.match(patron, cadena):
                data = (cadena.strip(), int(cantidad.get()), float(precio.get()))
                sql = (
                    "INSERT INTO productos(producto, cantidad, precio) VALUES(?, ?, ?)"
                )
                self.cursor.execute(sql, data)
                self.con.commit()
                producto.set("")
                cantidad.set("")
                precio.set("")
                return "Producto agregado exitosamente"
            else:
                return "Error en nombre de producto"
        except sqlite3.Error as e:
            print(f"Error al insertar producto: {e}")

    def productos(
        self,
    ):
        try:
            sql = "SELECT * FROM productos ORDER BY id DESC"
            con = self.conexion()
            cursor = con.cursor()
            datos = cursor.execute(sql)
            return datos.fetchall()
        except sqlite3.Error as e:
            print(f"Error en listar productos: {e}")
            return []

    def consultar(self, producto):
        try:
            consulta = producto.get().strip()
            data = (consulta,)
            sql = "SELECT * FROM productos WHERE producto = ?;"
            datos = self.cursor.execute(sql, data).fetchall()
            return datos
        except sqlite3.Error as e:
            print(f"Error en consulta: {e}")
            return []

    def borrar(self, seleccion):
        try:
            data = (seleccion,)
            sql = "DELETE FROM productos WHERE id = ?;"
            self.cursor.execute(sql, data)
            self.con.commit()
            return "Producto eliminado exitosamente"
        except sqlite3.Error as e:
            print(f"Error en borrado: {e}")
            return "No se pudo borrar"
