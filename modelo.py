import sqlite3
import re


# ##############################################
# MODELO
# ##############################################
class Model:

    def __init__(self):
        """
        Inicializa una nueva instancia de la clase `Model`.

        Establece una conexión con la base de datos, crea un cursor y llama a la función `crear_tabla` para asegurar que la tabla exista.

        :return: None
        :rtype: None
        """
        self.con = self.conexion()
        self.cursor = self.con.cursor()
        self.crear_tabla()

    def conexion(self):
        """
        Establece una conexión con la base de datos SQLite.

        Intenta conectar a una base de datos llamada "mibase.db". En caso de error, imprime el mensaje de error.

        :return: La conexión a la base de datos SQLite.
        :rtype: sqlite3.Connection
        """
        try:
            con = sqlite3.connect("mibase.db")
            return con
        except sqlite3.Error as e:
            print(f"Error en conexion: {e}")

    def crear_tabla(self):
        """
        Crea la tabla `productos` en la base de datos si no existe.

        La tabla `productos` tiene las siguientes columnas:
        - `id`: Identificador único del producto (clave primaria, autoincremental).
        - `producto`: Nombre del producto.
        - `cantidad`: Cantidad del producto.
        - `precio`: Precio del producto.

        :return: None
        :rtype: None
        """
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
        """
        Agrega un nuevo producto a la tabla `productos`.

        Valida que el nombre del producto contenga solo letras y espacios. Inserta el producto en la base de datos si la validación es correcta.

        :param producto: El nombre del producto.
        :type producto: tkinter.StringVar
        :param cantidad: La cantidad del producto.
        :type cantidad: tkinter.StringVar
        :param precio: El precio del producto.
        :type precio: tkinter.StringVar
        :return: Mensaje indicando si el producto fue agregado exitosamente o si hubo un error.
        :rtype: str
        """
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
        """
        Obtiene una lista de todos los productos en la tabla `productos`.

        Ordena los productos por `id` en orden descendente.

        :return: Lista de tuplas con los datos de los productos.
        :rtype: list of tuples
        """
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
        """
        Consulta la tabla `productos` para obtener los productos que coincidan con el nombre dado.

        :param producto: El nombre del producto a consultar.
        :type producto: tkinter.StringVar
        :return: Lista de tuplas con los datos de los productos que coinciden.
        :rtype: list of tuples
        """
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
        """
        Elimina un producto de la tabla `productos` basado en el identificador proporcionado.

        :param seleccion: El identificador del producto a eliminar.
        :type seleccion: int
        :return: Mensaje indicando si el producto fue eliminado exitosamente o si hubo un error.
        :rtype: str
        """
        try:
            data = (seleccion,)
            sql = "DELETE FROM productos WHERE id = ?;"
            self.cursor.execute(sql, data)
            self.con.commit()
            return "Producto eliminado exitosamente"
        except sqlite3.Error as e:
            print(f"Error en borrado: {e}")
            return "No se pudo borrar"
