from datetime import datetime
import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from faker import Faker
from sqlalchemy import and_, or_, create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Order, OrderItem, Quotation, QuotationItem, Product

fake = Faker()

def get_connection():
    return create_engine(f"sqlite:///app_database.db")

# class DatabaseOps():
engine = get_connection()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class MainWindow():
    """ Initialize the main window of the application"""
    def __init__(self, root):
        self.root = root
        self.root.title("Quote & Invoice")
        self.selected_customer = None
        self.selected_quote = None
        self.selected_order = None

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

        # Create a Notebook and Frames
        self.notebook = ttk.Notebook(self.root, style="notebook.TNotebook",)
        self.home_frame = ttk.Frame(self.notebook)
        self.customer_list_frame = ttk.Frame(self.notebook)
        self.customer_frame = ttk.Frame(self.notebook)
        self.quotation_list_frame = ttk.Frame(self.notebook)
        self.quotations_frame = ttk.Frame(self.notebook)
        self.order_list_frame = ttk.Frame(self.notebook)
        self.orders_frame = ttk.Frame(self.notebook)

        # Add tabs/pages to the Notebook
        self.notebook.add(self.home_frame, text="Home")
        self.notebook.add(self.customer_list_frame, text="Customer List")
        self.notebook.add(self.customer_frame, text="Customer Details")
        self.notebook.add(self.quotation_list_frame, text="Quotation List")
        self.notebook.add(self.quotations_frame, text="Quote Details")
        self.notebook.add(self.order_list_frame, text="Order List")
        self.notebook.add(self.orders_frame, text="Order Details")
        
        # Grid Notebook
        self.notebook.grid(column=0, row=0, columnspan=2, rowspan=12, sticky=(N, W, E, S))


    def setup_home_tab(self):
        """Configure the home tab page"""
        # Frames
        top_frame = ttk.Frame(
            self.home_frame,
            borderwidth=5, 
            # relief="solid"
        )
        mid_frame = ttk.Frame(
            self.home_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.home_frame,
            borderwidth=5, 
            # relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(W, E, S))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Quote & Invoice v0.0.1",
            anchor="center",
            style="heading.TLabel",
        )

        main_menu_lbl = ttk.Label(
            mid_frame,
            text="Main Menu",
            anchor="center",
            style="main_menu.TLabel",
            padding=(180,2)
        )

        creator_lbl = ttk.Label(
            bottom_frame,
            text="Created by Festus Abiatar",
            anchor="e",
        )

        heading_lbl.grid(row=0)
        main_menu_lbl.grid(column=0, row=0, columnspan=2)
        creator_lbl.grid(column=1, row=0, sticky=(S, E))

        # Buttons
        customer_list_btn = ttk.Button(
            mid_frame,
            text="Customer List",
            style="home_btns.TButton",
            padding=26
        )
        customer_btn = ttk.Button(
            mid_frame, 
            text="Customer Details",
            style="home_btns.TButton",
            padding=(15, 26)
        )
        quotations_btn = ttk.Button(
            mid_frame, 
            text="Quotations",
            style="home_btns.TButton",
            padding=26
        )
        orders_invoies_btn = ttk.Button(
            mid_frame, 
            text="Orders/Invoices",
            style="home_btns.TButton",
            padding=(15, 26)
        )

        customer_list_btn.grid(column=0, row=1, sticky=E)
        customer_btn.grid(column=0, row=2, sticky=E)
        quotations_btn.grid(column=1, row=1, sticky=W)
        orders_invoies_btn.grid(column=1, row=2, sticky=W)

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.rowconfigure(1, weight=1)

        for child in mid_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def setup_customer_list_tab(self):
        """Configure the customer list tab"""
        # Frames
        top_frame = ttk.Frame(
            self.customer_list_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.customer_list_frame, 
            borderwidth=5, 
            relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.customer_list_frame,
            borderwidth=5, 
            relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Customer List",
            anchor="center",
            style="heading.TLabel",
        )

        heading_lbl.grid(row=0)

        def select_record(event):
            print("Record selected")
            record = tree.focus()
            self.selected_customer = tree.item(record)
        
        def add_new_customer():
            self.id_ent.state(["!disabled"])
            self.id_ent.delete(0, END)
            self.id_ent.state(["disabled"])
            self.type_cbx.set("")
            self.first_name_ent.delete(0, END)
            self.last_name_ent.delete(0, END)
            self.entity_ent.delete(0, END)
            self.email_ent.delete(0, END)
            self.phone_ent.delete(0, END)
            self.address_ent.delete(0, END)
            self.town_ent.delete(0, END)
            self.country_ent.delete(0, END)
            self.since_ent.delete(0, END)
            self.notes_txt.delete("1.0", END)
            self.notebook.select(self.customer_frame)
        
        def view_customer():
            print(f"SELECTED RECORD: {self.selected_customer}")
            customer = self.selected_customer
            if not self.selected_customer:
                error_message = messagebox.showerror(
                    message='No record is selected!',
                    title='Error'
                )
                return error_message
            self.id_ent.state(["!disabled"])
            self.id_ent.delete(0, END)
            self.id_ent.insert(0, customer['values'][0])
            self.id_ent.state(["disabled"])
            self.type_cbx.set(customer['values'][1])
            self.first_name_ent.delete(0, END)
            self.first_name_ent.insert(0, customer['values'][2])
            self.last_name_ent.delete(0, END)
            self.last_name_ent.insert(0, customer['values'][3])
            self.entity_ent.delete(0, END)
            self.entity_ent.insert(0, customer['values'][4])
            self.email_ent.delete(0, END)
            self.email_ent.insert(0, customer['values'][6])
            self.phone_ent.delete(0, END)
            self.phone_ent.insert(0, customer['values'][7])
            self.address_ent.delete(0, END)
            self.address_ent.insert(0, customer['values'][8])
            self.town_ent.delete(0, END)
            self.town_ent.insert(0, customer['values'][9])
            self.country_ent.delete(0, END)
            self.country_ent.insert(0, customer['values'][10])
            self.since_ent.delete(0, END)
            self.since_ent.insert(0, customer['values'][11])
            self.notes_txt.delete("1.0", END)
            self.notes_txt.insert("1.0", customer['values'][12])
            self.notebook.select(self.customer_frame)

        # Buttons
        open_customer_btn = ttk.Button(
            bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21,
            command=view_customer
        )
        add_customer_btn = ttk.Button(
            bottom_frame, 
            text="Add New Customer",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=add_new_customer
        )
        search_customer_btn = ttk.Button(
            bottom_frame, 
            text="Search Customer",
            # style="home_btns.TButton",
            padding=(10, 21)
        )


        open_customer_btn.grid(column=0, row=1, sticky=E)
        add_customer_btn.grid(column=1, row=1, sticky=E)
        search_customer_btn.grid(column=2, row=1, sticky=E)

        # Treeview
        tree = ttk.Treeview(mid_frame, show='headings', height=20)
        tree.bind('<ButtonRelease-1>', select_record)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
        x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
        y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
        x_scroll.grid(column=0, row=1, sticky=(E, W))
        tree['yscrollcommand'] = y_scroll.set
        tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        tree["columns"] = (
            "ID",
            "Customer Type",
            "First Name",
            "Last Name",
            "Entity Name",
            "Customer Name",
            "Email",
            "Phone",
            "Address",
            "Town",
            "Country",
            "Customer Since",
            "Notes"
        )

        # Columns to display
        tree["displaycolumns"] = (
            "ID",
            "Customer Name",
            "Town",
            "Phone",
            "Email",
            "Customer Since"
        )

        # Format Our Columns
        tree.column("ID", anchor=CENTER)
        tree.column("Customer Name", anchor=W)
        tree.column("Town", anchor=W)
        tree.column("Phone", anchor=W)
        tree.column("Email", anchor=W)
        tree.column("Customer Since", anchor=E)
        # tree.column("Customer Type", anchor=W)
        # tree.column("First Name", anchor=W)
        # tree.column("Last Name", anchor=W)
        # tree.column("Entity Name", anchor=W)
        # tree.column("Address", anchor=W)
        # tree.column("Country", anchor=W)
        # tree.column("Notes", anchor=W)

        # Create Headings
        tree.heading("ID", text="ID", anchor=CENTER)
        tree.heading("Customer Name", text="Customer Name", anchor=W)
        tree.heading("Town", text="Town", anchor=W)
        tree.heading("Phone", text="Phone", anchor=W)
        tree.heading("Email", text="Email", anchor=W)
        tree.heading("Customer Since", text="Customr Since", anchor=E)
        # tree.heading("Customer Type", text="Customer Type", anchor=W)
        # tree.heading("First Name", text="First Name", anchor=W)
        # tree.heading("Last Name", text="Last Name", anchor=W)
        # tree.heading("Entity Name", text="Entity Name", anchor=W)
        # tree.heading("Address", text="Address", anchor=W)
        # tree.heading("Country", text="Country", anchor=W)
        # tree.heading("Notes", text="Notes", anchor=W)

        # Insert the data in Treeview widget
        customers = session.query(Customer).order_by(Customer.customer_id).all()
        print(f"TOTAL CUSTOMERS: {len(customers)}")
        # for i in range(1, total_customers+1):
        for customer in customers:
            if customer.first_name and customer.last_name:
                customer_name = f"{customer.last_name} {customer.first_name}"
            else:
                customer_name = customer.entity_name
            tree.insert('', 'end', iid=f"{customer.customer_id}",
            values=(
                f"{customer.customer_id}",
                customer.customer_type,
                customer.first_name,
                customer.last_name,
                customer.entity_name,
                customer_name,
                customer.email,
                customer.phone,
                customer.address,
                customer.town,
                customer.country,
                customer.customer_since,
                customer.notes
                )
            )

        # for i in range(1,21):
        #     tree.insert('', 'end', values=(
        #         f"{i}",
        #         fake.last_name(),
        #         fake.first_name(),
        #         fake.city(),
        #         fake.company(),
        #         datetime.strptime(fake.date(), '%Y-%m-%d').date()
        #         )
        #     )

        tree.grid(column=0, row=0, sticky=(N, S, W, E))

        

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)

    def setup_customer_tab(self):
        """Configure the customer form tab"""
        # Frames
        top_frame = ttk.Frame(
            self.customer_frame,
            borderwidth=5, 
            # relief="solid"
        )
        mid_frame = ttk.Frame(
            self.customer_frame, 
            borderwidth=5, 
            relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.customer_frame,
            borderwidth=5, 
            # relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # Labels
        heading_lbl = ttk.Label(
            top_frame,
            text="Customer Details",
            anchor="center",
            style="heading.TLabel",
        )
        id_lbl = ttk.Label(
            mid_frame,
            text="Customer ID",
            anchor=W,
            # style="heading.TLabel",
        )
        type_lbl = ttk.Label(
            mid_frame,
            text="Customer Type",
            anchor=W,
            # style="heading.TLabel",
        )
        first_name_lbl = ttk.Label(
            mid_frame,
            text="First Name",
            anchor=W,
            # style="heading.TLabel",
        )
        last_name_lbl = ttk.Label(
            mid_frame,
            text="Last Name",
            anchor=W,
            # style="heading.TLabel",
        )
        entity_lbl = ttk.Label(
            mid_frame,
            text="Entity Name",
            anchor=W,
            # style="heading.TLabel",
        )
        email_lbl = ttk.Label(
            mid_frame,
            text="Email",
            anchor=W,
            # style="heading.TLabel",
        )
        phone_lbl = ttk.Label(
            mid_frame,
            text="Phone",
            anchor=W,
            # style="heading.TLabel",
        )
        address_lbl = ttk.Label(
            mid_frame,
            text="Address",
            anchor=W,
            # style="heading.TLabel",
        )
        town_lbl = ttk.Label(
            mid_frame,
            text="Town",
            anchor=W,
            # style="heading.TLabel",
        )
        country_lbl = ttk.Label(
            mid_frame,
            text="Country",
            anchor=W,
            # style="heading.TLabel",
        )
        since_lbl = ttk.Label(
            mid_frame,
            text="Customer Since",
            anchor=W,
            # style="heading.TLabel",
        )
        notes_lbl = ttk.Label(
            mid_frame,
            text="Notes",
            anchor=E,
            # style="heading.TLabel",
        )

        heading_lbl.grid(row=0, sticky=(N, S, W, E))
        id_lbl.grid(column=0, row=1, sticky=(W, ))
        type_lbl.grid(column=0, row=2, sticky=(W, ))
        first_name_lbl.grid(column=0, row=3, sticky=(W, ))
        last_name_lbl.grid(column=0, row=4, sticky=(W, ))
        entity_lbl.grid(column=0, row=5, sticky=(W, ))
        email_lbl.grid(column=0, row=6, sticky=(W, ))
        phone_lbl.grid(column=0, row=7, sticky=(W, ))
        address_lbl.grid(column=0, row=8, sticky=(W, ))
        town_lbl.grid(column=0, row=9, sticky=(W, ))
        country_lbl.grid(column=0, row=10, sticky=(W, ))
        since_lbl.grid(column=0, row=11, sticky=(W, ))
        notes_lbl.grid(column=4, row=0, sticky=(E, ))

        # Entries
        self.id_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        # self.id_ent.state(["disabled"])

        self.first_name_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.last_name_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.entity_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.email_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.phone_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.address_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.town_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.country_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.since_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        # Comboboxes
        self.type_cbx = ttk.Combobox(
            mid_frame,
            width=38,
            values=("Person", "Entity")
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.type_cbx.state(["readonly"])

        # Texts
        self.notes_txt = Text(
            mid_frame,
            width=35, 
            height=9,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        self.id_ent.grid(column=1, row=1, sticky=(N, S, E, W))
        self.type_cbx.grid(column=1, row=2, sticky=(N, S, E, W))
        self.first_name_ent.grid(column=1, row=3, sticky=(N, S, E, W))
        self.last_name_ent.grid(column=1, row=4, sticky=(N, S, E, W))
        self.entity_ent.grid(column=1, row=5, sticky=(N, S, E, W))
        self.email_ent.grid(column=1, row=6, sticky=(N, S, E, W))
        self.phone_ent.grid(column=1, row=7, sticky=(N, S, E, W))
        self.address_ent.grid(column=1, row=8, sticky=(N, S, E, W))
        self.town_ent.grid(column=1, row=9, sticky=(N, S, E, W))
        self.country_ent.grid(column=1, row=10, sticky=(N, S, E, W))
        self.since_ent.grid(column=1, row=11, sticky=(N, S, E, W))
        self.notes_txt.grid(column=2, columnspan=3,row=1, rowspan=5, sticky=(N, S, E, W))

        # Buttons
        save_btn = ttk.Button(
            mid_frame,
            text="Save Record",
            # style="home_btns.TButton",
            padding=5
        )
        new_customer_btn = ttk.Button(
            mid_frame,
            text="New Customer",
            # style="home_btns.TButton",
            padding=5
        )
        orders_btn = ttk.Button(
            mid_frame, 
            text="Orders",
            # style="home_btns.TButton",
            padding=5
        )
        contacts_btn = ttk.Button(
            mid_frame, 
            text="Contacts",
            # style="home_btns.TButton",
            padding=5
        )

        save_btn.grid(column=0, columnspan=5, row=11, sticky=(E, W))
        new_customer_btn.grid(column=2, row=6, sticky=(N, S, E, W))
        orders_btn.grid(column=3, row=6, sticky=(N, S, E, W))
        contacts_btn.grid(column=4, row=6, sticky=(N, S, E, W))

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=5)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.columnconfigure(2, weight=1)
        mid_frame.columnconfigure(3, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)
        mid_frame.rowconfigure(2, weight=1)
        mid_frame.rowconfigure(3, weight=1)
        mid_frame.rowconfigure(4, weight=1)
        mid_frame.rowconfigure(5, weight=1)
        mid_frame.rowconfigure(6, weight=1)
        mid_frame.rowconfigure(7, weight=1)
        mid_frame.rowconfigure(8, weight=1)
        mid_frame.rowconfigure(9, weight=1)
        mid_frame.rowconfigure(10, weight=1)
        mid_frame.rowconfigure(11, weight=1)

        for child in mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=5)

    def setup_quotation_list_tab(self):
        """Configure the quotation list tab"""
        # Frames
        top_frame = ttk.Frame(
            self.quotation_list_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.quotation_list_frame, 
            borderwidth=5, 
            relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.quotation_list_frame,
            borderwidth=5, 
            relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Quotation List",
            anchor="center",
            style="heading.TLabel",
        )

        heading_lbl.grid(row=0)

        # Buttons
        open_quotation_btn = ttk.Button(
            bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21
        )
        add_quotation_btn = ttk.Button(
            bottom_frame, 
            text="Add New Quotation",
            # style="home_btns.TButton",
            padding=(10, 21)
        )
        search_quotation_btn = ttk.Button(
            bottom_frame, 
            text="Search Quotation",
            # style="home_btns.TButton",
            padding=(10, 21)
        )

        open_quotation_btn.grid(column=0, row=1, sticky=E)
        add_quotation_btn.grid(column=1, row=1, sticky=E)
        search_quotation_btn.grid(column=2, row=1, sticky=E)

        # Treeview
        tree = ttk.Treeview(mid_frame, show='headings', height=20)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
        x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
        y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
        x_scroll.grid(column=0, row=1, sticky=(E, W))
        tree['yscrollcommand'] = y_scroll.set
        tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        tree['columns'] = (
            "ID",
            "Customer",
            "Description",
            "Quote Date",
            "Accepted", 
            "Closed"
        )

        # Format Our Columns
        tree.column("ID", anchor=CENTER)
        tree.column("Customer", anchor=W)
        tree.column("Description", anchor=W)
        tree.column("Quote Date", anchor=E)
        tree.column("Accepted", anchor=CENTER)
        tree.column("Closed", anchor=CENTER)

        # Create Headings
        tree.heading("ID", text="ID", anchor=CENTER)
        tree.heading("Customer", text="Customer", anchor=W)
        tree.heading("Description", text="Description", anchor=W)
        tree.heading("Quote Date", text="Quote Date", anchor=E)
        tree.heading("Accepted", text="Accepted", anchor=CENTER)
        tree.heading("Closed", text="Closed", anchor=CENTER)

        # Insert the data in Treeview widget
        for i in range(1,21):
            tree.insert('', 'end', values=(
                f"{i}",
                fake.name(),
                fake.sentence(nb_words=3),
                datetime.strptime(fake.date(), '%Y-%m-%d').date(),
                random.choice(["Yes", "No"]),
                random.choice(["Yes", "No"]),
                )
            )

        tree.grid(column=0, row=0, sticky=(N, S, W, E))

        

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)

    def setup_quotations_tab(self):
        """Configure the quotations tab"""
        # Frames
        top_frame = ttk.Frame(
            self.quotations_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.quotations_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.quotations_frame,
            borderwidth=5, 
            relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Quotation Details",
            anchor="center",
            style="heading.TLabel",
        )
        id_lbl = ttk.Label(
            mid_frame,
            text="Quote ID",
            anchor=W,
            # style="heading.TLabel",
        )
        date_lbl = ttk.Label(
            mid_frame,
            text="Quote Date",
            anchor=W,
            # style="heading.TLabel",
        )
        quote_description_lbl = ttk.Label(
            mid_frame,
            text="Quote Description",
            anchor=W,
            # style="heading.TLabel",
        )
        customer_lbl = ttk.Label(
            mid_frame,
            text="Customer",
            anchor=W,
            # style="heading.TLabel",
        )
        notes_lbl = ttk.Label(
            mid_frame,
            text="Notes",
            anchor=E,
            # style="heading.TLabel",
        )
        # product_description_lbl = ttk.Label(
        #     bottom_frame,
        #     text="Product Description",
        #     anchor=E,
        #     # style="heading.TLabel",
        # )
        total_lbl = ttk.Label(
            mid_frame,
            text="Total Cost:",
            anchor=E,
            # style="heading.TLabel",
        )
        amount_lbl = ttk.Label(
            mid_frame,
            text="N$50,555.00",
            anchor=E,
            # style="heading.TLabel",
        )
        input_product_lbl = ttk.Label(
            bottom_frame,
            text="Product",
            anchor=CENTER,
            # style="heading.TLabel",
        )
        input_description_lbl = ttk.Label(
            bottom_frame,
            text="Description",
            anchor=CENTER,
            # style="heading.TLabel",
        )
        input_quantity_lbl = ttk.Label(
            bottom_frame,
            text="Quantity",
            anchor=CENTER,
            # style="heading.TLabel",
        )

        heading_lbl.grid(row=0, sticky=(N, S, W, E))
        id_lbl.grid(column=0, row=0, sticky=(W, ))
        date_lbl.grid(column=0, row=1, sticky=(W, ))
        quote_description_lbl.grid(column=0, row=2, sticky=(W, ))
        customer_lbl.grid(column=0, row=3, sticky=(W, ))
        notes_lbl.grid(column=3, row=0, sticky=(E, ))
        # product_description_lbl.grid(column=0, row=0, sticky=(W, ))
        total_lbl.grid(column=3, row=6, sticky=(N, S, W, E))
        amount_lbl.grid(column=4, row=6, sticky=(N, S, W, E))
        input_product_lbl.grid(column=0, row=0, sticky=(N, S, W, E))
        input_description_lbl.grid(column=1, row=0, sticky=(N, S, W, E))
        input_quantity_lbl.grid(column=2, row=0, sticky=(N, S, W, E))

        # Entries
        id_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        id_ent.state(["disabled"])

        date_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        quote_description_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        input_description_ent = ttk.Entry(
            bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        # Spinboxes
        input_quantity_spx = ttk.Spinbox(
            bottom_frame,
            from_=1,
            to=500000,
        )

        # Comboboxes
        customer_cbx = ttk.Combobox(
            mid_frame,
            width=38,
            values=("Abiatar", "Mumbala")
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        customer_cbx.state(["readonly"])
        input_product_cbx = ttk.Combobox(
            bottom_frame,
            width=40,
            values=("Chair", "Table")
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        # Texts
        notes_txt = Text(
            mid_frame,
            width=50, 
            height=3,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        # product_description_txt = Text(
        #     bottom_frame,
        #     width=85, 
        #     height=2,
        #     # textvariable="",
        #     # style="heading.TLabel",
        # )

        # Checkboxes
        accepted_chk = ttk.Checkbutton(
            mid_frame,
            text='Is Accepted', 
	        # command=metricChanged, 
            # variable=measureSystem,
	        onvalue='accepted', 
            offvalue='not accepted',
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        id_ent.grid(column=1, row=0, sticky=(S, N, E, W))
        date_ent.grid(column=1, row=1, sticky=(S, N, E, W))
        quote_description_ent.grid(column=1, row=2, sticky=(S, N, E, W))
        customer_cbx.grid(column=1, row=3, sticky=(S, N, E, W))
        accepted_chk.grid(column=2, row=0, sticky=(S, N, E, W))
        notes_txt.grid(column=2, columnspan=2, row=1, rowspan=3, sticky=(S, N, E, W))
        # product_description_txt.grid(column=1, row=0, sticky=(W))
        input_product_cbx.grid(column=0, row=1, rowspan=2, sticky=(S, N, E, W))
        input_description_ent.grid(column=1, row=1, rowspan=2, sticky=(S, N, E, W))
        input_quantity_spx.grid(column=2, row=1, rowspan=2, sticky=(S, N, E, W))
        
        def add_item():
            product = input_product_cbx.get(),
            description = input_description_ent.get(),
            quantity = input_quantity_spx.get()
            print(f"PRODUCT: {product[0]}")
            print(f"DESCRIPTION: {description[0]}")
            print(f"QUANTITY: {quantity}")
            if product[0] == "" or description[0] == "":
                print("INVALID ITEM")
                error_message = messagebox.showerror(
                    message='Item could not be added to the quotation!',
                    title='Invalid Item'
                )
                return error_message
            tree.insert('', 'end', values=(
                product[0],
                description[0],
                quantity
                )
            )
            input_product_cbx.set("")
            input_description_ent.delete(0,END)
            input_quantity_spx.delete(0,END)
            return

        # Buttons
        preview_btn = ttk.Button(
            mid_frame,
            text="Print/Preview Quotation",
            # style="home_btns.TButton",
            padding=(0, 10)
        )
        add_quote_btn = ttk.Button(
            mid_frame,
            text="Add a New Quotation",
            # style="home_btns.TButton",
            padding=10
        )
        save_btn = ttk.Button(
            mid_frame, 
            text="Save Quotation",
            # style="home_btns.TButton",
            padding=5
        )
        input_add_btn = ttk.Button(
            bottom_frame, 
            text="Add Item",
            # style="home_btns.TButton",
            padding=5,
            command=add_item
        )


        preview_btn.grid(column=4, row=0, rowspan=2, sticky=(N, W, E, S))
        add_quote_btn.grid(column=4, row=2, rowspan=2, sticky=(N,W, E, S))
        save_btn.grid(column=0, columnspan=3, row=6, sticky=(N, S, W, E))
        input_add_btn.grid(column=3, row=1, rowspan=2, sticky=(N, S, W, E))

        # Treeview
        tree = ttk.Treeview(mid_frame, show='headings', height=5)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
        x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
        y_scroll.grid(column=5, row=4, sticky=(N, S, W))
        x_scroll.grid(column=0, columnspan=5, row=5, sticky=(E, W))
        tree['yscrollcommand'] = y_scroll.set
        tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        tree['columns'] = (
            "Product", 
            "Description", 
            "Qty", 
            "Unit Price", 
            "Ext Price",
        )

        # Format Our Columns
        tree.column("Product", anchor=W)
        tree.column("Description", anchor=W)
        tree.column("Qty", anchor=E)
        tree.column("Unit Price", anchor=E)
        tree.column("Ext Price", anchor=E)

        # Create Headings
        tree.heading("Product", text="Product", anchor=W)
        tree.heading("Description", text="Description", anchor=W)
        tree.heading("Qty", text="Qty", anchor=E)
        tree.heading("Unit Price", text="Unit Price", anchor=E)
        tree.heading("Ext Price", text="Ext Price", anchor=E)

        # Insert the data in Treeview widget
        for i in range(1,6):
            tree.insert('', 'end', values=(
                fake.word(part_of_speech="noun"),
                fake.sentence(nb_words=3),
                random.randint(1,100),
                f"N${float(fake.pricetag()[1:].replace(',', ''))}",
                f"N${float(fake.pricetag()[1:].replace(',', ''))}"
                )
            )
        

        tree.grid(column=0, columnspan=5, row=4, sticky=(N, S, W, E))

        

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.columnconfigure(2, weight=1)
        mid_frame.columnconfigure(3, weight=1)
        mid_frame.columnconfigure(4, weight=1)
        mid_frame.columnconfigure(5, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)
        mid_frame.rowconfigure(2, weight=1)
        mid_frame.rowconfigure(3, weight=1)
        mid_frame.rowconfigure(4, weight=1)
        mid_frame.rowconfigure(5, weight=1)
        mid_frame.rowconfigure(6, weight=1)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        for child in mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=3)

    
    def setup_order_list_tab(self):
        """Configure the order list tab"""
        # Frames
        top_frame = ttk.Frame(
            self.order_list_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.order_list_frame, 
            borderwidth=5, 
            relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.order_list_frame,
            borderwidth=5, 
            relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Order List",
            anchor="center",
            style="heading.TLabel",
        )

        heading_lbl.grid(row=0)

        # Buttons
        open_order_btn = ttk.Button(
            bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21
        )
        add_order_btn = ttk.Button(
            bottom_frame, 
            text="Add New Order",
            # style="home_btns.TButton",
            padding=(10, 21)
        )
        search_order_btn = ttk.Button(
            bottom_frame, 
            text="Search Order",
            # style="home_btns.TButton",
            padding=(10, 21)
        )

        open_order_btn.grid(column=0, row=1, sticky=E)
        add_order_btn.grid(column=1, row=1, sticky=E)
        search_order_btn.grid(column=2, row=1, sticky=E)

        # Treeview
        tree = ttk.Treeview(mid_frame, show='headings', height=20)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
        x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
        y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
        x_scroll.grid(column=0, row=1, sticky=(E, W))
        tree['yscrollcommand'] = y_scroll.set
        tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        tree['columns'] = (
            "ID",
            "Customer",
            "Description",
            "Order Date",
            "Paid"
        )

        # Format Our Columns
        tree.column("ID", anchor=CENTER)
        tree.column("Customer", anchor=W)
        tree.column("Description", anchor=W)
        tree.column("Order Date", anchor=E)
        tree.column("Paid", anchor=CENTER)

        # Create Headings
        tree.heading("ID", text="ID", anchor=CENTER)
        tree.heading("Customer", text="Customer", anchor=W)
        tree.heading("Description", text="Description", anchor=W)
        tree.heading("Order Date", text="Order Date", anchor=E)
        tree.heading("Paid", text="Paid", anchor=CENTER)

        # Insert the data in Treeview widget
        for i in range(1,21):
            tree.insert('', 'end', values=(
                f"{i}",
                fake.name(),
                fake.sentence(nb_words=3),
                datetime.strptime(fake.date(), '%Y-%m-%d').date(),
                random.choice(["Yes", "No"])
                )
            )

        tree.grid(column=0, row=0, sticky=(N, S, W, E))

        

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)



    def setup_orders_tab(self):
        """configure the orders tab"""
        # Frames
        top_frame = ttk.Frame(
            self.orders_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.orders_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.orders_frame,
            borderwidth=5, 
            relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Order Details",
            anchor="center",
            style="heading.TLabel",
        )
        id_lbl = ttk.Label(
            mid_frame,
            text="Order ID",
            anchor=W,
            # style="heading.TLabel",
        )
        date_lbl = ttk.Label(
            mid_frame,
            text="Order Date",
            anchor=W,
            # style="heading.TLabel",
        )
        order_description_lbl = ttk.Label(
            mid_frame,
            text="Order Description",
            anchor=W,
            # style="heading.TLabel",
        )
        customer_lbl = ttk.Label(
            mid_frame,
            text="Customer",
            anchor=W,
            # style="heading.TLabel",
        )
        notes_lbl = ttk.Label(
            mid_frame,
            text="Notes",
            anchor=E,
            # style="heading.TLabel",
        )
        # product_description_lbl = ttk.Label(
        #     bottom_frame,
        #     text="Product Description",
        #     anchor=E,
        #     # style="heading.TLabel",
        # )
        total_lbl = ttk.Label(
            mid_frame,
            text="Total Cost:",
            anchor=E,
            # style="heading.TLabel",
        )
        amount_lbl = ttk.Label(
            mid_frame,
            text="N$50,555.00",
            anchor=E,
            # style="heading.TLabel",
        )

        heading_lbl.grid(row=0, sticky=(N, S, W, E))
        id_lbl.grid(column=0, row=0, sticky=(W, ))
        date_lbl.grid(column=0, row=1, sticky=(W, ))
        order_description_lbl.grid(column=0, row=2, sticky=(W, ))
        customer_lbl.grid(column=0, row=3, sticky=(W, ))
        notes_lbl.grid(column=3, row=0, sticky=(E, ))
        # product_description_lbl.grid(column=0, row=0, sticky=(W, ))
        total_lbl.grid(column=3, row=6, sticky=(N, S, W, E))
        amount_lbl.grid(column=4, row=6, sticky=(N, S, W, E))

        # Entries
        id_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        id_ent.state(["disabled"])

        date_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        order_description_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        # Comboboxes
        customer_cbx = ttk.Combobox(
            mid_frame,
            width=38,
            values=("Abiatar", "Mumbala")
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        customer_cbx.state(["readonly"])

        # Texts
        notes_txt = Text(
            mid_frame,
            width=50, 
            height=3,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        # product_description_txt = Text(
        #     bottom_frame,
        #     width=85, 
        #     height=2,
        #     # textvariable="",
        #     # style="heading.TLabel",
        # )

        # Checkboxes
        paid_chk = ttk.Checkbutton(
            mid_frame,
            text='Is Paid', 
	        # command=metricChanged, 
            # variable=measureSystem,
	        onvalue='paid', 
            offvalue='not paid',
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        id_ent.grid(column=1, row=0, sticky=(S, N, E, W))
        date_ent.grid(column=1, row=1, sticky=(S, N, E, W))
        order_description_ent.grid(column=1, row=2, sticky=(S, N, E, W))
        customer_cbx.grid(column=1, row=3, sticky=(S, N, E, W))
        paid_chk.grid(column=2, row=0, sticky=(S, N, E, W))
        notes_txt.grid(column=2, columnspan=2, row=1, rowspan=3, sticky=(S, N, E, W))
        # product_description_txt.grid(column=1, row=0, sticky=(W))

        # Buttons
        preview_btn = ttk.Button(
            mid_frame,
            text="Print/Preview Invoice",
            # style="home_btns.TButton",
            padding=(0, 10)
        )
        add_order_btn = ttk.Button(
            mid_frame,
            text="Add a New Order",
            # style="home_btns.TButton",
            padding=10
        )
        save_btn = ttk.Button(
            mid_frame, 
            text="Save Order",
            # style="home_btns.TButton",
            padding=5
        )


        preview_btn.grid(column=4, row=0, rowspan=2, sticky=(N, W, E, S))
        add_order_btn.grid(column=4, row=2, rowspan=2, sticky=(N,W, E, S))
        save_btn.grid(column=0, columnspan=3, row=6, sticky=(N, S, W, E))

        # Treeview
        tree = ttk.Treeview(mid_frame, show='headings', height=5)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
        x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
        y_scroll.grid(column=5, row=4, sticky=(N, S, W))
        x_scroll.grid(column=0, columnspan=5, row=5, sticky=(E, W))
        tree['yscrollcommand'] = y_scroll.set
        tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        tree['columns'] = (
            "Product", 
            "Description", 
            "Qty", 
            "Unit Price", 
            "Ext Price",
        )

        # Format Our Columns
        tree.column("Product", anchor=W)
        tree.column("Description", anchor=W)
        tree.column("Qty", anchor=E)
        tree.column("Unit Price", anchor=E)
        tree.column("Ext Price", anchor=E)

        # Create Headings
        tree.heading("Product", text="Product", anchor=W)
        tree.heading("Description", text="Description", anchor=W)
        tree.heading("Qty", text="Qty", anchor=E)
        tree.heading("Unit Price", text="Unit Price", anchor=E)
        tree.heading("Ext Price", text="Ext Price", anchor=E)

        # Insert the data in Treeview widget
        for i in range(1,6):
            tree.insert('', 'end', values=(
                fake.word(part_of_speech="noun"),
                fake.sentence(nb_words=3),
                random.randint(1,100),
                f"N${float(fake.pricetag()[1:].replace(',', ''))}",
                f"N${float(fake.pricetag()[1:].replace(',', ''))}"
                )
            )
        

        tree.grid(column=0, columnspan=5, row=4, sticky=(N, S, W, E))

        
        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.columnconfigure(2, weight=1)
        mid_frame.columnconfigure(3, weight=1)
        mid_frame.columnconfigure(4, weight=1)
        mid_frame.columnconfigure(5, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)
        mid_frame.rowconfigure(2, weight=1)
        mid_frame.rowconfigure(3, weight=1)
        mid_frame.rowconfigure(4, weight=1)
        mid_frame.rowconfigure(5, weight=1)
        mid_frame.rowconfigure(6, weight=1)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        for child in mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=3)

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

        self.quotations_frame.columnconfigure(0, weight=1)
        self.quotations_frame.columnconfigure(1, weight=1)
        self.quotations_frame.rowconfigure(0, weight=1)
        self.quotations_frame.rowconfigure(1, weight=1)
        self.quotations_frame.rowconfigure(2, weight=1)

        self.order_list_frame.columnconfigure(0, weight=1)
        self.order_list_frame.columnconfigure(1, weight=1)
        self.order_list_frame.rowconfigure(0, weight=1)
        self.order_list_frame.rowconfigure(1, weight=1)
        self.order_list_frame.rowconfigure(2, weight=1)

        self.orders_frame.columnconfigure(0, weight=1)
        self.orders_frame.columnconfigure(1, weight=1)
        self.orders_frame.rowconfigure(0, weight=1)
        self.orders_frame.rowconfigure(1, weight=1)
        self.orders_frame.rowconfigure(2, weight=1)
