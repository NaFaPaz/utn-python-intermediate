from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk


# ##############################################
# VISTA
# ##############################################
class View:
    def __init__(self, window, controller):
        self.root = window
        self.controlador = controller
        self.root.title("STOCK")
        self.titulo = Label(
            self.root,
            text="G e s t i o n   d e   P r o d u c t o s",
            bg="SteelBlue1",
            height=2,
            width=60,
        )
        self.titulo.grid(row=0, column=0, columnspan=5, pady=5, sticky=W + E)

        self.producto = Label(self.root, text="Producto")
        self.producto.grid(row=1, column=0, padx=15, pady=(5, 0), sticky=W)
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
        self.vcmd = self.root.register(self.validar_longitud)

        # INPUTS
        self.entrada1 = Entry(
            self.root,
            textvariable=self.a_val,
            width=w_ancho,
            validate="key",
            validatecommand=(self.vcmd, "%P", 20),
        )
        self.entrada1.grid(row=1, column=1)
        self.entrada1.bind(
            "<Button-1>", lambda _: self.limpiar(self.a_val, self.error1)
        )
        self.entrada2 = Entry(self.root, textvariable=self.b_val, width=w_ancho)
        self.entrada2.grid(row=2, column=1)
        self.entrada2.bind(
            "<Button-1>", lambda _: self.limpiar(self.b_val, self.error2)
        )
        self.entrada3 = Entry(self.root, textvariable=self.c_val, width=w_ancho)
        self.entrada3.grid(row=3, column=1)
        self.entrada3.bind(
            "<Button-1>", lambda _: self.limpiar(self.c_val, self.error3)
        )

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
            self.limpiar_errores()

        self.tree.bind("<Button-1>", on_treeview_click)

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        self.boton_alta = Button(
            self.root,
            text="Alta",
            width=w_ancho - 5,
            command=lambda: self.controlador.alta(),
        )
        self.boton_alta.grid(row=4, column=1, pady=5)

        self.boton_consulta = Button(
            self.root,
            text="Consultar",
            width=w_ancho - 5,
            command=lambda: self.controlador.consulta(self.a_val),
        )
        self.boton_consulta.grid(row=5, column=1, pady=5)

        self.boton_borrar = Button(
            self.root,
            text="Borrar",
            width=w_ancho - 5,
            command=lambda: self.controlador.borrar(),
        )
        self.boton_borrar.grid(row=6, column=1, pady=5)

        self.boton_listar = Button(
            self.root,
            text="Listar productos",
            command=lambda: self.controlador.listar(),
        )
        self.boton_listar.grid(row=4, column=3, pady=5)

        self.boton_limpiar = Button(
            self.root,
            text="Limpiar",
            command=lambda: self.limpiar_todo(),
        )
        self.boton_limpiar.grid(row=6, column=3, pady=5)

    def limpiar_treeview(
        self,
    ):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def limpiar_error(self, error):
        error.config(text="")

    def limpiar_errores(
        self,
    ):
        self.limpiar_error(self.error1)
        self.limpiar_error(self.error2)
        self.limpiar_error(self.error3)

    def limpiar(self, input, error):
        self.limpiar_error(error)
        input.set("")

    def limpiar_todo(
        self,
    ):
        self.limpiar_errores()
        self.limpiar_treeview()

    def validar_longitud(self, char, max_length):
        max_char = len(char)
        max_len = int(max_length)
        if max_char == max_len:
            self.error1.config(text="Maximo 20 caracteres")
        return max_char <= max_len
