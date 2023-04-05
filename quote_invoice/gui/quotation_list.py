from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from quote_invoice.db import operations as db
from quote_invoice.db.models import Customer, Quotation


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
            # relief="solid"
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

        self.quotations = self.session.query(Quotation).order_by(Quotation.quote_date).all()
        self.list_quotations(self.quotations)
        self.tree.grid(column=0, row=0, sticky=(N, S, W, E))

        for child in self.mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)
        
        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            parent_frame,
            borderwidth=5, 
            # relief="solid"
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
            style="btns.TButton",
            padding=21,
            command=self.view_quotation
        )
        self.open_quotation_btn.grid(column=0, row=1, sticky=E)

        self.add_quotation_btn = ttk.Button(
            self.bottom_frame, 
            text="Add New Quotation",
            style="btns.TButton",
            padding=(10, 21),
            command=self.open_blank_quote_form
        )
        self.add_quotation_btn.grid(column=1, row=1, sticky=E)

        self.search_quotation_btn = ttk.Button(
            self.bottom_frame, 
            text="Search Quotation",
            style="btns.TButton",
            padding=(10, 21),
            command=self.search_quotation
        )
        self.search_quotation_btn.grid(column=4, row=1, sticky=E)

        for child in self.bottom_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#
       
    def list_quotations(self, quotations, from_customer=False):
        """List all quotations in the database or of a specific customer if from_customer"""
        if not from_customer:
            customers = self.session.query(Customer).all()
        else:
            customers = self.session.query(Customer).filter(Customer.customer_id==quotations[0].customer_id)
            # print(f"CUSTOMERS={customers}")
        self.customers_dict = dict() # {customer display name: [customer details]}
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
        self.customer_id_name_dict = dict() # {customer_id:customer displa name}
        for name in tuple(self.customers_dict):
            self.customer_id_name_dict.update({self.customers_dict[name][0]:name })
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

    def select_record(self, event):
        # print("Record selected")
        record = self.tree.focus()
        self.selected_quotation = self.tree.item(record)
    
    def open_blank_quote_form(self):
        self.quote_details_tab.open_blank_quote_form()
        self.notebook.select(4) # Change to tab name instead of index (same on customer)
    
    def view_quotation(self):
        """View the quote details of the quotation selected in the order list treeview"""
        if not self.selected_quotation:
            error_message = messagebox.showerror(
                message='No record is selected!',
                title='Error'
            )
            return error_message
        quotation = db.get_quotations(self.session, pk=self.selected_quotation['values'][0])
        self.quote_details_tab.populate_fields(quotation)
        self.notebook.select(4)
 
    def search_quotation(self):
        search_option = self.quote_search_option_cbx.get()
        search_value = self.quote_search_ent.get()
        self.list_quotations(self.quotations)
        if search_option == "Quote ID":
            self.search_by_quote_id(search_value)
        elif search_option == "Customer ID":
            self.search_by_customer_id(search_value)
        else:
            self.search_by_other_fields(search_value)
            
    def search_by_quote_id(self, quote_id=""):
        if not quote_id:
            error_message = messagebox.showerror(
                message="Cannot search with a blank Quote ID.",
                title='Error'
            )
            return error_message
        try:
            quote_id = int(quote_id)
        except ValueError as e:
            error_message = messagebox.showerror(
            message="Invalid Quote ID.",
            detail="Please ensure that you entered an integer value for Quote ID.",
            title='Error'
        )
            return error_message
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
                message=f"No record with Order ID {quote_id} was found.",
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
            quotations = db.get_quotations(self.session, other_fields=other_fields)
            if not quotations:
                info_message = messagebox.showinfo(
                    message=f"No record matching the term '{other_fields}' was found.",
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



        

        
        