from datetime import datetime, date
import random
from quote_invoice.db import operations as db
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from faker import Faker
from moneyed import Money, NAD
from sqlalchemy import and_, or_, create_engine, select
from sqlalchemy.orm import sessionmaker
from quote_invoice.db.models import Customer, Order, OrderItem, Quotation, QuotationItem, Product

class QuoteDetailsTab():
    def __init__(self, notebook, parent_frame, session):
        """Configure the quote details tab"""
        self.notebook = notebook
        self.session = session
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
            text="Quotation Details",
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0, sticky=(N, S, W, E))
        #-------------------------------TOP FRAME ENDS--------------------------------------#

        #-------------------------------MID FRAME-------------------------------------------#
        #Frames:
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
            # style="heading.TLabel",
        )
        self.id_lbl.grid(column=0, row=0, sticky=(W, ))

        self.date_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Date",
            anchor=W,
            # style="heading.TLabel",
        )
        self.date_lbl.grid(column=0, row=1, sticky=(W, ))

        self.quote_description_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Description",
            anchor=W,
            # style="heading.TLabel",
        )
        self.quote_description_lbl.grid(column=0, row=2, sticky=(W, ))

        self.customer_lbl = ttk.Label(
            self.mid_frame,
            text="Customer",
            anchor=W,
            # style="heading.TLabel",
        )
        self.customer_lbl.grid(column=0, row=3, sticky=(W, ))

        self.notes_lbl = ttk.Label(
            self.mid_frame,
            text="Notes",
            anchor=E,
            # style="heading.TLabel",
        )
        self.notes_lbl.grid(column=3, row=0, sticky=(E, ))

        # product_description_lbl = ttk.Label(
        #     bottom_frame,
        #     text="Product Description",
        #     anchor=E,
        #     # style="heading.TLabel",
        # )
        # product_description_lbl.grid(column=0, row=0, sticky=(W, ))

        # total_lbl = ttk.Label(
        #     mid_frame,
        #     text="Total Cost:",
        #     anchor=E,
        #     # style="heading.TLabel",
        # )
        # total_lbl.grid(column=3, row=6, sticky=(N, S, W, E))

        self.quote_amount = StringVar(value="Total Cost:\tN$0.00")
        self.amount_lbl = ttk.Label(
            self.mid_frame,
            textvariable=self.quote_amount,
            anchor=E,
            # style="heading.TLabel",
        )
        self.amount_lbl.grid(column=4, row=6, sticky=(N, S, W, E))

        # Entries:
        self.quote_id_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_id_ent.insert(0, "New")
        self.quote_id_ent.state(["disabled"])
        self.quote_id_ent.grid(column=1, row=0, sticky=(S, N, E, W))

        self.quote_date_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_date_ent.insert(0, date.today().strftime('%Y/%m/%d'))
        self.quote_date_ent.grid(column=1, row=1, sticky=(S, N, E, W))

        self.quote_description_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_description_ent.grid(column=1, row=2, sticky=(S, N, E, W))

        # Comboboxes:
        self.quote_customer_cbx = ttk.Combobox(
            self.mid_frame,
            width=38,
            values=sorted(tuple(self.customers_dict))
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_customer_cbx.state(["readonly"])
        self.products = session.query(Product).all()
        self.products_dict = {
            product.product_name:[
                product.product_id,
                product.product_name,
                product.description,
                product.price,
                product.quantity,
                product.sku,
                product.barcode
                ] for product in self.products
            }
        self.quote_customer_cbx.grid(column=1, row=3, sticky=(S, N, E, W))
        
        # Texts:
        self.quote_notes_txt = Text(
            self.mid_frame,
            width=50, 
            height=3,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_notes_txt.grid(column=2, columnspan=2, row=1, rowspan=3, sticky=(S, N, E, W))

        # Checkboxes:
        self.is_accepted =  BooleanVar()
        self.quote_accepted_chk = ttk.Checkbutton(
            self.mid_frame,
            text='Is Accepted',
            variable=self.is_accepted,
            onvalue="True",
            offvalue="False",
            state="disabled"
        )
        self.quote_accepted_chk.grid(column=2, row=0, sticky=(S, N, E, W))

        # Buttons:
        self.quote_preview_btn = ttk.Button(
            self.mid_frame,
            text="Print/Preview Quotation",
            # style="home_btns.TButton",
            padding=(0, 10)
        )
        self.quote_preview_btn.grid(column=4, row=0, rowspan=2, sticky=(N, W, E, S))

        self.add_quote_btn = ttk.Button(
            self.mid_frame,
            text="Add a New Quotation",
            # style="home_btns.TButton",
            padding=10,
            command=self.open_blank_quote_form
        )
        self.add_quote_btn.grid(column=4, row=2, rowspan=2, sticky=(N,W, E, S))

        self.quote_save_update = StringVar(value="Save Quotation")
        self.quote_save_update_btn = ttk.Button(
            self.mid_frame, 
            textvariable=self.quote_save_update,
            # style="home_btns.TButton",
            padding=5,
            command=self.create_or_update_quotation
        )
        self.quote_save_update_btn.grid(column=0, row=6, sticky=(N, S, W, E))

        self.change_to_order_btn = ttk.Button(
            self.mid_frame,
            text="Change to Order",
            # style="home_btns.TButton",
            padding=10,
            # command=change_quote_to_order
        )
        self.change_to_order_btn.grid(column=1, row=6, sticky=(N, S, W, E))

        self.mark_closed_btn = ttk.Button(
            self.mid_frame,
            text="Mark as Closed",
            # style="home_btns.TButton",
            padding=10,
            command=self.mark_quote_closed
        )
        self.mark_closed_btn.grid(column=2, row=6, sticky=(N, S, W, E))

        self.reuse_quote_btn = ttk.Button(
            self.mid_frame,
            text="Reuse Quotation",
            # style="home_btns.TButton",
            padding=10,
            # command=self.reuse_quotation
        )
        self.reuse_quote_btn.grid(column=3, row=6, sticky=(N, S, W, E))

        # Treeviews:
        self.quote_items_tree = ttk.Treeview(self.mid_frame, show='headings', height=5)
        self.quote_items_tree.bind('<ButtonRelease-1>', self.select_record)
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
        
        # Scrollbars:
        y_scroll = ttk.Scrollbar(self.mid_frame, orient=VERTICAL, command=self.quote_items_tree.yview)
        x_scroll = ttk.Scrollbar(self.mid_frame, orient=HORIZONTAL, command=self.quote_items_tree.xview)
        y_scroll.grid(column=5, row=4, sticky=(N, S, W))
        x_scroll.grid(column=0, columnspan=5, row=5, sticky=(E, W))
        self.quote_items_tree['yscrollcommand'] = y_scroll.set
        self.quote_items_tree['xscrollcommand'] = x_scroll.set
        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            parent_frame,
            borderwidth=5, 
            relief="solid"
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
        self.quote_input_description_ent.grid(column=1, row=1, rowspan=2, sticky=(S, N, E, W))

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
        self.quote_input_product_cbx.grid(column=0, row=1, rowspan=2, sticky=(S, N, E, W))
        self.quote_input_product_cbx.bind('<<ComboboxSelected>>', self.populate_item_description)

        # Buttons:
        self.quote_input_delete_btn = ttk.Button(
            self.bottom_frame, 
            text="Delete Item",
            # style="home_btns.TButton",
            padding=5,
            command=self.delete_item
        )
        self.quote_input_delete_btn.grid(column=2, row=2, sticky=(N, S, W, E))

        self.quote_input_add_btn = ttk.Button(
            self.bottom_frame, 
            text="Add Item",
            # style="home_btns.TButton",
            padding=5,
            command=self.add_item
        )
        self.quote_input_add_btn.grid(column=3, row=1, rowspan=2, sticky=(N, S, W, E))

        #-------------------------------BOTTOM FRAME ENDS------------------------------------#
    
        # product_ids as keys
        self.products_dict2 = {
            product.product_id:product.product_name for product in self.products
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
        # print("Record selected")
        # print(f"ITEM EXISTS: {self.quote_items_tree.exists('11')}")
        record = self.quote_items_tree.focus()
        selected_item = self.quote_items_tree.item(record)
        # print(f"SELECTED ITEM: {selected_item}")
        self.quote_input_product_cbx.state(["!disabled"])
        # self.quote_input_product_cbx.delete(0, END)
        self.quote_input_product_cbx.set(f"{self.products_dict2[selected_item['values'][0]]}")
        self.quote_input_description_ent.state(["!disabled"])
        self.quote_input_description_ent.delete(0, END)
        self.quote_input_description_ent.insert(0, f"{selected_item['values'][3]}")
        self.quote_input_quantity_spx.state(["!disabled"])
        self.quote_input_quantity_spx.set(f"{selected_item['values'][4]}")
        self.quote_input_delete_btn.state(["!disabled"]) # Needs to check if quotation is closed


    def add_item(self):
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
        product_id = str(self.products_dict[product][0])
        unit_price = Money(str(self.products_dict[product][3]), NAD)
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

    def delete_item(self):
        product = self.quote_input_product_cbx.get()
        if not product:
            self.quote_input_product_cbx.set("")
            self.quote_input_description_ent.delete(0,END)
            self.quote_input_quantity_spx.delete(0,END)
            return
        try:
            product_id = str(self.products_dict[product][0])
        except KeyError:
            self.quote_input_product_cbx.set("")
            self.quote_input_description_ent.delete(0,END)
            self.quote_input_quantity_spx.delete(0,END)
            return
        if self.quote_items_tree.exists(product_id):
            selected_item = self.quote_items_tree.set(product_id, column="Total Price")
            selected_item_total_price = Money(selected_item, NAD)
            quote_amount = Money(self.quote_amount.get()[14:], NAD)
            quote_amount = quote_amount-selected_item_total_price
            self.quote_items_tree.delete([product_id])
            self.quote_amount.set(f"Total Cost:\tN${quote_amount.amount}")
        self.quote_input_product_cbx.set("")
        self.quote_input_description_ent.delete(0,END)
        self.quote_input_quantity_spx.delete(0,END)
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
        self.quote_input_delete_btn.state(["!disabled"])
        # print(f"ITEMS: {self.quote_items_tree.get_children()}")
        # items = []
        for item in self.quote_items_tree.get_children():
            # items.append(self.quote_items_tree.item(item))
            self.quote_items_tree.delete(item)
        # print(f"ITEMS: {items}")
        self.quote_amount.set("Total Cost:\tN$0.00")
        self.quote_save_update.set("Save Quotation")
        # self.notebook.select(self.quotation_frame)

    
    def create_quotation(self):
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
                self.session, 
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
                            self.session,
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
                    quote_items = self.session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == new_quote_id).all()
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
    
    def update_quotation(self):
        quote_id = self.quote_id_ent.get()
        try:
            quotation = db.get_quotations(self.session, quote_id)
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
            self.session.commit()
            if self.quote_items_tree.get_children(): # If there are items on the list
                try:
                    items = []
                    item_ids = set()
                    old_items = self.session.query(QuotationItem).filter(QuotationItem.quote_id==quote_id).all()
                    old_item_ids = [item.quote_item_id for item in old_items]
                    for item in self.quote_items_tree.get_children():
                        items.append(self.quote_items_tree.item(item))
                        item_ids.add(self.quote_items_tree.item(item)["values"][1])
                    # print(f"ITEM IDs: {item_ids}")
                    # print(f"OLD ITEM IDs: {old_item_ids}")
                    for item in items:
                        if not item["values"][1]: # If it's new item (has no id)
                            db.add_quotation_item(
                                self.session,
                                quote_id=quote_id,
                                product_id=item["values"][0],
                                quantity=item["values"][4],
                                description=item["values"][3]
                            )
                        else:
                            existing_item = self.session.query(QuotationItem).get(item["values"][1])
                            existing_item.product_id=item["values"][0]
                            existing_item.quantity=item["values"][4]
                            existing_item.description=item["values"][3]
                            self.session.commit()
                    for id in old_item_ids:
                        if id not in item_ids:
                            db.delete_quotation_item(self.session, pk=id)
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
                    quote_items = self.session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == quote_id).all()                            
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
    
    
    def create_or_update_quotation(self):
        quote_id = self.quote_id_ent.get()
        if quote_id == "New":
            self.create_quotation()
        else:
            self.update_quotation()

    def mark_quote_closed(self):
        quote_id = self.quote_id_ent.get()
        if quote_id == "New":
            error_message = messagebox.showerror(
                message='Cannot update an unsaved quotation!',
                title='Invalid Action'
            )
            return error_message
        quotation = db.get_quotations(self.session, quote_id)
        quotation.is_closed = True
        self.session.commit()
        self.quote_customer_cbx.state(["disabled"])
        self.quote_description_ent.state(["disabled"])
        self.quote_date_ent.state(["disabled"])
        self.quote_notes_txt.config(state=DISABLED)
        self.quote_accepted_chk.state(["!disabled"])
        # self.quote_accepted_chk.invoke()
        self.quote_accepted_chk.state(["disabled"])
        self.quote_input_product_cbx.state(["disabled"])
        self.quote_input_description_ent.state(["disabled"])
        self.quote_input_quantity_spx.state(["disabled"])
        self.quote_input_add_btn.state(["disabled"])
        self.quote_save_update_btn.state(["disabled"])
        self.change_to_order_btn.state(["disabled"])
        self.mark_closed_btn.state(["disabled"])
        self.quote_input_delete_btn.state(["disabled"])
        success_message = messagebox.showinfo(
            message='Quotation was successfully updated!',
            title='Success'
        )
        return success_message

    def populate_fields(self, quotation):
        # Get quote items from datatbase
        quote_id = quotation['values'][0]
        quote_amount = Money("0.00", NAD)
        quote_items = self.session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == quotation['values'][0]).all()
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
        self.quote_save_update_btn.state(["!disabled"])
        self.change_to_order_btn.state(["!disabled"])
        self.mark_closed_btn.state(["!disabled"])
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
            self.quote_input_delete_btn.state(["disabled"])
        
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
        # self.notebook.select(self.quotation_frame)

        