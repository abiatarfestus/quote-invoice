from tkinter import *
from tkinter import ttk
from moneyed import Money, NAD
from tkinter import messagebox
from datetime import datetime
from quote_invoice.db import operations as db
from quote_invoice.db.models import Customer, Order, OrderItem, Quotation, QuotationItem, Product


class QuotationListTab():
    def __init__(self, notebook, parent_frame, quote_details_tab, session):
        self.notebook = notebook
        self.session = session
        self.selected_quotation = None
        self.quote_details_tab = quote_details_tab
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
            text="Quotation List",
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
        y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
        x_scroll.grid(column=0, row=1, sticky=(E, W))
        self.tree['yscrollcommand'] = y_scroll.set
        self.tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        self.tree['columns'] = (
            "ID",
            "Customer",
            "Description",
            "Quote Date",
            "Accepted", 
            "Closed",
            "Notes"
        )

        self.tree['displaycolumns'] = (
            "ID",
            "Customer",
            "Description",
            "Quote Date",
            "Accepted", 
            "Closed"
        )

        # Format Our Columns
        self.tree.column("ID", anchor=CENTER)
        self.tree.column("Customer", anchor=W)
        self.tree.column("Description", anchor=W)
        self.tree.column("Quote Date", anchor=E)
        self.tree.column("Accepted", anchor=CENTER)
        self.tree.column("Closed", anchor=CENTER)
        self.tree.column("Notes", anchor=W)

        # Create Headings
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Customer", text="Customer", anchor=W)
        self.tree.heading("Description", text="Description", anchor=W)
        self.tree.heading("Quote Date", text="Quote Date", anchor=E)
        self.tree.heading("Accepted", text="Accepted", anchor=CENTER)
        self.tree.heading("Closed", text="Closed", anchor=CENTER)
        self.tree.heading("Notes", text="Notes", anchor=W)

        customers = self.session.query(Customer).all()
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
        self.customer_id_name_dict = dict()
        for name in tuple(self.customers_dict):
            self.customer_id_name_dict.update({self.customers_dict[name][0]:name })
        # print(f"CUSTOMER_ID_NAME DICT: {self.customer_id_name_dict}")

        self.quotations = self.session.query(Quotation).order_by(Quotation.quote_date).all()
        # print(f"TOTAL QUOTATIONS: {len(quotations)}")
        for quote in self.quotations:
            self.tree.insert('', 'end', iid=f"{quote.quote_id}",
            values=(
                f"{quote.quote_id}",
                self.customer_id_name_dict[quote.customer_id],
                quote.description,
                quote.quote_date,
                quote.is_accepted,
                quote.is_closed,
                quote.notes
                )
            )

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
        self.quote_search_ent = ttk.Entry(
            self.bottom_frame,
        )
        self.quote_search_ent.grid(column=3, row=1, sticky=(S, N, W, E))

        # Comboboxes
        self.quote_search_option_cbx = ttk.Combobox(
            self.bottom_frame,
            width=38,
            values=("Quote ID", "Customer ID", "Other Variables"),
        )
        self.quote_search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

        # Buttons:
        self.open_quotation_btn = ttk.Button(
            self.bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21,
            command=self.view_quotation
        )
        self.open_quotation_btn.grid(column=0, row=1, sticky=E)

        self.add_quotation_btn = ttk.Button(
            self.bottom_frame, 
            text="Add New Quotation",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=self.open_blank_quote_form
        )
        self.add_quotation_btn.grid(column=1, row=1, sticky=E)

        self.search_quotation_btn = ttk.Button(
            self.bottom_frame, 
            text="Search Quotation",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=self.search_quotation
        )
        self.search_quotation_btn.grid(column=4, row=1, sticky=E)
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#
       
    def select_record(self, event):
        # print("Record selected")
        record = self.tree.focus()
        self.selected_quotation = self.tree.item(record)
    
    def open_blank_quote_form(self):
        self.quote_details_tab.open_blank_quote_form()
        self.notebook.select(4) # Change to tab name instead of index (same on customer)
    
    def view_quotation(self):
        # print(f"SELECTED RECORD: {self.selected_quotation}")
        quotation = self.selected_quotation
        if not self.selected_quotation:
            error_message = messagebox.showerror(
                message='No record is selected!',
                title='Error'
            )
            return error_message
        self.quote_details_tab.populate_fields(quotation)
        self.notebook.select(4)
        

    def search_quotation(self):
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
                    quotation = db.get_quotations(self.session, pk=quote_id)
                    if quotation:
                        for item in self.tree.get_children():
                            self.tree.delete(item)
                        self.tree.insert('', 'end', iid=f"{quotation.quote_id}",
                        values=(
                            f"{quotation.quote_id}",
                            self.customer_id_name_dict[quotation.customer_id],
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
                    quotations = db.get_quotations(self.session, customer_id=customer_id)
                    if quotations:
                        for item in self.tree.get_children():
                            self.tree.delete(item)
                        for quote in quotations:
                            self.tree.insert('', 'end', iid=f"{quote.quote_id}",
                            values=(
                                f"{quote.quote_id}",
                                self.customer_id_name_dict[quote.customer_id],
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
                quotations = db.get_quotations(self.session, other_fields=search_value)
                if not quotations:
                    info_message = messagebox.showinfo(
                        message="No matching record was found.",
                        title='Info'
                        )
                    return info_message
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for quote in quotations:
                    self.tree.insert('', 'end', iid=f"{quote.quote_id}",
                    values=(
                        f"{quote.quote_id}",
                        self.customer_id_name_dict[quote.customer_id],
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




        

        
        