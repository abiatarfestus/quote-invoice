from tkinter import *
from tkinter import ttk

def style():
    """Configure the style of the application"""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("notebook.TNotebook.Tab", padding=10, font=(None, 16))
    style.configure("home_btns.TButton", font=(None, 16))
    style.configure("heading.TLabel", font=(None, 31))
    return style