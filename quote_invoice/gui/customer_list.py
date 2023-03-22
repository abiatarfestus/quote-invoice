from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from quote_invoice.db import operations as db
from quote_invoice.db.models import Customer

class CustomerListTab():
    def __init__(self, notebook, parent_frame, customer_details_tab, session):
        """Configure the customer list tab"""
        self.session = session
        self.notebook = notebook
        self.selected_customer = None
        self.customer_details_tab = customer_details_tab
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
        

    def select_record(self, event):
        print("Record selected")
        record = self.tree.focus()
        self.selected_customer = self.tree.item(record)
    
    
    
    def open_blank_customer_form(self):
        self.customer_details_tab.open_blank_customer_form()
        self.notebook.select(2)
    
    def view_customer(self):
        if not self.selected_customer:
            error_message = messagebox.showerror(
                message='No record is selected!',
                title='Error'
            )
            return error_message
        customer = db.get_customers(self.session, pk=self.selected_customer['values'][0])
        self.customer_details_tab.populate_fields(customer)
        self.notebook.select(2)

    def search_customer(self):
        search_option = self.search_option_cbx.get()
        search_value = self.search_ent.get()
        if search_option == "Customer ID":
            customer_id = search_value
            if not customer_id:
                error_message = messagebox.showerror(
                    message="Cannot search with a blank Customer ID.",
                    title='Error'
                )
                return error_message
            try:
                customer_id = int(customer_id)
                try:
                    customer = db.get_customers(self.session, pk=customer_id)
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
                customers = db.get_customers(self.session, other_fields=search_value)
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
    

    
