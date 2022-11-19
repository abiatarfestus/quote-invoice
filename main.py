from tkinter import *
from tkinter import ttk
# from main_window import MainWindow
from main_window import MainWindow
from models import get_connection, Base

def main():
    engine = get_connection()
    Base.metadata.create_all(engine)
    
    root = Tk()
    root.state('zoomed')
    # root.geometry("500x500")

    app = MainWindow(root)
    app.setup_home_tab()
    app.setup_customer_list_tab()
    app.setup_customer_tab()
    app.setup_quotation_list_tab()
    app.setup_quotation_tab()
    app.setup_order_list_tab()
    app.setup_order_tab()
    app.configure_rows_columns()

    # root.columnconfigure(0, weight=1)
    # root.rowconfigure(0, weight=1)
    root.mainloop()

if __name__ == "__main__":
    main()