from tkinter import Tk
from vista import View
from modelo import Model


class Controller:
    def __init__(self, root):
        """
        Inicializa una nueva instancia de la clase `Controller`.

        Configura la instancia de `Model`, `View`, y el objeto raíz de la aplicación.

        :param root: La ventana raíz de la aplicación.
        :type root: tkinter.Tk
        :return: None
        :rtype: None
        """
        self.root = root
        self.modelo = Model()
        self.vista = View(self.root, self)

    def alta(
        self,
    ):
        """
        Maneja el proceso de alta de un nuevo producto.

        Llama a la función `validar_alta` para validar y agregar un nuevo producto.

        :return: None
        :rtype: None
        """
        self.validar_alta()

    def consulta(self, producto):
        """
        Realiza una consulta de productos basado en el nombre proporcionado.

        Muestra un mensaje de error si el producto no se encuentra. De lo contrario, limpia la vista y muestra los resultados.

        :param producto: El nombre del producto a consultar.
        :type producto: tkinter.StringVar
        :return: None
        :rtype: None
        """
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
        """
        Maneja el proceso de eliminación de un producto.

        Elimina el producto seleccionado de la vista. Muestra un mensaje de error si no se selecciona ningún elemento.

        :return: None
        :rtype: None
        """
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
        """
        Lista todos los productos disponibles en la vista.

        Limpia la vista y muestra todos los productos almacenados. Muestra un mensaje de error si no se encuentran productos.

        :return: None
        :rtype: None
        """
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
        """
        Valida los campos de entrada y agrega un nuevo producto si los datos son válidos.

        Valida los campos de entrada para el nombre del producto, cantidad y precio. Si todos los datos son válidos, llama a la función `alta` de `Model`.

        :return: None
        :rtype: None
        """
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
        """
        Verifica si el campo de entrada está vacío.

        :param input: El campo de entrada a verificar.
        :type input: tkinter.StringVar
        :return: `True` si el campo de entrada está vacío, de lo contrario `False`.
        :rtype: bool
        """
        return input.get().strip() == ""

    def validar_consulta(self, producto):
        """
        Valida el campo de entrada para la consulta y retorna los resultados de la consulta.

        Limpia el error de la vista y valida que el campo de producto no esté vacío antes de realizar la consulta.

        :param producto: El nombre del producto a consultar.
        :type producto: tkinter.StringVar
        :return: Lista de tuplas con los datos de los productos que coinciden.
        :rtype: list of tuples
        """
        self.vista.limpiar_error(self.vista.error1)
        if self.es_vacio(producto):
            self.vista.error1.config(text="Ingrese producto a consultar")
            return []
        else:
            return self.modelo.consultar(producto)

    def validar_input(self, input, error, error_text):
        """
        Valida si el campo de entrada no está vacío y muestra un mensaje de error si es necesario.

        :param input: El campo de entrada a validar.
        :type input: tkinter.StringVar
        :param error: El widget de error donde se mostrará el mensaje.
        :type error: tkinter.Label
        :param error_text: El mensaje de error a mostrar.
        :type error_text: str
        :return: `True` si el campo de entrada no está vacío, de lo contrario `False`.
        :rtype: bool
        """
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
