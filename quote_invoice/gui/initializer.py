from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .home import HomeTab
from .customer_list import CustomerListTab
from .quotation_list import QuotationListTab
from .customer_details import CustomerDetailsTab
from .quote_details import QuoteDetailsTab
from .order_list import OrderListTab
from .order_details import OrderDetailsTab

def get_connection():
    return create_engine(f"sqlite:///app_database.db")

# class DatabaseOps():
engine = get_connection()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Window():
    """ Initialize the main window of the application"""
    def __init__(self, root):
        self.root = root
        self.root.title("Quote & Invoice")
        self.selected_customer = None
        self.selected_quotation = None
        self.selected_order = None
        self.selected_quote = None
        self.selected_order = None
        # self.customer_id_name_dict = dict()

        # Styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("notebook.TNotebook.Tab", padding=10, font=(None, 16))
        style.configure("home_btns.TButton", font=(None, 24))
        style.configure("heading.TLabel", font=(None, 31))
        style.configure(
            "main_menu.TLabel", 
            font=(None, 24), 
            background="blue",
            foreground="white"
        )
        self.create_notebook()
        self.configure_rows_columns()
        self.home_tab = self.setup_home_tab()
        self.customer_details_tab = self.setup_customer_tab()
        self.customer_list_tab = self.setup_customer_list_tab()
        self.quote_details_tab = self.setup_quote_tab()
        self.quotation_list_tab = self.setup_quotation_list_tab()
        self.order_details_tab = self.setup_order_tab()
        self.order_list_tab = self.setup_order_list_tab()

    
    def create_notebook(self):
        """Create a Notebook and Frames"""
        self.notebook = ttk.Notebook(self.root, style="notebook.TNotebook",)
        self.home_frame = ttk.Frame(self.notebook)
        self.customer_list_frame = ttk.Frame(self.notebook)
        self.customer_frame = ttk.Frame(self.notebook)
        self.quotation_list_frame = ttk.Frame(self.notebook)
        self.quotation_frame = ttk.Frame(self.notebook)
        self.order_list_frame = ttk.Frame(self.notebook)
        self.order_frame = ttk.Frame(self.notebook)

        # Add tabs/pages to the Notebook
        self.notebook.add(self.home_frame, text="Home")
        self.notebook.add(self.customer_list_frame, text="Customer List")
        self.notebook.add(self.customer_frame, text="Customer Details")
        self.notebook.add(self.quotation_list_frame, text="Quotation List")
        self.notebook.add(self.quotation_frame, text="Quote Details")
        self.notebook.add(self.order_list_frame, text="Order List")
        self.notebook.add(self.order_frame, text="Order Details")
        
        # Grid Notebook
        self.notebook.grid(column=0, row=0, columnspan=2, rowspan=12, sticky=(N, W, E, S))

    def configure_rows_columns(self):
        """Configure the rows and columns resizing behaviour"""
        # Root
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)

        self.home_frame.columnconfigure(0, weight=1)
        self.home_frame.columnconfigure(1, weight=1)
        self.home_frame.rowconfigure(0, weight=1)
        self.home_frame.rowconfigure(1, weight=1)
        self.home_frame.rowconfigure(2, weight=1)

        self.customer_list_frame.columnconfigure(0, weight=1)
        self.customer_list_frame.columnconfigure(1, weight=1)
        self.customer_list_frame.rowconfigure(0, weight=1)
        self.customer_list_frame.rowconfigure(1, weight=1)
        self.customer_list_frame.rowconfigure(2, weight=1)

        self.customer_frame.columnconfigure(0, weight=1)
        self.customer_frame.columnconfigure(1, weight=1)
        self.customer_frame.rowconfigure(0, weight=1)
        self.customer_frame.rowconfigure(1, weight=1)
        self.customer_frame.rowconfigure(2, weight=1)

        self.quotation_list_frame.columnconfigure(0, weight=1)
        self.quotation_list_frame.columnconfigure(1, weight=1)
        self.quotation_list_frame.rowconfigure(0, weight=1)
        self.quotation_list_frame.rowconfigure(1, weight=1)
        self.quotation_list_frame.rowconfigure(2, weight=1)

        self.quotation_frame.columnconfigure(0, weight=1)
        self.quotation_frame.columnconfigure(1, weight=1)
        self.quotation_frame.rowconfigure(0, weight=1)
        self.quotation_frame.rowconfigure(1, weight=1)
        self.quotation_frame.rowconfigure(2, weight=1)

        self.order_list_frame.columnconfigure(0, weight=1)
        self.order_list_frame.columnconfigure(1, weight=1)
        self.order_list_frame.rowconfigure(0, weight=1)
        self.order_list_frame.rowconfigure(1, weight=1)
        self.order_list_frame.rowconfigure(2, weight=1)

        self.order_frame.columnconfigure(0, weight=1)
        self.order_frame.columnconfigure(1, weight=1)
        self.order_frame.rowconfigure(0, weight=1)
        self.order_frame.rowconfigure(1, weight=1)
        self.order_frame.rowconfigure(2, weight=1)

    def setup_home_tab(self):
        home_tab = HomeTab(self.notebook, self.home_frame)
        return home_tab

    def setup_customer_tab(self):
        customer_details_tab = CustomerDetailsTab(self.notebook, self.customer_frame, session)
        return customer_details_tab
    
    def setup_customer_list_tab(self):
        customer_list_tab = CustomerListTab(
            self.notebook, 
            self.customer_list_frame, 
            self.customer_details_tab, 
            session
        )
        return customer_list_tab
    
    def setup_quote_tab(self):
        quote_details_tab = QuoteDetailsTab(self.notebook, self.quotation_frame, session)
        return quote_details_tab
    
    def setup_quotation_list_tab(self):
        quotation_list_tab = QuotationListTab(
            self.notebook, 
            self.quotation_list_frame, 
            self.quote_details_tab, 
            session
        )
        return quotation_list_tab
    # Pass customer_details_tab object to the list_tab object, enables calling customer_details_tab methods from list
    def setup_order_tab(self):
        order_details_tab = OrderDetailsTab(self.notebook, self.order_frame, session)
        return order_details_tab
    
    def setup_order_list_tab(self):
        order_list_tab = OrderListTab(
            self.notebook, 
            self.order_list_frame, 
            self.order_details_tab, 
            session
        )
        return order_list_tab