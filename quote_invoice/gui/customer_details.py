from datetime import date, datetime
from tkinter import *
from tkinter import messagebox, ttk

from quote_invoice.db import operations as db


class CustomerDetailsTab:
    def __init__(
        self, notebook, parent_frame, quotation_list_tab, order_list_tab, session
    ):
        """Configure the customer form tab"""
        self.notebook = notebook
        self.quotation_list_tab = quotation_list_tab
        self.order_list_tab = order_list_tab
        self.session = session
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
            text="Customer Details",
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0, sticky=(N, S, W, E))
        # -------------------------------TOP FRAME ENDS--------------------------------------#

        # -------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(parent_frame, borderwidth=5, relief="solid")
        self.mid_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        self.mid_frame.columnconfigure(0, weight=1)
        self.mid_frame.columnconfigure(1, weight=1)
        self.mid_frame.columnconfigure(2, weight=1)
        self.mid_frame.columnconfigure(3, weight=1)
        self.mid_frame.columnconfigure(4, weight=1)
        self.mid_frame.columnconfigure(5, weight=1)
        self.mid_frame.rowconfigure(0, weight=1)
        self.mid_frame.rowconfigure(1, weight=1)
        self.mid_frame.rowconfigure(2, weight=1)
        self.mid_frame.rowconfigure(3, weight=1)
        self.mid_frame.rowconfigure(4, weight=1)
        self.mid_frame.rowconfigure(5, weight=1)
        self.mid_frame.rowconfigure(6, weight=1)
        self.mid_frame.rowconfigure(7, weight=1)
        self.mid_frame.rowconfigure(8, weight=1)
        self.mid_frame.rowconfigure(9, weight=1)
        self.mid_frame.rowconfigure(10, weight=1)
        self.mid_frame.rowconfigure(11, weight=1)
        self.mid_frame.rowconfigure(12, weight=1)

        for child in self.mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=5)

        # Labels:
        self.id_lbl = ttk.Label(
            self.mid_frame,
            text="Customer ID",
            anchor=W,
            style="txt.TLabel",
        )
        self.id_lbl.grid(column=0, row=1, sticky=(W,))

        self.type_lbl = ttk.Label(
            self.mid_frame,
            text="Customer Type",
            anchor=W,
            style="txt.TLabel",
        )
        self.type_lbl.grid(column=0, row=2, sticky=(W,))

        self.first_name_lbl = ttk.Label(
            self.mid_frame,
            text="First Name",
            anchor=W,
            style="txt.TLabel",
        )
        self.first_name_lbl.grid(column=0, row=3, sticky=(W,))

        self.last_name_lbl = ttk.Label(
            self.mid_frame,
            text="Last Name",
            anchor=W,
            style="txt.TLabel",
        )
        self.last_name_lbl.grid(column=0, row=4, sticky=(W,))

        self.entity_lbl = ttk.Label(
            self.mid_frame,
            text="Entity Name",
            anchor=W,
            style="txt.TLabel",
        )
        self.entity_lbl.grid(column=0, row=5, sticky=(W,))

        self.email_lbl = ttk.Label(
            self.mid_frame,
            text="Email",
            anchor=W,
            style="txt.TLabel",
        )
        self.email_lbl.grid(column=0, row=6, sticky=(W,))

        self.phone_lbl = ttk.Label(
            self.mid_frame,
            text="Phone",
            anchor=W,
            style="txt.TLabel",
        )
        self.phone_lbl.grid(column=0, row=7, sticky=(W,))

        self.address_lbl = ttk.Label(
            self.mid_frame,
            text="Address",
            anchor=W,
            style="txt.TLabel",
        )
        self.address_lbl.grid(column=0, row=8, sticky=(W,))

        self.town_lbl = ttk.Label(
            self.mid_frame,
            text="Town",
            anchor=W,
            style="txt.TLabel",
        )
        self.town_lbl.grid(column=0, row=9, sticky=(W,))

        self.country_lbl = ttk.Label(
            self.mid_frame,
            text="Country",
            anchor=W,
            style="txt.TLabel",
        )
        self.country_lbl.grid(column=0, row=10, sticky=(W,))

        self.since_lbl = ttk.Label(
            self.mid_frame,
            text="Customer Since",
            anchor=W,
            style="txt.TLabel",
        )
        self.since_lbl.grid(column=0, row=11, sticky=(W,))

        self.notes_lbl = ttk.Label(
            self.mid_frame,
            text="Notes",
            anchor=E,
            style="txt.TLabel",
        )
        self.notes_lbl.grid(column=5, row=0, sticky=(E,W,N,S))

        # Entries:
        self.id_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.id_ent.insert(0, "New")
        self.id_ent.state(["disabled"])
        self.id_ent.grid(column=1, row=1, sticky=(N, S, E, W))

        self.first_name_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.first_name_ent.grid(column=1, row=3, sticky=(N, S, E, W))

        self.last_name_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.last_name_ent.grid(column=1, row=4, sticky=(N, S, E, W))

        self.entity_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.entity_ent.grid(column=1, row=5, sticky=(N, S, E, W))

        self.email_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.email_ent.grid(column=1, row=6, sticky=(N, S, E, W))

        self.phone_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.phone_ent.grid(column=1, row=7, sticky=(N, S, E, W))

        self.address_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.address_ent.grid(column=1, row=8, sticky=(N, S, E, W))

        self.town_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.town_ent.grid(column=1, row=9, sticky=(N, S, E, W))

        self.country_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.country_ent.insert(0, "Namibia")
        self.country_ent.grid(column=1, row=10, sticky=(N, S, E, W))

        self.since_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.since_ent.insert(0, date.today().strftime("%Y/%m/%d"))
        self.since_ent.grid(column=1, row=11, sticky=(N, S, E, W))

        # Comboboxes
        self.type_cbx = ttk.Combobox(
            self.mid_frame,
            width=38,
            values=("Person", "Entity")
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.type_cbx.state(["readonly"])
        self.type_cbx.grid(column=1, row=2, sticky=(N, S, E, W))

        # Texts
        self.notes_txt = Text(
            self.mid_frame,
            width=35,
            height=9,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.notes_txt.grid(
            column=2, columnspan=4, row=1, rowspan=5, sticky=(N, S, E, W)
        )

        # Buttons:
        self.save_btn = ttk.Button(
            self.mid_frame,
            text="Save Record",
            style="btns.TButton",
            padding=5,
            command=self.create_or_update_customer,
        )
        self.save_btn.grid(column=0, columnspan=6, row=12, sticky=(E, W))

        self.new_customer_btn = ttk.Button(
            self.mid_frame,
            text="New Customer",
            style="btns.TButton",
            padding=5,
            command=self.open_blank_customer_form,
        )
        self.new_customer_btn.grid(column=2, row=6, sticky=(N, S, E, W))

        self.quotes_btn = ttk.Button(
            self.mid_frame,
            text="View Quotes",
            style="btns.TButton",
            padding=5,
            command=self.view_customer_quotations,
        )
        self.quotes_btn.grid(column=3, row=6, sticky=(N, S, E, W))

        self.orders_btn = ttk.Button(
            self.mid_frame,
            text="View Orders",
            style="btns.TButton",
            padding=5,
            command=self.view_customer_orders,
        )
        self.orders_btn.grid(column=4, columnspan=2, row=6, sticky=(N, S, E, W))
        self.disable_buttons()

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
        self.bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))
        # -------------------------------BOTTOM FRAME ENDS------------------------------------#

    def open_blank_customer_form(self):
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
        self.country_ent.insert(0, "Namibia")
        self.since_ent.state(["!disabled"])
        self.since_ent.delete(0, END)
        self.since_ent.insert(0, date.today().strftime("%Y/%m/%d"))
        self.notes_txt.delete("1.0", END)
        self.save_btn.configure(text="Save Record")
        self.disable_buttons()

    def create_or_update_customer(self):
        customer_id = self.id_ent.get()
        if customer_id == "New":
            try:
                db.add_customer(
                    self.session,
                    customer_type=self.type_cbx.get(),
                    first_name=self.first_name_ent.get(),
                    last_name=self.last_name_ent.get(),
                    entity_name=self.entity_ent.get(),
                    email=self.email_ent.get(),
                    phone=self.phone_ent.get(),
                    address=self.address_ent.get(),
                    town=self.town_ent.get(),
                    country=self.country_ent.get(),
                    customer_since=datetime.strptime(
                        self.since_ent.get(), "%Y/%m/%d"
                    ).date(),
                    notes=self.notes_txt.get("1.0", END),
                )
                # self.open_blank_customer_form()
                self.since_ent.state(["disabled"])
                self.enable_buttons()
                self.save_btn.configure(text="Update Record")
                success_message = messagebox.showinfo(
                    message="Customer was successfully created!", title="Success"
                )
                return success_message
            except Exception as e:
                error_message = messagebox.showerror(
                    message="Oops! Something went wrong.", detail=e, title="Error"
                )
                return error_message
        else:
            try:
                customer = db.get_customers(self.session, customer_id)
                db.update_customer(
                    self.session,
                    pk=customer.customer_id,
                    customer_type=self.type_cbx.get(),
                    first_name=self.first_name_ent.get(),
                    last_name=self.last_name_ent.get(),
                    entity_name=self.entity_ent.get(),
                    email=self.email_ent.get(),
                    phone=self.phone_ent.get(),
                    address=self.address_ent.get(),
                    town=self.town_ent.get(),
                    country=self.country_ent.get(),
                    notes=self.notes_txt.get("1.0", END),
                )
                success_message = messagebox.showinfo(
                    message="Record was successfully updated!", title="Success"
                )
                return success_message
            except Exception as e:
                error_message = messagebox.showerror(
                    message="Oops! Something went wrong.", detail=e, title="Error"
                )
                return error_message

    def populate_fields(self, customer):
        self.id_ent.state(["!disabled"])
        self.id_ent.delete(0, END)
        self.id_ent.insert(0, customer.customer_id)
        self.id_ent.state(["disabled"])
        self.type_cbx.set(customer.customer_type)
        self.first_name_ent.delete(0, END)
        self.first_name_ent.insert(0, customer.first_name)
        self.last_name_ent.delete(0, END)
        self.last_name_ent.insert(0, customer.last_name)
        self.entity_ent.delete(0, END)
        self.entity_ent.insert(0, customer.entity_name)
        self.email_ent.delete(0, END)
        self.email_ent.insert(0, customer.email)
        self.phone_ent.delete(0, END)
        self.phone_ent.insert(0, customer.phone)
        self.address_ent.delete(0, END)
        self.address_ent.insert(0, customer.address)
        self.town_ent.delete(0, END)
        self.town_ent.insert(0, customer.town)
        self.country_ent.delete(0, END)
        self.country_ent.insert(0, customer.country)
        self.since_ent.delete(0, END)
        self.since_ent.insert(0, customer.customer_since)
        self.since_ent.state(["disabled"])
        self.notes_txt.delete("1.0", END)
        self.notes_txt.insert("1.0", customer.notes)
        self.save_btn.configure(text="Update Record")
        self.enable_buttons()

    def enable_buttons(self):
        self.orders_btn.state(["!disabled"])
        self.quotes_btn.state(["!disabled"])

    def disable_buttons(self):
        self.orders_btn.state(["disabled"])
        self.quotes_btn.state(["disabled"])

    def view_customer_quotations(self):
        customer_id = self.id_ent.get()
        if customer_id == "New":
            return messagebox.showerror(
                message="Cannot open quotations of an unsaved customer!", title="Error"
            )
        quotations = db.get_quotations(self.session, customer_id=customer_id)
        if not quotations:
            return messagebox.showinfo(
                message="No quotations found for this customer.", title="Info"
            )
        self.quotation_list_tab.list_quotations(quotations, from_customer=True)
        self.notebook.select(3)

    def view_customer_orders(self):
        customer_id = self.id_ent.get()
        if customer_id == "New":
            return messagebox.showerror(
                message="Cannot open orders of an unsaved customer!", title="Error"
            )
        orders = db.get_orders(self.session, customer_id=customer_id)
        if not orders:
            return messagebox.showinfo(
                message="No orders found for this customer.", title="Info"
            )
        self.order_list_tab.list_orders(orders, from_customer=True)
        self.notebook.select(5)
