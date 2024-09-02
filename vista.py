from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import modelo


# ##############################################
# VISTA
# ##############################################
class Panel:
    def __init__(self, window):
        self.root = window
        self.root.title("STOCK")
        self.titulo = Label(
            self.root,
            text="G e s t i o n   d e   P r o d u c t o s",
            bg="SteelBlue1",
            height=2,
            width=60,
        )
        self.titulo.grid(row=0, column=0, columnspan=5, pady=5, sticky=W + E)

        self.objeto = modelo.Abmc()

        try:
            self.objeto.conexion()
            self.objeto.crear_tabla()
        except:
            print("Error")

        self.producto = Label(self.root, text="Producto")
        self.producto.grid(row=1, column=0, padx=15, pady=5, sticky=W)
        self.cantidad = Label(self.root, text="Cantidad")
        self.cantidad.grid(row=2, column=0, padx=15, pady=5, sticky=W)
        self.precio = Label(self.root, text="Precio")
        self.precio.grid(row=3, column=0, padx=15, pady=(0, 5), sticky=W)

        # Defino variables para tomar valores de campos de entrada
        self.a_val, self.b_val, self.c_val = StringVar(), StringVar(), StringVar()
        w_ancho = 21

        self.error1 = Label(self.root, text="", fg="red")
        self.error1.grid(row=1, column=2, columnspan=3)
        self.error2 = Label(self.root, text="", fg="red")
        self.error2.grid(row=2, column=2, columnspan=3)
        self.error3 = Label(self.root, text="", fg="red")
        self.error3.grid(row=3, column=2, columnspan=3)

        # Register validation
        self.vcmd = self.root.register(self.validate_length)

        # INPUTS
        self.entrada1 = Entry(
            self.root,
            textvariable=self.a_val,
            width=w_ancho,
            validate="key",
            validatecommand=(self.vcmd, "%P", 20),
        )
        self.entrada1.grid(row=1, column=1)
        self.entrada1.bind("<Button-1>", lambda _: self.clear(self.a_val, self.error1))
        self.entrada2 = Entry(self.root, textvariable=self.b_val, width=w_ancho)
        self.entrada2.grid(row=2, column=1)
        self.entrada2.bind("<Button-1>", lambda _: self.clear(self.b_val, self.error2))
        self.entrada3 = Entry(self.root, textvariable=self.c_val, width=w_ancho)
        self.entrada3.grid(row=3, column=1)
        self.entrada3.bind("<Button-1>", lambda _: self.clear(self.c_val, self.error3))

        # --------------------------------------------------
        # TREEVIEW
        # --------------------------------------------------

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("col1", "col2", "col3")
        self.tree.column("#0", width=90, minwidth=50)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80, anchor="center")
        self.tree.column("col3", width=200, minwidth=80, anchor="center")
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Producto")
        self.tree.heading("col2", text="Cantidad")
        self.tree.heading("col3", text="Precio")
        self.tree.grid(row=10, column=0, columnspan=4, pady=(5, 0))

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=10, column=4, sticky="ns")

        def on_treeview_click(event):
            self.clear_errors()

        self.tree.bind("<Button-1>", on_treeview_click)

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        self.boton_alta = Button(
            self.root,
            text="Alta",
            width=w_ancho - 5,
            command=lambda: self.validate_create(),
        )
        self.boton_alta.grid(row=4, column=1, pady=5)

        self.boton_consulta = Button(
            self.root,
            text="Consultar",
            width=w_ancho - 5,
            command=lambda: self.validate_query(),
        )
        self.boton_consulta.grid(row=5, column=1, pady=5)

        self.boton_borrar = Button(
            self.root,
            text="Borrar",
            width=w_ancho - 5,
            command=lambda: self.objeto.borrar(self.a_val, self.error1, self.tree),
        )
        self.boton_borrar.grid(row=6, column=1, pady=5)

        self.boton_listar = Button(
            self.root,
            text="Listar productos",
            command=lambda: self.objeto.actualizar_treeview(self.tree),
        )
        self.boton_listar.grid(row=4, column=3, pady=5)

        self.boton_limpiar = Button(
            self.root,
            text="Limpiar",
            command=lambda: self.clear_all(),
        )
        self.boton_limpiar.grid(row=6, column=3, pady=5)

    def clear_error(self, error):
        error.config(text="")

    def clear_errors(
        self,
    ):
        self.clear_error(self.error1)
        self.clear_error(self.error2)
        self.clear_error(self.error3)

    def clear(self, input, error):
        self.clear_error(error)
        input.set("")

    def clear_all(
        self,
    ):
        self.clear_errors()
        self.objeto.limpiar_treeview(self.tree)

    # VALIDATIONS #
    def validate_length(self, char, max_length):
        max_char = len(char)
        max_len = int(max_length)
        if max_char == max_len:
            self.error1.config(text="Maximo 20 caracteres")
        return max_char <= max_len

    def is_empty(self, input):
        return input.get().strip() == ""

    def validate_create(
        self,
    ):
        valid_product = self.validate_product()
        valid_quantity = self.validate_quantity()
        valid_price = self.validate_price()
        if valid_product and valid_quantity and valid_price:
            response = self.objeto.alta(self.a_val, self.b_val, self.c_val, self.tree)
            if response:
                self.error1.config(text=response)

    def validate_query(
        self,
    ):
        self.clear_error(self.error1)
        if self.is_empty(self.a_val):
            self.error1.config(text="Ingrese producto a consultar")
        else:
            response = self.objeto.consultar(self.a_val, self.tree)
            if response != None:
                self.error1.config(text=response)

    def validate_product(
        self,
    ):
        if self.is_empty(self.a_val):
            self.error1.config(text="Ingrese producto")
            return False
        else:
            return True

    def validate_quantity(
        self,
    ):
        if self.is_empty(self.b_val):
            self.error2.config(text="Ingrese cantidad")
            return False
        else:
            return True

    def validate_price(
        self,
    ):
        if self.is_empty(self.c_val):
            self.error3.config(text="Ingrese precio")
            return False
        else:
            return True
