from tkinter import *
from tkinter import ttk

def style():
    """Configure the style of the application"""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("notebook.TNotebook.Tab", padding=10, font=(None, 16))
    style.configure("btns.TButton", font=(None, 13))
    style.configure("heading.TLabel", font=(None, 20))
    style.configure("heading2.TLabel", font=(None, 14))
    style.configure("txt.TLabel", font=(None, 12))
    style.configure("txt.TEntry", font=(None, 12))
    return style