from tkinter import *
from tkinter import messagebox, ttk

from quote_invoice.db import operations as db
from quote_invoice.db.models import (
    Customer,
    Order,
    OrderItem,
    Product,
    Quotation,
    QuotationItem,
)
from quote_invoice.gui import customer_details


def setup_customer_list_tab(notebook, parent_frame, session):
    """Configure the customer list tab"""
    # -------------------------------------TOP FRAME-----------------------------------#
    # Frames:
    top_frame = ttk.Frame(parent_frame, borderwidth=5, relief="solid")
    top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
    top_frame.columnconfigure(0, weight=1)
    top_frame.rowconfigure(0, weight=1)

    # Labels:
    heading_lbl = ttk.Label(
        top_frame,
        text="Customer List",
        anchor="center",
        style="heading.TLabel",
    )
    heading_lbl.grid(column=0, row=0, sticky=(S, N, W, E))
    # -------------------------------TOP FRAME ENDS--------------------------------------#

    # -------------------------------MID FRAME-------------------------------------------#
    # Frames:
    mid_frame = ttk.Frame(parent_frame, borderwidth=5, relief="solid")
    mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
    mid_frame.columnconfigure(0, weight=1)
    mid_frame.columnconfigure(1, weight=1)
    mid_frame.rowconfigure(0, weight=1)
    mid_frame.rowconfigure(1, weight=1)

    # Treeviews:
    tree = ttk.Treeview(mid_frame, show="headings", height=20)
    tree.bind("<ButtonRelease-1>", select_record)

    # Define columns:
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
        "Notes",
    )

    # Columns to display:
    tree["displaycolumns"] = (
        "ID",
        "Customer Name",
        "Town",
        "Phone",
        "Email",
        "Customer Since",
    )

    # Format columns:
    tree.column("ID", anchor=CENTER)
    tree.column("Customer Name", anchor=W)
    tree.column("Town", anchor=W)
    tree.column("Phone", anchor=W)
    tree.column("Email", anchor=W)
    tree.column("Customer Since", anchor=E)

    # Add headings:
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
        tree.insert(
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
    tree.grid(column=0, row=0, sticky=(N, S, W, E))

    # Scrollbars:
    y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
    x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
    y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
    x_scroll.grid(column=0, row=1, sticky=(E, W))
    tree["yscrollcommand"] = y_scroll.set
    tree["xscrollcommand"] = x_scroll.set
    # -------------------------------MID FRAME ENDS---------------------------------------#

    # -------------------------------BOTTOM FRAME-----------------------------------------#
    # Frames:
    bottom_frame = ttk.Frame(parent_frame, borderwidth=5, relief="solid")
    bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

    # Entries:
    search_ent = ttk.Entry(
        bottom_frame,
    )
    search_ent.grid(column=3, row=1, sticky=(S, N, W, E))

    # Comboboxes:
    search_option_cbx = ttk.Combobox(
        bottom_frame,
        width=38,
        values=("Customer ID", "Other Variables"),
    )
    search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

    # Buttons:
    open_customer_btn = ttk.Button(
        bottom_frame,
        text="Open Selected Record",
        # style="home_btns.TButton",
        padding=21,
        command=view_customer,
    )
    add_customer_btn = ttk.Button(
        bottom_frame,
        text="Add New Customer",
        # style="home_btns.TButton",
        padding=(10, 21),
        command=open_blank_customer_form,
    )
    search_customer_btn = ttk.Button(
        bottom_frame,
        text="Search Customer",
        # style="home_btns.TButton",
        padding=(10, 21),
        command=search_customer,
    )
    open_customer_btn.grid(column=0, row=1, sticky=E)
    add_customer_btn.grid(column=1, row=1, sticky=E)
    search_customer_btn.grid(column=4, row=1, sticky=E)
    # -------------------------------BOTTOM FRAME ENDS------------------------------------#

    selected_customer = None

    def select_record(event):
        global selected_customer
        print("Record selected")
        record = tree.focus()
        selected_customer = tree.item(record)

    def open_blank_customer_form():
        customer_details.new_customer()
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
        notebook.select(customer_frame)

    def view_customer():
        print(f"SELECTED RECORD: {selected_customer}")
        customer = selected_customer
        if not selected_customer:
            error_message = messagebox.showerror(
                message="No record is selected!", title="Error"
            )
            return error_message
        customer_details.populate(customer)
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
        notebook.select(customer_frame)

    def search_customer(session):
        search_option = search_option_cbx.get()
        search_value = search_ent.get()
        if search_option == "Customer ID":
            customer_id = search_value
            if not customer_id:
                error_message = messagebox.showerror(
                    message="Cannot search with blank Customer ID.", title="Error"
                )
                return error_message
            try:
                customer_id = int(customer_id)
                try:
                    customer = db.get_customers(session, pk=customer_id)
                    if customer:
                        if customer.first_name and customer.last_name:
                            customer_name = (
                                f"{customer.last_name} {customer.first_name}"
                            )
                        else:
                            customer_name = customer.entity_name
                        for item in tree.get_children():
                            tree.delete(item)
                        tree.insert(
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
                    else:
                        info_message = messagebox.showinfo(
                            message="No matching record was found.", title="Info"
                        )
                        return info_message
                except Exception as e:
                    error_message = messagebox.showerror(
                        message="Oops! Something went wrong.", detail=e, title="Error"
                    )
                    return error_message
            except Exception as e:
                error_message = messagebox.showerror(
                    message="Invalid Customer ID.", detail=e, title="Error"
                )
                return error_message
        else:
            try:
                customers = db.get_customers(session, other_fields=search_value)
                if not customers:
                    info_message = messagebox.showinfo(
                        message="No matching record was found.", title="Info"
                    )
                    return info_message
                for item in tree.get_children():
                    tree.delete(item)
                for customer in customers:
                    if customer.first_name and customer.last_name:
                        customer_name = f"{customer.last_name} {customer.first_name}"
                    else:
                        customer_name = customer.entity_name
                    tree.insert(
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
            except Exception as e:
                error_message = messagebox.showerror(
                    message="Oops! Something went wrong.", detail=e, title="Error"
                )
                return error_message
