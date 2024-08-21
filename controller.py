from tkinter import Tk
import vista


class Controller:
    def __init__(self, root):
        self.root = root
        self.objeto_vista = vista.Panel(self.root)


if __name__ == "__main__":
    root = Tk()
    # Screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Window dimensions
    root.update_idletasks()  # This ensures that the geometry information is up-to-date
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    # Window starting position
    x_position = (screen_width // 2) - (current_width * 2)
    y_position = (screen_height // 2) - (current_height * 2)
    root.geometry(f"+{x_position}+{y_position}")

    mi_app = Controller(root)
    root.mainloop()
