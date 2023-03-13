from tkinter import *
from tkinter import ttk
# from main_window import MainWindow
from .gui.initializer import Window
from .db.models import get_connection, Base

def run():
    engine = get_connection()
    Base.metadata.create_all(engine)
    root = Tk()
    root.state('zoomed')
    # root.geometry("500x500")
    app = Window(root)
    root.mainloop()
