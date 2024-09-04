from tkinter import Tk
from vista import View
from modelo import Model


class Controller:
    def __init__(self, root):
        self.root = root
        self.modelo = Model()
        self.vista = View(self.root, self)

    def alta(
        self,
    ):
        self.validar_alta()

    def consulta(self, producto):
        resultado = self.validar_consulta(producto)
        if len(resultado) <= 0:
            self.vista.error1.config(text="Producto no encontrado")
        else:
            self.vista.limpiar_treeview()
            for dato in resultado:
                self.vista.tree.insert(
                    "", 0, text=dato[0], values=(dato[1], dato[2], dato[3])
                )

    def borrar(
        self,
    ):
        seleccion = self.vista.tree.selection()
        item = self.vista.tree.item(seleccion)
        id = item["text"]
        if id == "":
            self.vista.error1.config(text="Seleccione 1 elemento del listado")
        else:
            resultado = self.modelo.borrar(id)
            if resultado:
                self.vista.error1.config(text=resultado)
                self.vista.limpiar_treeview()

    def listar(
        self,
    ):
        self.vista.limpiar_todo()
        resultado = self.modelo.productos()
        if len(resultado) <= 0:
            self.vista.error1.config(text="No se encontraron productos")
        else:
            for fila in resultado:
                self.vista.tree.insert(
                    "", 0, text=fila[0], values=(fila[1], fila[2], fila[3])
                )

    def validar_alta(
        self,
    ):
        producto_valido = self.validar_input(
            self.vista.a_val, self.vista.error1, "Ingrese producto"
        )
        cantidad_valida = self.validar_input(
            self.vista.b_val, self.vista.error2, "Ingrese cantidad"
        )
        precio_valido = self.validar_input(
            self.vista.c_val, self.vista.error3, "Ingrese precio"
        )
        if producto_valido and cantidad_valida and precio_valido:
            resultado = self.modelo.alta(
                self.vista.a_val, self.vista.b_val, self.vista.c_val
            )
            if resultado:
                self.vista.error1.config(text=resultado)

    def es_vacio(self, input):
        return input.get().strip() == ""

    def validar_consulta(self, producto):
        self.vista.limpiar_error(self.vista.error1)
        if self.es_vacio(producto):
            self.vista.error1.config(text="Ingrese producto a consultar")
            return []
        else:
            return self.modelo.consultar(producto)

    def validar_input(self, input, error, error_text):
        if self.es_vacio(input):
            error.config(text=error_text)
            return False
        else:
            return True


if __name__ == "__main__":
    root = Tk()
    # Screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Window dimensions
    root.update_idletasks()
    current_width = root.winfo_width()
    current_height = root.winfo_height()
    root.resizable(False, False)
    # Window starting position
    x_position = (screen_width // 2) - (current_width * 2)
    y_position = (screen_height // 2) - (current_height * 2)
    root.geometry(f"+{x_position}+{y_position}")

    mi_app = Controller(root)
    root.mainloop()
