from tkinter import *
from tkinter import ttk
# from main_window import MainWindow
from main_window import MainWindow

root = Tk()
# root.geometry("500x500")
app = MainWindow(root)
app.setup_home_tab()
app.setup_customer_list_tab()
app.setup_customer_form_tab()
app.configure_rows_columns()

# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
root.mainloop()
