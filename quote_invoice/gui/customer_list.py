from tkinter import *
from tkinter import messagebox, ttk

from quote_invoice.db import operations as db
from quote_invoice.db.models import Customer


class CustomerListTab:
    def __init__(self, notebook, parent_frame, customer_details_tab, session):
        """Configure the customer list tab"""
        self.session = session
        self.notebook = notebook
        self.selected_customer = None
        self.customer_details_tab = customer_details_tab
        # -------------------------------------TOP FRAME-----------------------------------#
        # Frames:
        self.top_frame = ttk.Frame(
            parent_frame,
            borderwidth=5,
            # relief="solid"
        )
        self.top_frame.grid(column=0, row=0, sticky=(N, W, E, S))
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
        # -------------------------------TOP FRAME ENDS--------------------------------------#

        # -------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(parent_frame, borderwidth=5, relief="solid")
        self.mid_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        self.mid_frame.columnconfigure(0, weight=1)
        # self.mid_frame.columnconfigure(1, weight=1)
        self.mid_frame.rowconfigure(0, weight=1)
        # self.mid_frame.rowconfigure(1, weight=1)

        # Treeviews:
        self.tree = ttk.Treeview(self.mid_frame, show="headings", height=20)

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
            "Notes",
        )

        # Columns to display:
        self.tree["displaycolumns"] = (
            "ID",
            "Customer Name",
            "Town",
            "Phone",
            "Email",
            "Customer Since",
        )

        # Format columns:
        self.tree.column("ID", width=100, anchor=CENTER)
        self.tree.column("Customer Name", width=300, anchor=W)
        self.tree.column("Town", anchor=W)
        self.tree.column("Phone", anchor=W)
        self.tree.column("Email", width=300, anchor=W)
        self.tree.column("Customer Since", anchor=E)

        # Add headings:
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Customer Name", text="Customer Name", anchor=W)
        self.tree.heading("Town", text="Town", anchor=W)
        self.tree.heading("Phone", text="Phone", anchor=W)
        self.tree.heading("Email", text="Email", anchor=W)
        self.tree.heading("Customer Since", text="Customr Since", anchor=E)
        self.tree.grid(column=0, row=0, sticky=(N, S, W, E))
        self.tree.bind("<ButtonRelease-1>", self.select_record)

        # Insert the data in Treeview widget
        self.update_customer_list_tree()

        # Scrollbars:
        y_scroll = ttk.Scrollbar(
            self.mid_frame, orient=VERTICAL, command=self.tree.yview
        )
        x_scroll = ttk.Scrollbar(
            self.mid_frame, orient=HORIZONTAL, command=self.tree.xview
        )
        y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
        x_scroll.grid(column=0, row=1, sticky=(N, S, W, E))
        self.tree["yscrollcommand"] = y_scroll.set
        self.tree["xscrollcommand"] = x_scroll.set

        for child in self.mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)
        # -------------------------------MID FRAME ENDS---------------------------------------#

        # -------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            parent_frame,
            borderwidth=5,
            # relief="solid"
        )
        self.bottom_frame.grid(column=0, row=2, sticky=(N, W, E, S))
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=3)
        self.bottom_frame.columnconfigure(3, weight=2)
        self.bottom_frame.columnconfigure(4, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        # self.bottom_frame.rowconfigure(1, weight=1)

        # Entries:
        self.search_ent = ttk.Entry(
            self.bottom_frame,
        )
        self.search_ent.grid(column=3, row=0, sticky=(S, N, W, E))

        # Comboboxes:
        self.search_option_cbx = ttk.Combobox(
            self.bottom_frame,
            width=38,
            values=("Customer ID", "Other Variables"),
        )
        self.search_option_cbx.grid(column=2, row=0, padx=2, sticky=(S, N, W, E))

        # Buttons:
        self.open_customer_btn = ttk.Button(
            self.bottom_frame,
            text="Open Selected Record",
            style="btns.TButton",
            padding=21,
            command=self.view_customer,
        )
        self.add_customer_btn = ttk.Button(
            self.bottom_frame,
            text="Add New Customer",
            style="btns.TButton",
            padding=(10, 21),
            command=self.open_blank_customer_form,
        )
        self.search_customer_btn = ttk.Button(
            self.bottom_frame,
            text="Search Customer",
            style="btns.TButton",
            padding=(10, 21),
            command=self.search_customer,
        )
        self.open_customer_btn.grid(column=0, row=0, sticky=(S, N, W, E))
        self.add_customer_btn.grid(column=1, row=0, sticky=(S, N, W, E))
        self.search_customer_btn.grid(column=4, row=0, sticky=(S, N, W, E))

        for child in self.bottom_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)
        # -------------------------------BOTTOM FRAME ENDS------------------------------------#
        # self.bind_widgets_to_methods()

    def update_customer_list_tree(self, query=None):
        if query:
            customers = query
        else:
            customers = (
                self.session.query(Customer).order_by(Customer.customer_id).all()
            )
        for item in self.tree.get_children():
            self.tree.delete(item)
        for customer in customers:
            if customer.first_name and customer.last_name:
                customer_name = f"{customer.last_name} {customer.first_name}"
            else:
                customer_name = customer.entity_name
            self.tree.insert(
                "",
                "end",
                iid=f"{customer.customer_id}",
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
                    customer.notes,
                ),
            )

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
                message="No record is selected!", title="Error"
            )
            return error_message
        customer = db.get_customers(
            self.session, pk=self.selected_customer["values"][0]
        )
        self.customer_details_tab.populate_fields(customer)
        self.notebook.select(2)

    def search_customer(self):
        search_option = self.search_option_cbx.get()
        search_value = self.search_ent.get()
        if search_option == "Customer ID":
            customer_id = search_value
            if not customer_id:
                error_message = messagebox.showerror(
                    message="Cannot search with a blank Customer ID.", title="Error"
                )
                return error_message
            try:
                customer_id = int(customer_id)
                try:
                    customer = db.get_customers(self.session, pk=customer_id)
                    if not customer:
                        info_message = messagebox.showinfo(
                            message="No matching record was found.", title="Info"
                        )
                        return info_message
                    self.update_customer_list_tree(query=[customer])
                except Exception as e:
                    error_message = messagebox.showerror(
                        message="Oops! An error occurred while getting or listing the customer.",
                        detail=e,
                        title="Error",
                    )
                    return error_message
            except Exception as e:
                error_message = messagebox.showerror(
                    message="Invalid Customer ID.", detail=e, title="Error"
                )
                return error_message
        else:
            try:
                customers = db.get_customers(self.session, other_fields=search_value)
                if not customers:
                    info_message = messagebox.showinfo(
                        message="No matching record was found.", title="Info"
                    )
                    return info_message
                self.update_customer_list_tree(query=customers)
            except Exception as e:
                error_message = messagebox.showerror(
                    message="Oops! Oops! An error occurred while getting or listing customers.",
                    detail=e,
                    title="Error",
                )
                return error_message
