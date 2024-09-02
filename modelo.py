import sqlite3
import re


# ##############################################
# MODELO
# ##############################################
class Abmc:
    def __init__(
        self,
    ):
        pass

    def conexion(
        self,
    ):
        con = sqlite3.connect("mibase.db")
        return con

    def crear_tabla(
        self,
    ):
        con = self.conexion()
        cursor = con.cursor()
        sql = """CREATE TABLE productos
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto varchar(20) NOT NULL,
                cantidad integer,
                precio real)
        """
        cursor.execute(sql)
        con.commit()

    def alta(self, producto, cantidad, precio, tree):
        patron = "^[A-Za-záéíóú\s]*$"  # regex para el campo cadena
        cadena = producto.get()
        if re.match(patron, cadena):
            con = self.conexion()
            cursor = con.cursor()
            data = (cadena.strip(), int(cantidad.get()), float(precio.get()))
            sql = "INSERT INTO productos(producto, cantidad, precio) VALUES(?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            producto.set("")
            cantidad.set("")
            precio.set("")
            self.actualizar_treeview(tree)
        else:
            return "Error en nombre de producto"

    def actualizar_treeview(self, tree):
        self.limpiar_treeview(tree)
        sql = "SELECT * FROM productos ORDER BY id DESC"
        con = self.conexion()
        cursor = con.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        for fila in resultado:
            tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))

    def limpiar_treeview(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def consultar(self, producto, tree):
        consulta = producto.get().strip()
        data = (consulta,)
        sql = "SELECT * FROM productos WHERE producto = ?;"
        con = self.conexion()
        cursor = con.cursor()
        datos = cursor.execute(sql, data).fetchall()
        self.limpiar_treeview(tree)
        if len(datos) <= 0:
            return "No existe el producto"
        else:
            for dato in datos:
                tree.insert("", 0, text=dato[0], values=(dato[1], dato[2], dato[3]))
            return None

    def borrar(self, input, error, tree):
        valor = tree.selection()
        print(valor)  # ('I005',)
        item = tree.item(valor)
        print(
            item
        )  # {'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
        print(item["text"])
        mi_id = item["text"]
        if mi_id == "":
            error.config(text="Seleccione elemento para borrar", fg="red")
        else:
            con = self.conexion()
            cursor = con.cursor()
            # mi_id = int(mi_id)
            data = (mi_id,)
            sql = "DELETE FROM productos WHERE id = ?;"
            cursor.execute(sql, data)
            con.commit()
            tree.delete(valor)
            input.set("")
            error.config(text="Elemento borrado exitosamente", fg="red")
