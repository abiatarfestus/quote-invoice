from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from quote_invoice.db import operations as db
from quote_invoice.db.models import Customer, Order


class OrderListTab():
    def __init__(self, notebook, parent_frame, order_details_tab, session):
        self.notebook = notebook
        self.session = session
        self.selected_order = None
        self.order_details_tab = order_details_tab
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
            text="Order List",
            anchor="center",
            style="heading.TLabel",
        )

        self.heading_lbl.grid(row=0)
        #-------------------------------TOP FRAME ENDS--------------------------------------#

        #-------------------------------MID FRAME-------------------------------------------#
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
        self.tree.bind('<ButtonRelease-1>', self.select_record)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(self.mid_frame, orient=VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(self.mid_frame, orient=HORIZONTAL, command=self.tree.xview)
        y_scroll.grid(column=1, row=0, sticky=(N,S, W))
        x_scroll.grid(column=0, row=1, sticky=(N, E, W))
        self.tree['yscrollcommand'] = y_scroll.set
        self.tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        self.tree['columns'] = (
            "ID",
            "Customer",
            "Description",
            "Order Date",
            "Paid",
            "Notes"
        )

        self.tree['displaycolumns'] = (
            "ID",
            "Customer",
            "Description",
            "Order Date",
            "Paid"
        )

        # Format Our Columns
        self.tree.column("ID",  width=100, anchor=CENTER)
        self.tree.column("Customer",  width=250, anchor=W)
        self.tree.column("Description", width=600, anchor=W)
        self.tree.column("Order Date",  width=100, anchor=E)
        self.tree.column("Paid", anchor=CENTER)
        # self.tree.column("Notes", anchor=W)

        # Create Headings
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Customer", text="Customer", anchor=W)
        self.tree.heading("Description", text="Description", anchor=W)
        self.tree.heading("Order Date", text="Order Date", anchor=E)
        self.tree.heading("Paid", text="Paid", anchor=CENTER)
        # self.tree.heading("Notes", text="Notes", anchor=W)

        self.orders = self.session.query(Order).order_by(Order.order_date).all()
        self.list_orders(self.orders)
        self.tree.grid(column=0, row=0, sticky=(N, S, W, E))
        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            parent_frame,
            borderwidth=5, 
            relief="solid"
        )
        self.bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # Entries
        self.order_search_ent = ttk.Entry(
            self.bottom_frame,
        )
        self.order_search_ent.grid(column=3, row=1, sticky=(S, N, W, E))

        # Comboboxes
        self.order_search_option_cbx = ttk.Combobox(
            self.bottom_frame,
            width=38,
            values=("Order ID", "Customer ID", "Other Variables"),
        )
        self.order_search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

        # Buttons:
        self.open_order_btn = ttk.Button(
            self.bottom_frame,
            text="Open Selected Record",
            style="btns.TButton",
            padding=21,
            command=self.view_order
        )
        self.open_order_btn.grid(column=0, row=1, sticky=E)

        self.add_order_btn = ttk.Button(
            self.bottom_frame, 
            text="Add New Order",
            style="btns.TButton",
            padding=(10, 21),
            command=self.open_blank_order_form
        )
        self.add_order_btn.grid(column=1, row=1, sticky=E)

        self.search_order_btn = ttk.Button(
            self.bottom_frame, 
            text="Search Order",
            style="btns.TButton",
            padding=(10, 21),
            command=self.search_order
        )
        self.search_order_btn.grid(column=4, row=1, sticky=E)
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#
    def list_orders(self, orders, from_customer=False):
        """List all orders in the database or of a specific customer if from_customer"""
        if not from_customer:
            customers = self.session.query(Customer).all()
        else:
            customers = self.session.query(Customer).filter(Customer.customer_id==orders[0].customer_id)
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
        # Create a dict of customer_id:customer_name for use in update customer
        self.customer_id_name_dict = dict()
        for name in tuple(self.customers_dict):
            self.customer_id_name_dict.update({self.customers_dict[name][0]:name })
        for item in self.tree.get_children():
            self.tree.delete(item)
        for order in orders:
            self.tree.insert('', 'end', iid=f"{order.order_id}",
            values=(
                f"{order.order_id}",
                self.customer_id_name_dict[order.customer_id],
                order.description,
                order.order_date,
                order.is_paid,
                order.notes
                )
            )

    def select_record(self, event):
        # print("Record selected")
        record = self.tree.focus()
        self.selected_order = self.tree.item(record)
    
    def open_blank_order_form(self):
        self.order_details_tab.open_blank_order_form()
        self.notebook.select(6) # Change to tab name instead of index (same on customer)
    
    def view_order(self):
        """View the oder details of the order selected in the order list treeview"""
        # print(f"SELECTED RECORD: {self.selected_order}")
        if not self.selected_order:
            error_message = messagebox.showerror(
                message='No record is selected!',
                title='Error'
            )
            return error_message
        order = db.get_orders(self.session, pk=self.selected_order['values'][0])
        self.order_details_tab.populate_fields(order)
        self.notebook.select(6)
        

    def search_order(self):
        search_option = self.order_search_option_cbx.get()
        search_value = self.order_search_ent.get()
        self.list_orders(self.orders)
        if search_option == "Order ID":
            self.search_by_order_id(search_value)
        elif search_option == "Customer ID":
            self.search_by_customer_id(search_value)
        else:
            self.search_by_other_fields(search_value)
            
    def search_by_order_id(self, order_id=""):
        if not order_id:
            error_message = messagebox.showerror(
                message="Cannot search with a blank Order ID.",
                title='Error'
            )
            return error_message
        try:
            order_id = int(order_id)
        except ValueError as e:
            error_message = messagebox.showerror(
            message="Invalid Order ID.",
            detail="Please ensure that you entered an integer value for Order ID.",
            title='Error'
        )
            return error_message
        try:
            order = db.get_orders(self.session, pk=order_id)
            if order:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.tree.insert('', 'end', iid=f"{order.order_id}",
                values=(
                    f"{order.order_id}",
                    self.customer_id_name_dict[order.customer_id],
                    order.description,
                    order.order_date,
                    order.is_paid,
                    order.notes
                    )
                )
            else:
                info_message = messagebox.showinfo(
                message=f"No record with Order ID {order_id} was found.",
                title='Info'
            )
                return info_message
        except KeyError as e:
                error_message = messagebox.showerror(
                message="Key Error: An error occured wile trying to retrieve customer name.",
                detail=e,
                title='Error'
            )
                return error_message
        except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! Something went wrong.",
                detail=e,
                title='Error'
            )
                return error_message
        
    def search_by_customer_id(self, customer_id=""):
        if not customer_id:
            error_message = messagebox.showerror(
                message="Cannot search with a blank Customer ID.",
                title='Error'
            )
            return error_message
        try:
            customer_id = int(customer_id)
        except ValueError as e:
            error_message = messagebox.showerror(
            message="Invalid Customer ID.",
            detail="Please ensure that you entered an integer value for Customer ID.",
            title='Error'
        )
            return error_message
        try:
            orders = db.get_orders(self.session, customer_id=customer_id)
            if orders:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for order in orders:
                    self.tree.insert('', 'end', iid=f"{order.order_id}",
                    values=(
                        f"{order.order_id}",
                        self.customer_id_name_dict[order.customer_id],
                        order.description,
                        order.order_date,
                        order.is_paid,
                        order.notes
                        )
                    )
            else:
                info_message = messagebox.showinfo(
                message=f"No record with Customer ID {customer_id} was found.",
                title='Info'
            )
                return info_message
        except KeyError as e:
                error_message = messagebox.showerror(
                message="Key Error: An error occured wile trying to retrieve customer name.",
                detail=e,
                title='Error'
            )
                return error_message
        except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! Something went wrong.",
                detail=e,
                title='Error'
            )
                return error_message
        
    def search_by_other_fields(self, other_fields=""):
        try:
            orders = db.get_orders(self.session, other_fields=other_fields)
            if not orders:
                info_message = messagebox.showinfo(
                    message=f"No record matching the term '{other_fields}' was found.",
                    title='Info'
                    )
                return info_message
            for item in self.tree.get_children():
                self.tree.delete(item)
            for order in orders:
                self.tree.insert('', 'end', iid=f"{order.order_id}",
                values=(
                    f"{order.order_id}",
                    self.customer_id_name_dict[order.customer_id],
                    order.description,
                    order.order_date,
                    order.is_paid,
                    order.notes
                    )
                )
        except KeyError as e:
                error_message = messagebox.showerror(
                message="Key Error: An error occured while trying to retrieve customer name.",
                detail=e,
                title='Error'
            )
                return error_message
        except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! Something went wrong.",
                detail=e,
                title='Error'
            )
                return error_message