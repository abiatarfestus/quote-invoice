from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style

def style():
    """Configure the style of the application"""
    # style = ttk.Style()
    style = Style()
    style.theme_use("flatly")
    style.configure(".", font=("Segoe UI", 10))
    style.configure("TNotebook.Tab", padding=10, font=("Segoe UI", 16))
    style.configure("TButton", font=("Segoe UI", 13))
    style.configure("heading.TLabel", font=("Segoe UI", 20))
    style.configure("heading2.TLabel", font=("Segoe UI", 14))
    style.configure("TLabel", font=("Segoe UI", 12))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=20)
    style.configure("ErrorLabel.TLabel", foreground="Red")
    # style.configure("txt.TEntry", font=("Segoe UI", 16))
    # style.configure("txt.TCombobox", font=("Segoe UI", 16))
    return style