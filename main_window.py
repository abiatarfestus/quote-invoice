from datetime import datetime, date
import random
import db
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from faker import Faker
from moneyed import Money, NAD
from sqlalchemy import and_, or_, create_engine, select
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

        # Create a Notebook and Frames
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

        heading_lbl.grid(column=0, row=0, sticky=(S, N, W, E))

        # ENTRIES
        self.search_ent = ttk.Entry(
            bottom_frame,
        )
        self.search_ent.grid(column=3, row=1, sticky=(S, N, W, E))

        # COMBOBOXES
        
        self.search_option_cbx = ttk.Combobox(
            bottom_frame,
            width=38,
            values=("Customer ID", "Other Variables"),
        )
        self.search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

        def select_record(event):
            print("Record selected")
            record = tree.focus()
            self.selected_customer = tree.item(record)
        
        def open_blank_customer_form():
            self.id_ent.state(["!disabled"])
            self.id_ent.delete(0, END)
            self.id_ent.insert(0, "New")
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

        def search_customer():
            search_option = self.search_option_cbx.get()
            search_value = self.search_ent.get()
            if search_option == "Customer ID":
                customer_id = search_value
                if not customer_id:
                    error_message = messagebox.showerror(
                        message="Cannot search with blank Customer ID.",
                        title='Error'
                    )
                    return error_message
                try:
                    customer_id = int(customer_id)
                    try:
                        customer = db.get_customers(session, pk=customer_id)
                        if customer:
                            if customer.first_name and customer.last_name:
                                customer_name = f"{customer.last_name} {customer.first_name}"
                            else:
                                customer_name = customer.entity_name
                            for item in tree.get_children():
                                tree.delete(item)
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
                        else:
                            info_message = messagebox.showinfo(
                            message="No matching record was found.",
                            title='Info'
                        )
                            return info_message
                    except Exception as e:
                            error_message = messagebox.showerror(
                            message="Oops! Something went wrong.",
                            detail=e,
                            title='Error'
                        )
                            return error_message
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Invalid Customer ID.",
                    detail=e,
                    title='Error'
                )
                    return error_message
            else:
                try:
                    customers = db.get_customers(session, other_fields=search_value)
                    if not customers:
                        info_message = messagebox.showinfo(
                            message="No matching record was found.",
                            title='Info'
                            )
                        return info_message
                    for item in tree.get_children():
                        tree.delete(item)
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
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Oops! Something went wrong.",
                    detail=e,
                    title='Error'
                )
                    return error_message

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
            command=open_blank_customer_form
        )
        search_customer_btn = ttk.Button(
            bottom_frame, 
            text="Search Customer",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=search_customer
        )


        open_customer_btn.grid(column=0, row=1, sticky=E)
        add_customer_btn.grid(column=1, row=1, sticky=E)
        search_customer_btn.grid(column=4, row=1, sticky=E)

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

        # Create Headings
        tree.heading("ID", text="ID", anchor=CENTER)
        tree.heading("Customer Name", text="Customer Name", anchor=W)
        tree.heading("Town", text="Town", anchor=W)
        tree.heading("Phone", text="Phone", anchor=W)
        tree.heading("Email", text="Email", anchor=W)
        tree.heading("Customer Since", text="Customr Since", anchor=E)

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

        def open_blank_customer_form():
            self.id_ent.state(["!disabled"])
            self.id_ent.delete(0, END)
            self.id_ent.insert(0, "New")
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
            # Update the Save/Update button
            # self.notebook.select(self.customer_frame)

        def create_or_update_customer():
            customer_id = self.id_ent.get()
            if customer_id == "New":
                try:
                    db.add_customer(
                    session, 
                    customer_type=self.type_cbx.get(),
                    first_name=self.first_name_ent.get(), 
                    last_name=self.last_name_ent.get(), 
                    entity_name=self.entity_ent.get(), 
                    email=self.email_ent.get(), 
                    phone=self.phone_ent.get(), 
                    address=self.address_ent.get(), 
                    town=self.town_ent.get(), 
                    country=self.country_ent.get(),
                    customer_since=datetime.strptime(self.since_ent.get(), '%Y-%m-%d').date(),
                    notes=self.notes_txt.get("1.0", END)
                )
                    open_blank_customer_form()
                    success_message = messagebox.showinfo(
                    message='Customer was successfully created!',
                    title='Success'
                )
                    return success_message
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Oops! Something went wrong.",
                    detail=e,
                    title='Error'
                )
                    return error_message
            else:
                try:
                    customer = db.get_customers(session, customer_id)
                    customer.customer_type = self.type_cbx.get()
                    customer.first_name = self.first_name_ent.get()
                    customer.last_name = self.last_name_ent.get()
                    customer.entity_name = self.entity_ent.get()
                    customer.email = self.email_ent.get()
                    customer.phone = self.phone_ent.get()
                    customer.address = self.address_ent.get()
                    customer.town = self.town_ent.get()
                    customer.country = self.country_ent.get()
                    customer.customer_since = datetime.strptime(self.since_ent.get(), '%Y-%m-%d').date()
                    customer.notes = self.notes_txt.get("1.0", END)
                    session.commit()
                    success_message = messagebox.showinfo(
                    message='Record was successfully updated!',
                    title='Success'
                )
                    return success_message
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Oops! Something went wrong.",
                    detail=e,
                    title='Error'
                )
                    return error_message 

        # Buttons
        save_btn = ttk.Button(
            mid_frame,
            text="Save Record",
            # style="home_btns.TButton",
            padding=5,
            command=create_or_update_customer
        )
        new_customer_btn = ttk.Button(
            mid_frame,
            text="New Customer",
            # style="home_btns.TButton",
            padding=5,
            command=open_blank_customer_form
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

        save_btn.grid(column=0, columnspan=5, row=12, sticky=(E, W))
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
        mid_frame.rowconfigure(12, weight=1)

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

        # ENTRIES
        self.quote_search_ent = ttk.Entry(
            bottom_frame,
        )
        self.quote_search_ent.grid(column=3, row=1, sticky=(S, N, W, E))

        # COMBOBOXES
        
        self.quote_search_option_cbx = ttk.Combobox(
            bottom_frame,
            width=38,
            values=("Quote ID", "Customer ID", "Other Variables"),
        )
        self.quote_search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

        def select_record(event):
            # print("Record selected")
            record = tree.focus()
            self.selected_quotation = tree.item(record)
        
        def open_blank_quote_form():
            self.quote_id_ent.state(["!disabled"])
            self.quote_id_ent.delete(0, END)
            self.quote_id_ent.insert(0, "New")
            self.quote_id_ent.state(["disabled"])
            self.quote_customer_cbx.state(["!disabled"])
            self.quote_customer_cbx.set("")
            self.quote_description_ent.state(["!disabled"])
            self.quote_description_ent.delete(0, END)
            self.quote_date_ent.state(["!disabled"])
            self.quote_date_ent.delete(0, END)
            self.quote_date_ent.insert(0, date.today().strftime('%Y/%m/%d'))
            self.quote_accepted_chk.state(["!disabled"])
            self.is_accepted.set(value="False")
            # self.quote_accepted_chk.invoke()
            self.quote_notes_txt.delete("1.0", END)
            self.quote_input_product_cbx.state(["!disabled"])
            self.quote_input_description_ent.state(["!disabled"])
            self.quote_input_quantity_spx.state(["!disabled"])
            self.quote_input_add_btn.state(["!disabled"])
            self.quote_save_update_btn.state(["!disabled"])
            self.change_to_order_btn.state(["!disabled"])
            self.mark_closed_btn.state(["!disabled"])
            for item in self.quote_items_tree.get_children():
                self.quote_items_tree.delete(item)
            self.quote_amount.set("Total Cost:\tN$0.00")
            self.quote_save_update.set("Save Quotation")
            self.notebook.select(self.quotation_frame)
        
        def view_quotation():
            # print(f"SELECTED RECORD: {self.selected_quotation}")
            quotation = self.selected_quotation
            if not self.selected_quotation:
                error_message = messagebox.showerror(
                    message='No record is selected!',
                    title='Error'
                )
                return error_message
            # Get quote items from datatbase
            quote_id = quotation['values'][0]
            quote_amount = Money("0.00", NAD)
            quote_items = session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == quotation['values'][0]).all()
            # print(quote_items)
            # print(f"QUOTE ITEMS\n Product\tDescription\tQuantity\tUnit Price\tTotal. Price")
            # for product,item in quote_items:
            #     print(f""" {product.product_name}\t{product.description[:10]}\tx{item.quantity}\t@{product.price}\t={item.quantity*product.price}""")
            
            self.quote_id_ent.state(["!disabled"])
            self.quote_id_ent.delete(0, END)
            self.quote_id_ent.insert(0, quote_id)
            self.quote_id_ent.state(["disabled"])
            self.quote_customer_cbx.state(["!disabled"])
            self.quote_customer_cbx.delete(0, END)
            self.quote_customer_cbx.set(quotation['values'][1])
            self.quote_customer_cbx.state(["disabled"])
            self.quote_description_ent.state(["!disabled"])
            self.quote_description_ent.delete(0, END)
            self.quote_description_ent.insert(0, quotation['values'][2])
            self.quote_date_ent.state(["!disabled"])
            self.quote_date_ent.delete(0, END)
            self.quote_date_ent.insert(0, quotation['values'][3].replace("-", "/"))
            self.quote_accepted_chk.state(["disabled"])
            self.is_accepted.set(value=quotation['values'][4])
            # print(f"CHECK VALUE: {self.is_accepted.get()}")
            self.quote_notes_txt.delete("1.0", END)
            self.quote_notes_txt.insert("1.0", quotation['values'][6])
            self.quote_input_product_cbx.state(["!disabled"])
            self.quote_input_description_ent.state(["!disabled"])
            self.quote_input_quantity_spx.state(["!disabled"])
            self.quote_input_add_btn.state(["!disabled"])
            if self.is_accepted.get() or quotation['values'][5] == "True":
                self.quote_customer_cbx.state(["disabled"])
                self.quote_description_ent.state(["disabled"])
                self.quote_date_ent.state(["disabled"])
                self.quote_accepted_chk.state(["!disabled"])
                self.quote_accepted_chk.invoke()
                self.quote_accepted_chk.state(["disabled"])
                self.quote_input_product_cbx.state(["disabled"])
                self.quote_input_description_ent.state(["disabled"])
                self.quote_input_quantity_spx.state(["disabled"])
                self.quote_input_add_btn.state(["disabled"])
                self.quote_save_update_btn.state(["disabled"])
                self.change_to_order_btn.state(["disabled"])
                self.mark_closed_btn.state(["disabled"])
            
            # Update item list
            for item in self.quote_items_tree.get_children():
                self.quote_items_tree.delete(item)
            for product,item in quote_items:
                unit_price = Money(product.price, NAD)
                total_price = unit_price*item.quantity
                self.quote_items_tree.insert('', 'end', iid=f"{product.product_id}",
                    values=(
                        product.product_id,
                        item.quote_item_id,
                        product.product_name,
                        item.description,
                        item.quantity,
                        unit_price.amount,
                        total_price.amount
                        )
                    )
                quote_amount += total_price
            self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")
            self.quote_save_update.set("Update Quotation")
            self.notebook.select(self.quotation_frame)

        def search_quotation():
            search_option = self.quote_search_option_cbx.get()
            search_value = self.quote_search_ent.get()
            if search_option == "Quote ID":
                quote_id = search_value
                if not quote_id:
                    error_message = messagebox.showerror(
                        message="Cannot search a with blank Quote ID.",
                        title='Error'
                    )
                    return error_message
                try:
                    quote_id = int(quote_id)
                    try:
                        quotation = db.get_quotations(session, pk=quote_id)
                        if quotation:
                            for item in tree.get_children():
                                tree.delete(item)
                            tree.insert('', 'end', iid=f"{quotation.quote_id}",
                            values=(
                                f"{quotation.quote_id}",
                                customer_id_name_dict[quotation.customer_id],
                                quotation.description,
                                quotation.quote_date,
                                quotation.is_accepted,
                                quotation.is_closed,
                                quotation.notes
                                )
                            )
                        else:
                            info_message = messagebox.showinfo(
                            message="No matching record was found.",
                            title='Info'
                        )
                            return info_message
                    except Exception as e:
                            error_message = messagebox.showerror(
                            message="Oops! Something went wrong.",
                            detail=e,
                            title='Error'
                        )
                            return error_message
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Invalid Quote ID.",
                    detail=e,
                    title='Error'
                )
                    return error_message
            elif search_option == "Customer ID":
                customer_id = search_value
                if not customer_id:
                    error_message = messagebox.showerror(
                        message="Cannot search a with blank Customer ID.",
                        title='Error'
                    )
                    return error_message
                try:
                    customer_id = int(customer_id)
                    try:
                        quotations = db.get_quotations(session, customer_id=customer_id)
                        if quotations:
                            for item in tree.get_children():
                                tree.delete(item)
                            for quote in quotations:
                                tree.insert('', 'end', iid=f"{quote.quote_id}",
                                values=(
                                    f"{quote.quote_id}",
                                    customer_id_name_dict[quote.customer_id],
                                    quote.description,
                                    quote.quote_date,
                                    quote.is_accepted,
                                    quote.is_closed,
                                    quote.notes
                                    )
                                )
                        else:
                            info_message = messagebox.showinfo(
                            message="No matching record was found.",
                            title='Info'
                        )
                            return info_message
                    except Exception as e:
                            error_message = messagebox.showerror(
                            message="Oops! Something went wrong.",
                            detail=e,
                            title='Error'
                        )
                            return error_message
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Invalid Quote ID.",
                    detail=e,
                    title='Error'
                )
                    return error_message
            else:
                try:
                    quotations = db.get_quotations(session, other_fields=search_value)
                    if not quotations:
                        info_message = messagebox.showinfo(
                            message="No matching record was found.",
                            title='Info'
                            )
                        return info_message
                    for item in tree.get_children():
                        tree.delete(item)
                    for quote in quotations:
                        tree.insert('', 'end', iid=f"{quote.quote_id}",
                        values=(
                            f"{quote.quote_id}",
                            customer_id_name_dict[quote.customer_id],
                            quote.description,
                            quote.quote_date,
                            quote.is_accepted,
                            quote.is_closed,
                            quote.notes
                            )
                        )
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Oops! Something went wrong.",
                    detail=e,
                    title='Error'
                )
                    return error_message




        # Buttons
        open_quotation_btn = ttk.Button(
            bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21,
            command=view_quotation
        )
        add_quotation_btn = ttk.Button(
            bottom_frame, 
            text="Add New Quotation",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=open_blank_quote_form
        )
        search_quotation_btn = ttk.Button(
            bottom_frame, 
            text="Search Quotation",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=search_quotation
        )

        open_quotation_btn.grid(column=0, row=1, sticky=E)
        add_quotation_btn.grid(column=1, row=1, sticky=E)
        search_quotation_btn.grid(column=4, row=1, sticky=E)

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
        tree['columns'] = (
            "ID",
            "Customer",
            "Description",
            "Quote Date",
            "Accepted", 
            "Closed",
            "Notes"
        )

        tree['displaycolumns'] = (
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
        tree.column("Notes", anchor=W)

        # Create Headings
        tree.heading("ID", text="ID", anchor=CENTER)
        tree.heading("Customer", text="Customer", anchor=W)
        tree.heading("Description", text="Description", anchor=W)
        tree.heading("Quote Date", text="Quote Date", anchor=E)
        tree.heading("Accepted", text="Accepted", anchor=CENTER)
        tree.heading("Closed", text="Closed", anchor=CENTER)
        tree.heading("Notes", text="Notes", anchor=W)

        customers = session.query(Customer).all()
        self.customers_dict = dict()
        for customer in customers:
            if customer.customer_type == "Person":
                key = f"{customer.last_name} {customer.first_name} >> {customer.phone}"
            else:
                key = f"{customer.entity_name} >> {customer.phone}"
            self.customers_dict.update({
                key:[
                    customer.customer_id,
                    customer.customer_type,
                    customer.first_name,
                    customer.last_name,
                    customer.entity_name,
                    customer.email,
                    customer.phone
                    ]
                }
            )
        # print(f"CUSTOMERS: {customers_dict}")
        # Create a dict of customer_id:customer_name for use in update customer
        customer_id_name_dict = dict()
        for name in tuple(self.customers_dict):
            customer_id_name_dict.update({self.customers_dict[name][0]:name })
        # print(f"CUSTOMER_ID_NAME DICT: {customer_id_name_dict}")

        quotations = session.query(Quotation).order_by(Quotation.quote_date).all()
        # print(f"TOTAL QUOTATIONS: {len(quotations)}")
        for quote in quotations:
            tree.insert('', 'end', iid=f"{quote.quote_id}",
            values=(
                f"{quote.quote_id}",
                customer_id_name_dict[quote.customer_id],
                quote.description,
                quote.quote_date,
                quote.is_accepted,
                quote.is_closed,
                quote.notes
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

    def setup_quotation_tab(self):
        """Configure the quotations tab"""
        # Frames
        top_frame = ttk.Frame(
            self.quotation_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.quotation_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.quotation_frame,
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
        # total_lbl = ttk.Label(
        #     mid_frame,
        #     text="Total Cost:",
        #     anchor=E,
        #     # style="heading.TLabel",
        # )
        self.quote_amount = StringVar(value="Total Cost:\tN$0.00")
        amount_lbl = ttk.Label(
            mid_frame,
            textvariable=self.quote_amount,
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
        # total_lbl.grid(column=3, row=6, sticky=(N, S, W, E))
        amount_lbl.grid(column=4, row=6, sticky=(N, S, W, E))
        input_product_lbl.grid(column=0, row=0, sticky=(N, S, W, E))
        input_description_lbl.grid(column=1, row=0, sticky=(N, S, W, E))
        input_quantity_lbl.grid(column=2, row=0, sticky=(N, S, W, E))

        # Entries
        self.quote_id_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_id_ent.insert(0, "New")
        self.quote_id_ent.state(["disabled"])

        self.quote_date_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_date_ent.insert(0, date.today().strftime('%Y/%m/%d'))

        self.quote_description_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_input_description_ent = ttk.Entry(
            bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        # Spinboxes
        self.quote_input_quantity_spx = ttk.Spinbox(
            bottom_frame,
            from_=1,
            to=500000,
        )

        # Comboboxes

        self.quote_customer_cbx = ttk.Combobox(
            mid_frame,
            width=38,
            values=sorted(tuple(self.customers_dict))
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_customer_cbx.state(["readonly"])
        products = session.query(Product).all()
        products_dict = {
            product.product_name:[
                product.product_id,
                product.product_name,
                product.description,
                product.price,
                product.quantity,
                product.sku,
                product.barcode
                ] for product in products
            }

        # product_ids as keys
        products_dict2 = {
            product.product_id:product.product_name for product in products
            }
        # print(f"PRODUCTS: {products_dict}")
        self.quote_input_product_cbx = ttk.Combobox(
            bottom_frame,
            width=40,
            values=sorted(tuple(products_dict))
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        # Texts
        self.quote_notes_txt = Text(
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
        self.is_accepted =  BooleanVar()
        self.quote_accepted_chk = ttk.Checkbutton(
            mid_frame,
            text='Is Accepted',
            variable=self.is_accepted,
            onvalue="True",
            offvalue="False",
            state="disabled"
        )

        self.quote_id_ent.grid(column=1, row=0, sticky=(S, N, E, W))
        self.quote_date_ent.grid(column=1, row=1, sticky=(S, N, E, W))
        self.quote_description_ent.grid(column=1, row=2, sticky=(S, N, E, W))
        self.quote_customer_cbx.grid(column=1, row=3, sticky=(S, N, E, W))
        self.quote_accepted_chk.grid(column=2, row=0, sticky=(S, N, E, W))
        self.quote_notes_txt.grid(column=2, columnspan=2, row=1, rowspan=3, sticky=(S, N, E, W))
        # product_description_txt.grid(column=1, row=0, sticky=(W))
        self.quote_input_product_cbx.grid(column=0, row=1, rowspan=2, sticky=(S, N, E, W))
        self.quote_input_description_ent.grid(column=1, row=1, rowspan=2, sticky=(S, N, E, W))
        self.quote_input_quantity_spx.grid(column=2, row=1, rowspan=2, sticky=(S, N, E, W))
        
        def select_record(event):
            # print("Record selected")
            # print(f"ITEM EXISTS: {self.quote_items_tree.exists('11')}")
            record = self.quote_items_tree.focus()
            selected_item = self.quote_items_tree.item(record)
            # print(f"SELECTED ITEM: {selected_item}")
            self.quote_input_product_cbx.state(["!disabled"])
            # self.quote_input_product_cbx.delete(0, END)
            self.quote_input_product_cbx.set(f"{products_dict2[selected_item['values'][0]]}")
            self.quote_input_description_ent.state(["!disabled"])
            self.quote_input_description_ent.delete(0, END)
            self.quote_input_description_ent.insert(0, f"{selected_item['values'][3]}")
            self.quote_input_quantity_spx.state(["!disabled"])
            self.quote_input_quantity_spx.set(f"{selected_item['values'][4]}")


        def add_item():
            product = self.quote_input_product_cbx.get()
            description = self.quote_input_description_ent.get()
            quantity = self.quote_input_quantity_spx.get()
            # print(f"PRODUCT: {product}")
            # print(f"PRODUCT ID: {products_dict[product][0]}")
            # print(f"DESCRIPTION: {description}")
            # print(f"QUANTITY: {quantity}")
            if product == "" or quantity == "":
                print("INVALID ITEM")
                error_message = messagebox.showerror(
                    message='Cannot add an item without a product or quantity!',
                    title='Invalid Item'
                )
                return error_message
            product_id = str(products_dict[product][0])
            unit_price = Money(str(products_dict[product][3]), NAD)
            total_price = unit_price*int(quantity)
            if self.quote_items_tree.exists(product_id):
                selected_item = self.quote_items_tree.set(product_id, column="Total Price")
                selected_item_total_price = Money(selected_item, NAD)
                # print(f"SELECTED ITEM TOTAL PRICE: {selected_item_total_price}")
                quote_amount = Money(self.quote_amount.get()[14:], NAD)
                quote_amount = quote_amount-selected_item_total_price
                self.quote_items_tree.set(product_id, column="Description", value=description)
                self.quote_items_tree.set(product_id, column="Quantity", value=quantity)
                self.quote_items_tree.set(product_id, column="Unit Price", value=str(unit_price.amount))
                self.quote_items_tree.set(product_id, column="Total Price", value=str(total_price.amount))
                quote_amount += total_price
            else:
                self.quote_items_tree.insert('', 'end', iid=f"{product_id}",
                values=(
                    product_id,  
                    "", # this is replaced with quote_item_id when data is pulled from the db
                    product,
                    description,
                    quantity,
                    str(unit_price.amount),
                    str(total_price.amount)
                    )
            )
                # print(f"SLICED QUOTE_AMOUNT: {self.quote_amount.get()[14:]}")
                quote_amount = Money(self.quote_amount.get()[14:], NAD)
                quote_amount += total_price
            # print(f"MONEY: {quote_amount.amount}")
            self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")
            self.quote_input_product_cbx.set("")
            self.quote_input_description_ent.delete(0,END)
            self.quote_input_quantity_spx.delete(0,END)
            return

        def open_blank_quote_form():
            self.quote_id_ent.state(["!disabled"])
            self.quote_id_ent.delete(0, END)
            self.quote_id_ent.insert(0, "New")
            self.quote_id_ent.state(["disabled"])
            self.quote_customer_cbx.state(["!disabled"])
            self.quote_customer_cbx.set("")
            self.quote_description_ent.state(["!disabled"])
            self.quote_description_ent.delete(0, END)
            self.quote_date_ent.state(["!disabled"])
            self.quote_date_ent.delete(0, END)
            self.quote_date_ent.insert(0, date.today().strftime('%Y/%m/%d'))
            self.quote_accepted_chk.state(["!disabled"])
            self.is_accepted.set(value="False")
            # self.quote_accepted_chk.invoke()
            self.quote_accepted_chk.state(["disabled"])
            self.quote_notes_txt.delete("1.0", END)
            self.quote_input_product_cbx.state(["!disabled"])
            self.quote_input_product_cbx.delete(0, END)
            self.quote_input_description_ent.state(["!disabled"])
            self.quote_input_description_ent.delete(0, END)
            self.quote_input_quantity_spx.state(["!disabled"])
            self.quote_input_quantity_spx.set("")
            self.quote_input_add_btn.state(["!disabled"])
            self.quote_save_update_btn.state(["!disabled"])
            self.change_to_order_btn.state(["!disabled"])
            self.mark_closed_btn.state(["!disabled"])
            # print(f"ITEMS: {self.quote_items_tree.get_children()}")
            # items = []
            for item in self.quote_items_tree.get_children():
                # items.append(self.quote_items_tree.item(item))
                self.quote_items_tree.delete(item)
            # print(f"ITEMS: {items}")
            self.quote_amount.set("Total Cost:\tN$0.00")
            self.quote_save_update.set("Save Quotation")
            self.notebook.select(self.quotation_frame)

        
        def create_quotation():
            try:
                customer_id = self.customers_dict[self.quote_customer_cbx.get()][0]
            except Exception as e:
                error_message = messagebox.showerror(
                message="Invalid customer entered.",
                detail=e,
                title='Error'
            )
                return error_message
            
            try:
                quote_date=datetime.strptime(self.quote_date_ent.get(), '%Y/%m/%d').date()
                new_quote_id = db.add_quotation(
                    session, 
                    quote_date=quote_date,
                    description=self.quote_description_ent.get(),
                    customer_id=customer_id,
                    is_accepted=self.is_accepted.get(),
                    notes=self.quote_notes_txt.get("1.0", END)
                )
                
                if self.quote_items_tree.get_children(): # If there are items on the list
                    try:
                        items = []
                        for item in self.quote_items_tree.get_children():
                            items.append(self.quote_items_tree.item(item))
                        for item in items:
                            db.add_quotation_item(
                                session,
                                quote_id=new_quote_id,
                                product_id=item["values"][0],
                                quantity=item["values"][4],
                                description=item["values"][3]
                            )
                        success_message = messagebox.showinfo(
                            message='Quotation was successfully created!',
                            title='Success'
                        )
                        return success_message
                    except Exception as e:
                        error_message = messagebox.showerror(
                        message="Oops! Something went wrong. Some items could not be added to the Quotation.",
                        detail=e,
                        title='Error'
                    )
                        return error_message
                    finally:
                        quote_items = session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == new_quote_id).all()
                        self.quote_id_ent.state(["!disabled"])
                        self.quote_id_ent.delete(0, END)
                        self.quote_id_ent.insert(0, new_quote_id)
                        self.quote_id_ent.state(["disabled"])
                        
                        # Update item list
                        quote_amount = Money("0.00", NAD)
                        for item in self.quote_items_tree.get_children():
                            self.quote_items_tree.delete(item)
                        for product,item in quote_items:
                            unit_price = Money(product.price, NAD)
                            total_price = unit_price*item.quantity
                            self.quote_items_tree.insert('', 'end', iid=f"{product.product_id}",
                                values=(
                                    product.product_id,
                                    item.quote_item_id,
                                    product.product_name,
                                    item.description,
                                    item.quantity,
                                    unit_price.amount,
                                    total_price.amount
                                    )
                                )
                            quote_amount += total_price
                        self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")
                        self.quote_save_update.set("Update Quotation")
                        self.notebook.select(self.quotation_frame)
            except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! Something went wrong. Quotation could not be created.",
                detail=e,
                title='Error'
            )
                return error_message
        
        def update_quotation():
            quote_id = self.quote_id_ent.get()
            try:
                quotation = db.get_quotations(session, quote_id)
                quote_date=datetime.strptime(self.quote_date_ent.get(), '%Y/%m/%d').date()
                try:
                    customer_id = self.customers_dict[self.quote_customer_cbx.get()][0]
                except Exception as e:
                    error_message = messagebox.showerror(
                    message="Invalid customer entered.",
                    detail=e,
                    title='Error'
                )
                    return error_message

                quotation.quote_date = quote_date
                quotation.description = self.quote_description_ent.get()
                quotation.customer_id = customer_id
                quotation.is_accepted = self.is_accepted.get()
                quotation.notes = self.quote_notes_txt.get("1.0", END)
                session.commit()
                if self.quote_items_tree.get_children(): # If there are items on the list
                    try:
                        items = []
                        for item in self.quote_items_tree.get_children():
                            items.append(self.quote_items_tree.item(item))
                        for item in items:
                            if not item["values"][1]: # If it's new item (has no id)
                                db.add_quotation_item(
                                    session,
                                    quote_id=quote_id,
                                    product_id=item["values"][0],
                                    quantity=item["values"][4],
                                    description=item["values"][3]
                                )
                            else:
                                existing_item = session.query(QuotationItem).get(item["values"][1])
                                existing_item.product_id=item["values"][0]
                                existing_item.quantity=item["values"][4]
                                existing_item.description=item["values"][3]
                                session.commit()
                        success_message = messagebox.showinfo(
                            message='Quotation was successfully updated!',
                            title='Success'
                        )
                        return success_message
                    except Exception as e:
                        error_message = messagebox.showerror(
                        message="Oops! Something went wrong. Some items could not be updated.",
                        detail=e,
                        title='Error'
                    )
                        return error_message
                    finally:
                        quote_items = session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == quote_id).all()                            
                        # Update item list
                        quote_amount = Money("0.00", NAD)
                        for item in self.quote_items_tree.get_children():
                            self.quote_items_tree.delete(item)
                        
                        for product,item in quote_items:
                            unit_price = Money(product.price, NAD)
                            total_price = unit_price*item.quantity
                            self.quote_items_tree.insert('', 'end', iid=f"{product.product_id}",
                                values=(
                                    product.product_id,
                                    item.quote_item_id,
                                    product.product_name,
                                    item.description,
                                    item.quantity,
                                    unit_price.amount,
                                    total_price.amount
                                    )
                                )
                            quote_amount += total_price
                        self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")
                        self.quote_save_update.set("Update Quotation")
                        self.notebook.select(self.quotation_frame)
                        return
                success_message = messagebox.showinfo(
                message='Record was successfully updated!',
                title='Success'
            )
                return success_message
            except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! Something went wrong.",
                detail=e,
                title='Error'
            )
                return error_message 
        
        
        def create_or_update_quotation():
            quote_id = self.quote_id_ent.get()
            if quote_id == "New":
                create_quotation()
            else:
                update_quotation()


        # Buttons
        quote_preview_btn = ttk.Button(
            mid_frame,
            text="Print/Preview Quotation",
            # style="home_btns.TButton",
            padding=(0, 10)
        )
        add_quote_btn = ttk.Button(
            mid_frame,
            text="Add a New Quotation",
            # style="home_btns.TButton",
            padding=10,
            command=open_blank_quote_form
        )
        self.quote_save_update = StringVar(value="Save Quotation")
        self.quote_save_update_btn = ttk.Button(
            mid_frame, 
            textvariable=self.quote_save_update,
            # style="home_btns.TButton",
            padding=5,
            command=create_or_update_quotation
        )
        self.change_to_order_btn = ttk.Button(
            mid_frame,
            text="Change to Order",
            # style="home_btns.TButton",
            padding=10,
            # command=change_quote_to_order
        )
        self.mark_closed_btn = ttk.Button(
            mid_frame,
            text="Mark as Closed",
            # style="home_btns.TButton",
            padding=10,
            # command=self.mark_quote_closed
        )
        self.reuse_quote_btn = ttk.Button(
            mid_frame,
            text="Reuse Quotation",
            # style="home_btns.TButton",
            padding=10,
            # command=reuse_quotation
        )
        self.quote_input_add_btn = ttk.Button(
            bottom_frame, 
            text="Add Item",
            # style="home_btns.TButton",
            padding=5,
            command=add_item
        )


        quote_preview_btn.grid(column=4, row=0, rowspan=2, sticky=(N, W, E, S))
        add_quote_btn.grid(column=4, row=2, rowspan=2, sticky=(N,W, E, S))
        self.quote_save_update_btn.grid(column=0, row=6, sticky=(N, S, W, E))
        self.change_to_order_btn.grid(column=1, row=6, sticky=(N, S, W, E))
        self.mark_closed_btn.grid(column=2, row=6, sticky=(N, S, W, E))
        self.reuse_quote_btn.grid(column=3, row=6, sticky=(N, S, W, E))
        self.quote_input_add_btn.grid(column=3, row=1, rowspan=2, sticky=(N, S, W, E))

        # Treeview
        self.quote_items_tree = ttk.Treeview(mid_frame, show='headings', height=5)
        self.quote_items_tree.bind('<ButtonRelease-1>', select_record)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=self.quote_items_tree.yview)
        x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=self.quote_items_tree.xview)
        y_scroll.grid(column=5, row=4, sticky=(N, S, W))
        x_scroll.grid(column=0, columnspan=5, row=5, sticky=(E, W))
        self.quote_items_tree['yscrollcommand'] = y_scroll.set
        self.quote_items_tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        self.quote_items_tree['columns'] = (
            "ID", # product_id
            "Quote_Item_ID",
            "Item", 
            "Description", # Item description/note, not necessarily product description
            "Quantity", 
            "Unit Price", 
            "Total Price",
        )

        self.quote_items_tree['displaycolumns'] = (
            "Item", 
            "Description", 
            "Quantity", 
            "Unit Price", 
            "Total Price",
        )

        # Format Our Columns
        self.quote_items_tree.column("ID", anchor=CENTER)
        self.quote_items_tree.column("Quote_Item_ID", anchor=CENTER)
        self.quote_items_tree.column("Item", anchor=W)
        self.quote_items_tree.column("Description", anchor=W)
        self.quote_items_tree.column("Quantity", anchor=E)
        self.quote_items_tree.column("Unit Price", anchor=E)
        self.quote_items_tree.column("Total Price", anchor=E)

        # Create Headings
        self.quote_items_tree.heading("Item", text="Item", anchor=W)
        self.quote_items_tree.heading("Description", text="Description", anchor=W)
        self.quote_items_tree.heading("Quantity", text="Quantity", anchor=E)
        self.quote_items_tree.heading("Unit Price", text="Unit Price", anchor=E)
        self.quote_items_tree.heading("Total Price", text="Total Price", anchor=E)

        # Insert the data in Treeview widget
        # for i in range(1,6):
        #     self.quote_items_tree.insert('', 'end', values=(
        #         fake.word(part_of_speech="noun"),
        #         fake.sentence(nb_words=3),
        #         random.randint(1,100),
        #         f"N${float(fake.pricetag()[1:].replace(',', ''))}",
        #         f"N${float(fake.pricetag()[1:].replace(',', ''))}"
        #         )
        #     )
        

        self.quote_items_tree.grid(column=0, columnspan=5, row=4, sticky=(N, S, W, E))

        

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



    def setup_order_tab(self):
        """configure the orders tab"""
        # Frames
        top_frame = ttk.Frame(
            self.order_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.order_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.order_frame,
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
            "Total Price",
        )

        # Format Our Columns
        tree.column("Product", anchor=W)
        tree.column("Description", anchor=W)
        tree.column("Qty", anchor=E)
        tree.column("Unit Price", anchor=E)
        tree.column("Total Price", anchor=E)

        # Create Headings
        tree.heading("Product", text="Product", anchor=W)
        tree.heading("Description", text="Description", anchor=W)
        tree.heading("Qty", text="Qty", anchor=E)
        tree.heading("Unit Price", text="Unit Price", anchor=E)
        tree.heading("Total Price", text="Total Price", anchor=E)

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
