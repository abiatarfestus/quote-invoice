from tkinter import *
from tkinter import ttk
from main_window import MainWindow

root = Tk()
root.geometry("500x500")
MainWindow(root)
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
root.mainloop()
