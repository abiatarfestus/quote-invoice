from datetime import date, datetime
from tkinter import *
from tkinter import messagebox, ttk

from moneyed import NAD, Money

from quote_invoice.db import operations as db
from quote_invoice.db.models import Customer, Product, QuotationItem
from quote_invoice.templates.quote import Quote


class QuoteDetailsTab:
    def __init__(self, notebook, parent_frame, order_details_tab, session):
        """Configure the quote details tab"""
        self.notebook = notebook
        self.session = session
        self.customers = self.session.query(Customer).all()
        self.customers_dict = dict()
        self.order_details_tab = order_details_tab
        for customer in self.customers:
            if customer.customer_type == "Person":
                key = f"{customer.last_name} {customer.first_name} >> {customer.phone}"
            else:
                key = f"{customer.entity_name} >> {customer.phone}"
            self.customers_dict.update(
                {
                    key: [
                        customer.customer_id,
                        customer.customer_type,
                        customer.first_name,
                        customer.last_name,
                        customer.entity_name,
                        customer.email,
                        customer.phone,
                    ]
                }
            )

        # -------------------------------------TOP FRAME-----------------------------------#
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
            text="Quotation Details",
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0, sticky=(N, S, W, E))
        # -------------------------------TOP FRAME ENDS--------------------------------------#

        # -------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(
            parent_frame,
            borderwidth=5,
            # relief="solid"
        )
        self.mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        self.mid_frame.columnconfigure(0, weight=1)
        self.mid_frame.columnconfigure(1, weight=1)
        self.mid_frame.columnconfigure(2, weight=1)
        self.mid_frame.columnconfigure(3, weight=1)
        self.mid_frame.columnconfigure(4, weight=1)
        self.mid_frame.columnconfigure(5, weight=1)
        self.mid_frame.columnconfigure(6, weight=1)
        self.mid_frame.columnconfigure(7, weight=1)
        self.mid_frame.rowconfigure(0, weight=1)
        self.mid_frame.rowconfigure(1, weight=1)
        self.mid_frame.rowconfigure(2, weight=1)
        self.mid_frame.rowconfigure(3, weight=1)
        self.mid_frame.rowconfigure(4, weight=1)
        self.mid_frame.rowconfigure(5, weight=1)
        self.mid_frame.rowconfigure(6, weight=1)

        for child in self.mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=3)

        # Labels:
        self.id_lbl = ttk.Label(
            self.mid_frame,
            text="Quote ID",
            anchor=W,
            style="txt.TLabel",
        )
        self.id_lbl.grid(column=0, row=0, sticky=(W,))

        self.date_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Date",
            anchor=W,
            style="txt.TLabel",
        )
        self.date_lbl.grid(column=0, row=1, sticky=(W,))

        self.quote_description_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Description",
            anchor=W,
            style="txt.TLabel",
        )
        self.quote_description_lbl.grid(column=0, row=2, sticky=(W,))

        self.customer_lbl = ttk.Label(
            self.mid_frame,
            text="Customer",
            anchor=W,
            style="txt.TLabel",
        )
        self.customer_lbl.grid(column=0, row=3, sticky=(W,))

        self.notes_lbl = ttk.Label(
            self.mid_frame,
            text="Notes",
            anchor=E,
            style="txt.TLabel",
        )
        self.notes_lbl.grid(column=5, row=0, sticky=(E,))

        self.quote_amount = StringVar(value="Total Cost:\tN$0.00")
        self.amount_lbl = ttk.Label(
            self.mid_frame,
            textvariable=self.quote_amount,
            # padding=5,
            anchor=E,
            style="txt.TLabel",
        )
        self.amount_lbl.grid(column=6, columnspan=2, row=6, sticky=(N, S, W, E))

        # Entries:
        self.quote_id_ent = ttk.Entry(
            self.mid_frame,
            width=20,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_id_ent.insert(0, "New")
        self.quote_id_ent.state(["disabled"])
        self.quote_id_ent.grid(column=1, columnspan=2, row=0, sticky=(S, N, E, W))

        self.quote_date_ent = ttk.Entry(
            self.mid_frame,
            width=20,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_date_ent.insert(0, date.today().strftime("%Y/%m/%d"))
        self.quote_date_ent.grid(column=1, columnspan=2, row=1, sticky=(S, N, E, W))

        self.quote_description_ent = ttk.Entry(
            self.mid_frame,
            width=20,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_description_ent.grid(
            column=1, columnspan=2, row=2, sticky=(S, N, E, W)
        )

        # Comboboxes:
        self.quote_customer_cbx = ttk.Combobox(
            self.mid_frame,
            width=20,
            values=sorted(tuple(self.customers_dict))
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_customer_cbx.state(["readonly"])
        self.products = session.query(Product).all()
        self.products_dict = {
            product.product_name: [
                product.product_id,
                product.product_name,
                product.description,
                product.price,
                product.quantity,
                product.sku,
                product.barcode,
            ]
            for product in self.products
        }
        self.quote_customer_cbx.grid(column=1, columnspan=2, row=3, sticky=(S, N, E, W))

        # Texts:
        self.quote_notes_txt = Text(
            self.mid_frame,
            width=20,
            height=3,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_notes_txt.grid(
            column=3, columnspan=3, row=1, rowspan=3, sticky=(S, N, E, W)
        )

        # Checkboxes:
        self.is_accepted = BooleanVar()
        self.quote_accepted_chk = ttk.Checkbutton(
            self.mid_frame,
            text="Is Accepted",
            variable=self.is_accepted,
            onvalue=1,
            offvalue=0,
            # state="disabled"
        )
        self.quote_accepted_chk.grid(column=3, row=0, sticky=(S, N, E, W))

        # Buttons:
        self.quote_preview_btn = ttk.Button(
            self.mid_frame,
            text="Print/Preview Quotation",
            style="btns.TButton",
            padding=(0, 10),
            command=self.print_quote,
        )
        self.quote_preview_btn.grid(
            column=6, columnspan=2, row=0, rowspan=2, sticky=(N, W, E, S)
        )

        self.add_quote_btn = ttk.Button(
            self.mid_frame,
            text="Add a New Quotation",
            style="btns.TButton",
            padding=10,
            command=self.open_blank_quote_form,
        )
        self.add_quote_btn.grid(
            column=6, columnspan=2, row=2, rowspan=2, sticky=(N, W, E, S)
        )

        self.quote_save_update = StringVar(value="Save Quotation")
        self.quote_save_update_btn = ttk.Button(
            self.mid_frame,
            textvariable=self.quote_save_update,
            style="btns.TButton",
            padding=5,
            command=self.create_or_update_quotation,
        )
        self.quote_save_update_btn.grid(column=0, row=6, sticky=(N, S, W, E))

        self.generate_order_btn = ttk.Button(
            self.mid_frame,
            text="Generate Order",
            style="btns.TButton",
            padding=10,
            command=self.qenerate_order_from_quote,
        )
        self.generate_order_btn.grid(column=1, row=6, sticky=(N, S, W, E))

        self.mark_closed_btn = ttk.Button(
            self.mid_frame,
            text="Mark as Closed",
            style="btns.TButton",
            padding=10,
            command=self.mark_quote_closed,
        )
        self.mark_closed_btn.grid(column=2, row=6, sticky=(N, S, W, E))

        self.reuse_quote_btn = ttk.Button(
            self.mid_frame,
            text="Reuse Quotation",
            style="btns.TButton",
            padding=10,
            command=self.reuse_quotation,
        )
        self.reuse_quote_btn.grid(column=3, row=6, sticky=(N, S, W, E))

        self.clear_quote_items_btn = ttk.Button(
            self.mid_frame,
            text="Clear Quote Items",
            style="btns.TButton",
            padding=10,
            command=self.clear_quote_items,
        )
        self.clear_quote_items_btn.grid(column=4, row=6, sticky=(N, S, W, E))

        self.reset_quote_btn = ttk.Button(
            self.mid_frame,
            text="Reset Quote",
            style="btns.TButton",
            padding=10,
            command=self.reset_quote,
        )
        self.reset_quote_btn.grid(column=5, row=6, sticky=(N, S, W, E))

        # Treeviews:
        self.quote_items_tree = ttk.Treeview(self.mid_frame, show="headings", height=5)
        self.quote_items_tree.bind("<ButtonRelease-1>", self.select_record)
        # Define Our Columns
        self.quote_items_tree["columns"] = (
            "ID",  # product_id
            "Quote_Item_ID",
            "Item",
            "Description",  # Item description/note, not necessarily product description
            "Quantity",
            "Unit Price",
            "Total Price",
        )

        self.quote_items_tree["displaycolumns"] = (
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
        self.quote_items_tree.column("Description", width=600, anchor=W)
        self.quote_items_tree.column("Quantity", width=100, anchor=E)
        self.quote_items_tree.column("Unit Price", width=100, anchor=E)
        self.quote_items_tree.column("Total Price", anchor=E)

        # Create Headings
        self.quote_items_tree.heading("Item", text="Item", anchor=W)
        self.quote_items_tree.heading("Description", text="Description", anchor=W)
        self.quote_items_tree.heading("Quantity", text="Quantity", anchor=E)
        self.quote_items_tree.heading("Unit Price", text="Unit Price", anchor=E)
        self.quote_items_tree.heading("Total Price", text="Total Price", anchor=E)
        self.quote_items_tree.grid(column=0, columnspan=8, row=4, sticky=(N, S, W, E))

        # Scrollbars:
        y_scroll = ttk.Scrollbar(
            self.mid_frame, orient=VERTICAL, command=self.quote_items_tree.yview
        )
        x_scroll = ttk.Scrollbar(
            self.mid_frame, orient=HORIZONTAL, command=self.quote_items_tree.xview
        )
        y_scroll.grid(column=8, row=4, sticky=(N, S, W))
        x_scroll.grid(column=0, columnspan=8, row=5, sticky=(E, W))
        self.quote_items_tree["yscrollcommand"] = y_scroll.set
        self.quote_items_tree["xscrollcommand"] = x_scroll.set

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
        self.bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E))
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        # Labels:
        self.input_product_lbl = ttk.Label(
            self.bottom_frame,
            text="Product",
            anchor=CENTER,
            # style="heading.TLabel",
        )
        self.input_product_lbl.grid(column=0, row=0, sticky=(N, S, W, E))

        self.input_description_lbl = ttk.Label(
            self.bottom_frame,
            text="Description",
            anchor=CENTER,
            # style="heading.TLabel",
        )
        self.input_description_lbl.grid(column=1, row=0, sticky=(N, S, W, E))

        # Entries:
        self.input_quantity_lbl = ttk.Label(
            self.bottom_frame,
            text="Quantity",
            anchor=CENTER,
            # style="heading.TLabel",
        )
        self.input_quantity_lbl.grid(column=2, row=0, sticky=(N, S, W, E))

        self.quote_input_description_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_input_description_ent.grid(
            column=1, row=1, rowspan=2, sticky=(S, N, E, W)
        )

        # Spinboxes:
        self.quote_input_quantity_spx = ttk.Spinbox(
            self.bottom_frame,
            from_=1,
            to=500000,
        )
        self.quote_input_quantity_spx.grid(column=2, row=1, sticky=(S, N, E, W))

        # Comboboxes:
        self.quote_input_product_cbx = ttk.Combobox(
            self.bottom_frame,
            width=40,
            values=sorted(tuple(self.products_dict))
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_input_product_cbx.grid(
            column=0, row=1, rowspan=2, sticky=(S, N, E, W)
        )
        self.quote_input_product_cbx.bind(
            "<<ComboboxSelected>>", self.populate_item_description
        )

        # Buttons:
        self.quote_input_delete_btn = ttk.Button(
            self.bottom_frame,
            text="Delete Item",
            style="btns.TButton",
            padding=5,
            command=self.delete_item,
        )
        self.quote_input_delete_btn.grid(column=2, row=2, sticky=(N, S, W, E))

        self.quote_input_add_btn = ttk.Button(
            self.bottom_frame,
            text="Add Item",
            style="btns.TButton",
            padding=5,
            command=self.add_item,
        )
        self.quote_input_add_btn.grid(column=3, row=1, rowspan=2, sticky=(N, S, W, E))

        for child in self.bottom_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)

        # -------------------------------BOTTOM FRAME ENDS------------------------------------#

        # product_ids as keys
        self.products_dict2 = {
            product.product_id: product.product_name for product in self.products
        }

    # print(f"PRODUCTS: {products_dict}")
    def populate_item_description(self, event):
        selected_product = self.quote_input_product_cbx.get()
        product_attributes = self.products_dict.get(selected_product)
        if product_attributes:
            product_description = product_attributes[2]
            self.quote_input_description_ent.insert(0, product_description)
            self.quote_input_quantity_spx.set("1")

    def select_record(self, event):
        quotation = db.get_quotations(self.session, pk=self.quote_id_ent.get())
        if quotation:
            if quotation.is_accepted or quotation.is_closed:
                return
        record = self.quote_items_tree.focus()
        selected_item = self.quote_items_tree.item(record)
        self.quote_input_product_cbx.state(["!disabled"])
        self.quote_input_product_cbx.set(
            f"{self.products_dict2[selected_item['values'][0]]}"
        )
        self.quote_input_description_ent.state(["!disabled"])
        self.quote_input_description_ent.delete(0, END)
        self.quote_input_description_ent.insert(0, f"{selected_item['values'][3]}")
        self.quote_input_quantity_spx.state(["!disabled"])
        self.quote_input_quantity_spx.set(f"{selected_item['values'][4]}")
        self.quote_input_delete_btn.state(
            ["!disabled"]
        )  # Needs to check if quotation is closed

    def add_item(self):
        product = self.quote_input_product_cbx.get()
        description = self.quote_input_description_ent.get()
        quantity = self.quote_input_quantity_spx.get()
        if product == "" or quantity == "":
            print("INVALID ITEM")
            error_message = messagebox.showerror(
                message="Cannot add an item without a product or quantity!",
                title="Invalid Item",
            )
            return error_message
        product_id = str(self.products_dict[product][0])
        unit_price = Money(str(self.products_dict[product][3]), NAD)
        total_price = unit_price * int(quantity)
        if self.quote_items_tree.exists(product_id):
            selected_item = self.quote_items_tree.set(product_id, column="Total Price")
            selected_item_total_price = Money(selected_item, NAD)
            quote_amount = Money(self.quote_amount.get()[14:], NAD)
            quote_amount = quote_amount - selected_item_total_price
            self.quote_items_tree.set(
                product_id, column="Description", value=description
            )
            self.quote_items_tree.set(product_id, column="Quantity", value=quantity)
            self.quote_items_tree.set(
                product_id, column="Unit Price", value=str(unit_price.amount)
            )
            self.quote_items_tree.set(
                product_id, column="Total Price", value=str(total_price.amount)
            )
            quote_amount += total_price
        else:
            self.quote_items_tree.insert(
                "",
                "end",
                iid=f"{product_id}",
                values=(
                    product_id,
                    "",  # this is replaced with quote_item_id when data is pulled from the db
                    product,
                    description,
                    quantity,
                    str(unit_price.amount),
                    str(total_price.amount),
                ),
            )
            # print(f"SLICED QUOTE_AMOUNT: {self.quote_amount.get()[14:]}")
            quote_amount = Money(self.quote_amount.get()[14:], NAD)
            quote_amount += total_price
        # print(f"MONEY: {quote_amount.amount}")
        self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")
        self.quote_input_product_cbx.set("")
        self.quote_input_description_ent.delete(0, END)
        self.quote_input_quantity_spx.delete(0, END)
        return

    def delete_item(self):
        product = self.quote_input_product_cbx.get()
        if not product:
            self.quote_input_product_cbx.set("")
            self.quote_input_description_ent.delete(0, END)
            self.quote_input_quantity_spx.delete(0, END)
            return
        try:
            product_id = str(self.products_dict[product][0])
        except KeyError:
            self.reset_quote_input_fields()
            return
        if self.quote_items_tree.exists(product_id):
            selected_item = self.quote_items_tree.set(product_id, column="Total Price")
            selected_item_total_price = Money(selected_item, NAD)
            quote_amount = Money(self.quote_amount.get()[14:], NAD)
            quote_amount = quote_amount - selected_item_total_price
            self.quote_items_tree.delete([product_id])
            self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")
        self.quote_input_product_cbx.set("")
        self.quote_input_description_ent.delete(0, END)
        self.quote_input_quantity_spx.delete(0, END)
        return

    def open_blank_quote_form(self):
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
        self.quote_date_ent.insert(0, date.today().strftime("%Y/%m/%d"))
        self.quote_accepted_chk.state(["!disabled"])
        self.is_accepted.set(value=0)
        self.quote_notes_txt.config(state=NORMAL)
        self.quote_notes_txt.delete("1.0", END)
        self.reset_quote_input_fields()
        self.quote_input_add_btn.state(["!disabled"])
        self.quote_save_update_btn.state(["!disabled"])
        self.mark_closed_btn.state(["!disabled"])
        self.clear_quote_items_btn.state(["!disabled"])
        self.reset_quote_btn.state(["!disabled"])
        self.quote_input_delete_btn.state(["!disabled"])
        for item in self.quote_items_tree.get_children():
            self.quote_items_tree.delete(item)
        self.quote_amount.set("Total Cost:\tN$0.00")
        self.quote_save_update.set("Save Quotation")

    def create_quotation(self):
        try:
            customer_id = self.customers_dict[self.quote_customer_cbx.get()][0]
        except Exception as e:
            error_message = messagebox.showerror(
                message="Invalid customer entered.", detail=e, title="Error"
            )
            return error_message

        try:
            quote_date = datetime.strptime(self.quote_date_ent.get(), "%Y/%m/%d").date()
            new_quote_id = db.add_quotation(
                self.session,
                quote_date=quote_date,
                description=self.quote_description_ent.get(),
                customer_id=customer_id,
                is_accepted=self.is_accepted.get(),
                notes=self.quote_notes_txt.get("1.0", END),
            )
            print(f"NEW QUOTE ID: {new_quote_id}")
        except Exception as e:
            error_message = messagebox.showerror(
                message="Oops! Something went wrong. Quotation could not be created.",
                detail=e,
                title="Error",
            )
            return error_message
        if self.quote_items_tree.get_children():  # If there are items on the list
            try:
                items = []
                for item in self.quote_items_tree.get_children():
                    items.append(self.quote_items_tree.item(item))
                for item in items:
                    db.add_quotation_item(
                        self.session,
                        quote_id=new_quote_id,
                        product_id=item["values"][0],
                        quantity=item["values"][4],
                        description=item["values"][3],
                    )
            except Exception as e:
                error_message = messagebox.showwarning(
                    message="Alert! Something went wrong. Some items could not be added to the Quotation.",
                    detail=e,
                    title="Error",
                )
                return error_message
        quote_items = (
            self.session.query(Product, QuotationItem)
            .join(QuotationItem)
            .filter(QuotationItem.quote_id == new_quote_id)
            .all()
        )
        self.quote_id_ent.state(["!disabled"])
        self.quote_id_ent.delete(0, END)
        print(f"NEW quote ID: {new_quote_id}")
        self.quote_id_ent.insert(0, new_quote_id)
        print(f"New quote id: {new_quote_id}")
        self.quote_id_ent.state(["disabled"])
        self.update_item_list_tree(quote_items)
        self.quote_save_update.set("Update Quotation")
        if self.is_accepted.get():
            self.disable_widgets()
        success_message = messagebox.showinfo(
            message="Quote was successfully created!", title="Success"
        )
        return success_message

    def update_quotation(self):
        quote_id = self.quote_id_ent.get()
        description = self.quote_description_ent.get()
        is_accepted = self.is_accepted.get()
        notes = self.quote_notes_txt.get("1.0", END)
        try:
            db.update_quotation(
                self.session,
                pk=quote_id,
                description=description,
                is_accepted=is_accepted,
                notes=notes,
            )
        except Exception as e:
            error_message = messagebox.showerror(
                message="Oops! Quotation update encountered an error.",
                detail=e,
                title="Error",
            )
            return error_message
        items = []
        item_ids = set()
        old_items = (
            self.session.query(QuotationItem)
            .filter(QuotationItem.quote_id == quote_id)
            .all()
        )
        old_item_ids = [item.quote_item_id for item in old_items]
        if self.quote_items_tree.get_children():  # If there are items on the list
            for item in self.quote_items_tree.get_children():
                items.append(self.quote_items_tree.item(item))
                item_ids.add(self.quote_items_tree.item(item)["values"][1])
            for item in items:
                if not item["values"][1]:  # If it's new item (has no id)
                    try:
                        db.add_quotation_item(
                            self.session,
                            quote_id=quote_id,
                            product_id=item["values"][0],
                            quantity=item["values"][4],
                            description=item["values"][3],
                        )
                    except Exception as e:
                        error_message = messagebox.showerror(
                            message="Error adding item", detail=e, title="Error"
                        )
                        return error_message
                else:
                    try:
                        db.update_quotation_item(
                            self.session,
                            pk=item["values"][1],
                            quantity=item["values"][4],
                            description=item["values"][3],
                        )
                    except Exception as e:
                        error_message = messagebox.showerror(
                            message="Oops! Some items could not be updated.",
                            detail=e,
                            title="Error",
                        )
                        return error_message
        for id in old_item_ids:
            if id not in item_ids:
                db.delete_quotation_item(self.session, pk=id)
        quote_items = (
            self.session.query(Product, QuotationItem)
            .join(QuotationItem)
            .filter(QuotationItem.quote_id == quote_id)
            .all()
        )
        self.update_item_list_tree(quote_items)
        self.quote_save_update.set("Update Quotation")
        if self.is_accepted.get():
            self.disable_widgets()
        success_message = messagebox.showinfo(
            message="Order was successfully updated!", title="Success"
        )
        return success_message

    def create_or_update_quotation(self):
        if self.is_accepted.get():
            if not messagebox.askyesno(
                message="This quote is marked as accepted. Saving it will lock it from editing.\nDo you still want to continue?",
                icon="question",
                title="Close Quote",
            ):
                return
        quote_id = self.quote_id_ent.get()
        if quote_id == "New":
            self.create_quotation()
        else:
            self.update_quotation()

    def mark_quote_closed(self):
        """Change quote is_closed to  true and lock it from editing"""
        quote_id = self.quote_id_ent.get()
        # Prompt if quote not is_accepted
        if quote_id == "New":
            error_message = messagebox.showerror(
                message="Cannot update an unsaved quotation!", title="Invalid Action"
            )
            return error_message
        elif not self.is_accepted.get():
            if not messagebox.askyesno(
                message="This quote has not been accepted. Closing it will lock it from editing.\nDo you still want to close it?",
                icon="question",
                title="Close Quote",
            ):
                return
        elif not messagebox.askyesno(
            message="Closing a quote will lock it from editing.\nDo you still want to continue?",
            icon="question",
            title="Close Quote",
        ):
            return
        quotation = db.get_quotations(self.session, quote_id)
        quotation.is_closed = True
        self.session.commit()
        self.disable_widgets()
        success_message = messagebox.showinfo(
            message="Quotation was successfully updated!", title="Success"
        )
        return success_message

    def populate_fields(self, quotation):
        """Populate quote detail fields with the currect quote details"""
        quote_id = quotation.quote_id
        quote_items = (
            self.session.query(Product, QuotationItem)
            .join(QuotationItem)
            .filter(QuotationItem.quote_id == quote_id)
            .all()
        )
        self.open_blank_quote_form()
        self.quote_id_ent.state(["!disabled"])
        self.quote_id_ent.delete(0, END)
        self.quote_id_ent.insert(0, quote_id)
        self.quote_id_ent.state(["disabled"])
        self.quote_customer_cbx.set(quotation.customer_id)
        self.quote_customer_cbx.state(["disabled"])
        self.quote_description_ent.insert(0, quotation.description)
        self.quote_date_ent.delete(0, END)
        self.quote_date_ent.insert(0, str(quotation.quote_date).replace("-", "/"))
        self.is_accepted.set(value=quotation.is_accepted)
        self.quote_notes_txt.insert("1.0", quotation.notes)
        if quotation.is_accepted or quotation.is_closed:
            self.disable_widgets()
        self.update_item_list_tree(quote_items)
        self.quote_save_update.set("Update Quotation")

    def clear_quote_items(self):
        """Clear all quote items from the treeview"""
        quote_amount = Money("0.00", NAD)
        for item in self.quote_items_tree.get_children():
            self.quote_items_tree.delete(item)
        self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")

    def reset_quote(self):
        """Reset the current active quotation to the last saved state"""
        quote_id = self.quote_id_ent.get()
        if quote_id == "New":
            messagebox.showerror(
                message="An unsaved quote cannot be reset!", title="Error"
            )
            return
        quotation = db.get_quotations(self.session, pk=quote_id)
        self.populate_fields(quotation)

    def reuse_quotation(self):
        """Generate a new quotation from the current quote"""
        quote_id = self.quote_id_ent.get()
        if quote_id == "New":
            messagebox.showerror(
                message="An unsaved quote cannot be reused!", title="Error"
            )
            return
        quotation = db.get_quotations(self.session, pk=quote_id)
        quote_items = (
            self.session.query(Product, QuotationItem)
            .join(QuotationItem)
            .filter(QuotationItem.quote_id == quote_id)
            .all()
        )
        self.open_blank_quote_form()
        self.quote_customer_cbx.state(["!disabled"])
        self.quote_description_ent.insert(0, quotation.description)
        self.is_accepted.set(value=0)
        self.quote_notes_txt.insert("1.0", quotation.notes)
        self.update_item_list_tree(quote_items)

    def qenerate_order_from_quote(self):
        """Generate a new order from the current quotation"""
        quote_id = self.quote_id_ent.get()
        if quote_id == "New":
            messagebox.showerror(
                message="Cannot generate an order from an unsaved quotation!",
                title="Error",
            )
            return
        quotation = db.get_quotations(self.session, pk=quote_id)
        self.order_details_tab.populate_fields_from_quote(quotation)
        self.notebook.select(6)

    def update_item_list_tree(self, quote_items):
        quote_amount = Money("0.00", NAD)
        for item in self.quote_items_tree.get_children():
            self.quote_items_tree.delete(item)
        for product, item in quote_items:
            unit_price = Money(product.price, NAD)
            total_price = unit_price * item.quantity
            self.quote_items_tree.insert(
                "",
                "end",
                iid=f"{product.product_id}",
                values=(
                    product.product_id,
                    item.quote_item_id,
                    product.product_name,
                    item.description,
                    item.quantity,
                    unit_price.amount,
                    total_price.amount,
                ),
            )
            quote_amount += total_price
        self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")

    def reset_quote_input_fields(self):
        self.quote_input_product_cbx.state(["!disabled"])
        self.quote_input_description_ent.state(["!disabled"])
        self.quote_input_quantity_spx.state(["!disabled"])
        self.quote_input_product_cbx.set("")
        self.quote_input_description_ent.delete(0, END)
        self.quote_input_quantity_spx.delete(0, END)

    def disable_widgets(self):
        self.quote_customer_cbx.state(["disabled"])
        self.quote_description_ent.state(["disabled"])
        self.quote_date_ent.state(["disabled"])
        self.quote_accepted_chk.state(["disabled"])
        self.quote_accepted_chk.invoke()
        self.quote_accepted_chk.state(["disabled"])
        self.quote_notes_txt.config(state=DISABLED)
        self.quote_input_product_cbx.state(["disabled"])
        self.quote_input_description_ent.state(["disabled"])
        self.quote_input_quantity_spx.state(["disabled"])
        self.quote_input_add_btn.state(["disabled"])
        self.quote_save_update_btn.state(["disabled"])
        self.clear_quote_items_btn.state(["disabled"])
        self.reset_quote_btn.state(["disabled"])
        self.mark_closed_btn.state(["disabled"])
        self.quote_input_delete_btn.state(["disabled"])

    def print_quote(self):
        try:
            quote_id = int(self.quote_id_ent.get())
        except ValueError as e:
            error_message = messagebox.showerror(
                message="Invalid Quote ID.",
                detail="Please ensure that there is an open quotation.",
                title="Error",
            )
            return error_message
        quote_template = Quote(self.session, quote_id)
        try:
            quote_template.generate_quote_preview()
        except Exception as e:
            messagebox.showerror(message=e, title="Error")
            return
