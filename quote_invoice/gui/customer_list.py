from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from quote_invoice.db import operations as db
from quote_invoice.gui import customer_details
from quote_invoice.db.models import Customer, Order, OrderItem, Quotation, QuotationItem, Product

class CustomerListTab():
    def __init__(self, notebook, parent_frame, session):
        """Configure the customer list tab"""
        self.session = session
        self.notebook = notebook
        #-------------------------------------TOP FRAME-----------------------------------#
        # Frames:
        self.top_frame = ttk.Frame(
            parent_frame,
            borderwidth=5, 
            relief="solid"
        )
        self.top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        # Labels:
        self.heading_lbl = ttk.Label(
            self.top_frame,
            text="Customer List",
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(column=0, row=0, sticky=(S, N, W, E))
        #-------------------------------TOP FRAME ENDS--------------------------------------#

        #-------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(
            parent_frame, 
            borderwidth=5, 
            relief="solid"
        )
        self.mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        self.mid_frame.columnconfigure(0, weight=1)
        self.mid_frame.columnconfigure(1, weight=1)
        self.mid_frame.rowconfigure(0, weight=1)
        self.mid_frame.rowconfigure(1, weight=1)
        
        # Treeviews:
        self.tree = ttk.Treeview(self.mid_frame, show='headings', height=20)
        

        # Define columns:
        self.tree["columns"] = (
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

        # Columns to display:
        self.tree["displaycolumns"] = (
            "ID",
            "Customer Name",
            "Town",
            "Phone",
            "Email",
            "Customer Since"
        )

        # Format columns:
        self.tree.column("ID", anchor=CENTER)
        self.tree.column("Customer Name", anchor=W)
        self.tree.column("Town", anchor=W)
        self.tree.column("Phone", anchor=W)
        self.tree.column("Email", anchor=W)
        self.tree.column("Customer Since", anchor=E)

        # Add headings:
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Customer Name", text="Customer Name", anchor=W)
        self.tree.heading("Town", text="Town", anchor=W)
        self.tree.heading("Phone", text="Phone", anchor=W)
        self.tree.heading("Email", text="Email", anchor=W)
        self.tree.heading("Customer Since", text="Customr Since", anchor=E)

        # Insert the data in Treeview widget
        customers = session.query(Customer).order_by(Customer.customer_id).all()
        print(f"TOTAL CUSTOMERS: {len(customers)}")
        # for i in range(1, total_customers+1):
        for customer in customers:
            if customer.first_name and customer.last_name:
                customer_name = f"{customer.last_name} {customer.first_name}"
            else:
                customer_name = customer.entity_name
            self.tree.insert('', 'end', iid=f"{customer.customer_id}",
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
        self.tree.grid(column=0, row=0, sticky=(N, S, W, E))
        self.tree.bind('<ButtonRelease-1>', self.select_record)

        # Scrollbars:
        y_scroll = ttk.Scrollbar(self.mid_frame, orient=VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(self.mid_frame, orient=HORIZONTAL, command=self.tree.xview)
        y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
        x_scroll.grid(column=0, row=1, sticky=(E, W))
        self.tree['yscrollcommand'] = y_scroll.set
        self.tree['xscrollcommand'] = x_scroll.set
        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            parent_frame,
            borderwidth=5, 
            relief="solid"
        )
        self.bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))
        
        # Entries:
        self.search_ent = ttk.Entry(
            self.bottom_frame,
        )
        self.search_ent.grid(column=3, row=1, sticky=(S, N, W, E))
        
        # Comboboxes:
        self.search_option_cbx = ttk.Combobox(
            self.bottom_frame,
            width=38,
            values=("Customer ID", "Other Variables"),
        )
        self.search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

        # Buttons:
        self.open_customer_btn = ttk.Button(
            self.bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21,
            command=self.view_customer
        )
        self.add_customer_btn = ttk.Button(
            self.bottom_frame, 
            text="Add New Customer",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=self.open_blank_customer_form
        )
        self.search_customer_btn = ttk.Button(
            self.bottom_frame, 
            text="Search Customer",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=self.search_customer
        )
        self.open_customer_btn.grid(column=0, row=1, sticky=E)
        self.add_customer_btn.grid(column=1, row=1, sticky=E)
        self.search_customer_btn.grid(column=4, row=1, sticky=E)
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#
        # self.bind_widgets_to_methods()
        self.selected_customer = None

    def select_record(self):
        print("Record selected")
        record = self.tree.focus()
        self.selected_customer = self.tree.item(record)
    
    
    
    def open_blank_customer_form(self):
        # customer_details.new_customer()
    #     id_ent.state(["!disabled"])
    #     id_ent.delete(0, END)
    #     id_ent.insert(0, "New")
    #     id_ent.state(["disabled"])
    #     type_cbx.set("")
    #     first_name_ent.delete(0, END)
    #     last_name_ent.delete(0, END)
    #     entity_ent.delete(0, END)
    #     email_ent.delete(0, END)
    #     phone_ent.delete(0, END)
    #     address_ent.delete(0, END)
    #     town_ent.delete(0, END)
    #     country_ent.delete(0, END)
    #     since_ent.delete(0, END)
    #     notes_txt.delete("1.0", END)
        self.notebook.select(self.notebook[2])
    
    def view_customer(self):
        print(f"SELECTED RECORD: {self.selected_customer}")
        customer = self.selected_customer
        if not self.selected_customer:
            error_message = messagebox.showerror(
                message='No record is selected!',
                title='Error'
            )
            return error_message
        # customer_details.populate(customer)
        # id_ent.state(["!disabled"])
        # id_ent.delete(0, END)
        # id_ent.insert(0, customer['values'][0])
        # id_ent.state(["disabled"])
        # type_cbx.set(customer['values'][1])
        # first_name_ent.delete(0, END)
        # first_name_ent.insert(0, customer['values'][2])
        # last_name_ent.delete(0, END)
        # last_name_ent.insert(0, customer['values'][3])
        # entity_ent.delete(0, END)
        # entity_ent.insert(0, customer['values'][4])
        # email_ent.delete(0, END)
        # email_ent.insert(0, customer['values'][6])
        # phone_ent.delete(0, END)
        # phone_ent.insert(0, customer['values'][7])
        # address_ent.delete(0, END)
        # address_ent.insert(0, customer['values'][8])
        # town_ent.delete(0, END)
        # town_ent.insert(0, customer['values'][9])
        # country_ent.delete(0, END)
        # country_ent.insert(0, customer['values'][10])
        # since_ent.delete(0, END)
        # since_ent.insert(0, customer['values'][11])
        # notes_txt.delete("1.0", END)
        # notes_txt.insert("1.0", customer['values'][12])
        self.notebook.select(self.notebook[2])

    def search_customer(self, session):
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
                        for item in self.tree.get_children():
                            self.tree.delete(item)
                        self.tree.insert('', 'end', iid=f"{customer.customer_id}",
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
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for customer in customers:
                    if customer.first_name and customer.last_name:
                        customer_name = f"{customer.last_name} {customer.first_name}"
                    else:
                        customer_name = customer.entity_name
                    self.tree.insert('', 'end', iid=f"{customer.customer_id}",
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

    
    # def bind_widgets_to_methods(self):
    #     self.tree.bind('<ButtonRelease-1>', self.select_record)
    #     self.open_customer_btn.configure(command=self.view_customer)
    #     self.add_customer_btn.configure(command=self.open_blank_customer_form)
    #     self.search_customer_btn = ttk.Button(command=self.search_customer)
    

    
