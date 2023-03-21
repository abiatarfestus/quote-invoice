from datetime import datetime, date
from quote_invoice.db import operations as db
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from moneyed import Money, NAD
from quote_invoice.db.models import Customer, OrderItem, Product


class OrderDetailsTab():
    def __init__(self, notebook, parent_frame, session):
        """Configure the order details tab"""
        self.notebook = notebook
        self.session = session
        self.customers = self.session.query(Customer).all()
        self.customers_dict = dict()
        for customer in self.customers:
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
            text="Order Details",
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
            text="Order ID",
            anchor=W,
            # style="heading.TLabel",
        )
        self.id_lbl.grid(column=0, row=0, sticky=(W, ))

        self.date_lbl = ttk.Label(
            self.mid_frame,
            text="Order Date",
            anchor=W,
            # style="heading.TLabel",
        )
        self.date_lbl.grid(column=0, row=1, sticky=(W, ))

        self.order_description_lbl = ttk.Label(
            self.mid_frame,
            text="Order Description",
            anchor=W,
            # style="heading.TLabel",
        )
        self.order_description_lbl.grid(column=0, row=2, sticky=(W, ))

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

        self.order_amount = StringVar(value="Total Cost:\tN$0.00")
        self.amount_lbl = ttk.Label(
            self.mid_frame,
            textvariable=self.order_amount,
            anchor=E,
            # style="heading.TLabel",
        )
        self.amount_lbl.grid(column=4, row=6, sticky=(N, S, W, E))

        # Entries:
        self.order_id_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.order_id_ent.insert(0, "New")
        self.order_id_ent.state(["disabled"])
        self.order_id_ent.grid(column=1, row=0, sticky=(S, N, E, W))

        self.order_date_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.order_date_ent.insert(0, date.today().strftime('%Y/%m/%d'))
        self.order_date_ent.grid(column=1, row=1, sticky=(S, N, E, W))

        self.order_description_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.order_description_ent.grid(column=1, row=2, sticky=(S, N, E, W))

        # Comboboxes:
        self.order_customer_cbx = ttk.Combobox(
            self.mid_frame,
            width=38,
            values=sorted(tuple(self.customers_dict))
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.order_customer_cbx.state(["readonly"])
        self.products = self.session.query(Product).all()
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
        self.order_customer_cbx.grid(column=1, row=3, sticky=(S, N, E, W))
        
        # Texts:
        self.order_notes_txt = Text(
            self.mid_frame,
            width=50, 
            height=3,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.order_notes_txt.grid(column=2, columnspan=2, row=1, rowspan=3, sticky=(S, N, E, W))

        # Checkboxes:
        self.is_paid =  BooleanVar()
        self.order_paid_chk = ttk.Checkbutton(
            self.mid_frame,
            text='Is Paid',
            variable=self.is_paid,
            onvalue=1,
            offvalue=0,
            # state="disabled"
        )
        self.order_paid_chk.grid(column=2, row=0, sticky=(S, N, E, W))

        # Buttons:
        self.order_preview_btn = ttk.Button(
            self.mid_frame,
            text="Print/Preview Order",
            # style="home_btns.TButton",
            padding=(0, 10)
        )
        self.order_preview_btn.grid(column=4, row=0, rowspan=2, sticky=(N, W, E, S))

        self.add_order_btn = ttk.Button(
            self.mid_frame,
            text="Add a New Order",
            # style="home_btns.TButton",
            padding=10,
            command=self.open_blank_order_form
        )
        self.add_order_btn.grid(column=4, row=2, rowspan=2, sticky=(N,W, E, S))

        self.order_save_update = StringVar(value="Save Order")
        self.order_save_update_btn = ttk.Button(
            self.mid_frame, 
            textvariable=self.order_save_update,
            # style="home_btns.TButton",
            padding=5,
            command=self.create_or_update_order
        )
        self.order_save_update_btn.grid(column=0, row=6, sticky=(N, S, W, E))

        self.clear_order_items_btn = ttk.Button(
            self.mid_frame,
            text="Clear Order Items",
            # style="home_btns.TButton",
            padding=10,
            command=self.clear_order_items
        )
        self.clear_order_items_btn.grid(column=1, row=6, sticky=(N, S, W, E))

        self.reuse_order_btn = ttk.Button(
            self.mid_frame,
            text="Reuse Order",
            # style="home_btns.TButton",
            padding=10,
            command=self.reuse_order
        )
        self.reuse_order_btn.grid(column=2, row=6, sticky=(N, S, W, E))

        self.reset_order_btn = ttk.Button(
            self.mid_frame,
            text="Reset Order",
            # style="home_btns.TButton",
            padding=10,
            command=self.reset_order
        )
        self.reset_order_btn.grid(column=3, row=6, sticky=(N, S, W, E))

        # Treeviews:
        self.order_items_tree = ttk.Treeview(self.mid_frame, show='headings', height=5)
        self.order_items_tree.bind('<ButtonRelease-1>', self.select_record)
        # Define Our Columns
        self.order_items_tree['columns'] = (
            "ID", # product_id
            "Order_Item_ID",
            "Item", 
            "Description", # Item description/note, not necessarily product description
            "Quantity", 
            "Unit Price", 
            "Total Price",
        )

        self.order_items_tree['displaycolumns'] = (
            "Item", 
            "Description", 
            "Quantity", 
            "Unit Price", 
            "Total Price",
        )

        # Format Our Columns
        self.order_items_tree.column("ID", anchor=CENTER)
        self.order_items_tree.column("Order_Item_ID", anchor=CENTER)
        self.order_items_tree.column("Item", anchor=W)
        self.order_items_tree.column("Description", width=600, anchor=W)
        self.order_items_tree.column("Quantity", width=100, anchor=E)
        self.order_items_tree.column("Unit Price", width=100, anchor=E)
        self.order_items_tree.column("Total Price", anchor=E)

        # Create Headings
        self.order_items_tree.heading("Item", text="Item", anchor=W)
        self.order_items_tree.heading("Description", text="Description", anchor=W)
        self.order_items_tree.heading("Quantity", text="Quantity", anchor=E)
        self.order_items_tree.heading("Unit Price", text="Unit Price", anchor=E)
        self.order_items_tree.heading("Total Price", text="Total Price", anchor=E)
        self.order_items_tree.grid(column=0, columnspan=5, row=4, sticky=(N, S, W, E))
        
        # Scrollbars:
        y_scroll = ttk.Scrollbar(self.mid_frame, orient=VERTICAL, command=self.order_items_tree.yview)
        x_scroll = ttk.Scrollbar(self.mid_frame, orient=HORIZONTAL, command=self.order_items_tree.xview)
        y_scroll.grid(column=5, row=4, sticky=(N, S, W))
        x_scroll.grid(column=0, columnspan=5, row=5, sticky=(E, W))
        self.order_items_tree['yscrollcommand'] = y_scroll.set
        self.order_items_tree['xscrollcommand'] = x_scroll.set
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

        self.order_input_description_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.order_input_description_ent.grid(column=1, row=1, rowspan=2, sticky=(S, N, E, W))

        # Spinboxes:
        self.order_input_quantity_spx = ttk.Spinbox(
            self.bottom_frame,
            from_=1,
            to=500000,
        )
        self.order_input_quantity_spx.grid(column=2, row=1, sticky=(S, N, E, W))

        # Comboboxes:
        self.order_input_product_cbx = ttk.Combobox(
            self.bottom_frame,
            width=40,
            values=sorted(tuple(self.products_dict))
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.order_input_product_cbx.grid(column=0, row=1, rowspan=2, sticky=(S, N, E, W))
        self.order_input_product_cbx.bind('<<ComboboxSelected>>', self.populate_item_description)

        # Buttons:
        self.order_input_delete_btn = ttk.Button(
            self.bottom_frame, 
            text="Delete Item",
            # style="home_btns.TButton",
            padding=5,
            command=self.delete_item
        )
        self.order_input_delete_btn.grid(column=2, row=2, sticky=(N, S, W, E))

        self.order_input_add_btn = ttk.Button(
            self.bottom_frame, 
            text="Add Item",
            # style="home_btns.TButton",
            padding=5,
            command=self.add_item
        )
        self.order_input_add_btn.grid(column=3, row=1, rowspan=2, sticky=(N, S, W, E))

        #-------------------------------BOTTOM FRAME ENDS------------------------------------#
    
        # product_ids as keys
        self.products_dict2 = {
            product.product_id:product.product_name for product in self.products
            }
    # print(f"PRODUCTS: {products_dict}")
    def populate_item_description(self, event):
        selected_product = self.order_input_product_cbx.get()
        product_attributes = self.products_dict.get(selected_product)
        if product_attributes:
            product_description = product_attributes[2]
            self.order_input_description_ent.insert(0, product_description)
            self.order_input_quantity_spx.set("1")      

    
    def select_record(self, event):
        order = db.get_orders(self.session, pk=self.order_id_ent.get())
        if order.is_paid:
            return
        record = self.order_items_tree.focus()
        selected_item = self.order_items_tree.item(record)
        # print(f"SELECTED ITEM: {selected_item}")
        self.order_input_product_cbx.state(["!disabled"])
        # self.order_input_product_cbx.delete(0, END)
        self.order_input_product_cbx.set(f"{self.products_dict2[selected_item['values'][0]]}")
        self.order_input_description_ent.state(["!disabled"])
        self.order_input_description_ent.delete(0, END)
        self.order_input_description_ent.insert(0, f"{selected_item['values'][3]}")
        self.order_input_quantity_spx.state(["!disabled"])
        self.order_input_quantity_spx.set(f"{selected_item['values'][4]}")
        self.order_input_delete_btn.state(["!disabled"]) # Needs to check if order is closed


    def add_item(self):
        product = self.order_input_product_cbx.get()
        description = self.order_input_description_ent.get()
        quantity = self.order_input_quantity_spx.get()
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
        if self.order_items_tree.exists(product_id):
            selected_item = self.order_items_tree.set(product_id, column="Total Price")
            selected_item_total_price = Money(selected_item, NAD)
            # print(f"SELECTED ITEM TOTAL PRICE: {selected_item_total_price}")
            order_amount = Money(self.order_amount.get()[14:], NAD)
            order_amount = order_amount-selected_item_total_price
            self.order_items_tree.set(product_id, column="Description", value=description)
            self.order_items_tree.set(product_id, column="Quantity", value=quantity)
            self.order_items_tree.set(product_id, column="Unit Price", value=str(unit_price.amount))
            self.order_items_tree.set(product_id, column="Total Price", value=str(total_price.amount))
            order_amount += total_price
        else:
            self.order_items_tree.insert('', 'end', iid=f"{product_id}",
            values=(
                product_id,  
                "", # this is replaced with order_item_id when data is pulled from the db
                product,
                description,
                quantity,
                str(unit_price.amount),
                str(total_price.amount)
                )
        )
            # print(f"SLICED QUOTE_AMOUNT: {self.order_amount.get()[14:]}")
            order_amount = Money(self.order_amount.get()[14:], NAD)
            order_amount += total_price
        # print(f"MONEY: {order_amount.amount}")
        self.order_amount.set(f"Total Cost:\tN${order_amount.amount}")
        self.order_input_product_cbx.set("")
        self.order_input_description_ent.delete(0,END)
        self.order_input_quantity_spx.delete(0,END)
        return

    def delete_item(self):
        """Delete the product from the item list treeview or reset the item input fields if product indicated is not on the item list"""
        product = self.order_input_product_cbx.get()
        if not product:
            self.order_input_product_cbx.set("")
            self.order_input_description_ent.delete(0,END)
            self.order_input_quantity_spx.delete(0,END)
            return
        try:
            product_id = str(self.products_dict[product][0])
        except KeyError:
            self.reset_order_input_fields()
            return
        if self.order_items_tree.exists(product_id):
            selected_item = self.order_items_tree.set(product_id, column="Total Price")
            selected_item_total_price = Money(selected_item, NAD)
            order_amount = Money(self.order_amount.get()[14:], NAD)
            order_amount = order_amount-selected_item_total_price
            self.order_items_tree.delete([product_id])
            self.order_amount.set(f"Total Cost:\tN${order_amount.amount}")
        self.order_input_product_cbx.set("")
        self.order_input_description_ent.delete(0,END)
        self.order_input_quantity_spx.delete(0,END)
        return

    def open_blank_order_form(self):
        self.order_id_ent.state(["!disabled"])
        self.order_id_ent.delete(0, END)
        self.order_id_ent.insert(0, "New")
        self.order_id_ent.state(["disabled"])
        self.order_customer_cbx.state(["!disabled"])
        self.order_customer_cbx.set("")
        self.order_description_ent.state(["!disabled"])
        self.order_description_ent.delete(0, END)
        self.order_date_ent.state(["!disabled"])
        self.order_date_ent.delete(0, END)
        self.order_date_ent.insert(0, date.today().strftime('%Y/%m/%d'))
        self.order_paid_chk.state(["!disabled"])
        self.is_paid.set(value=0)
        self.order_notes_txt.delete("1.0", END)
        self.reset_order_input_fields()
        self.order_input_add_btn.state(["!disabled"])
        self.order_save_update_btn.state(["!disabled"])
        self.clear_order_items_btn.state(["!disabled"])
        self.reset_order_btn.state(["!disabled"])
        self.order_input_delete_btn.state(["!disabled"])
        # print(f"ITEMS: {self.order_items_tree.get_children()}")
        # items = []
        for item in self.order_items_tree.get_children():
            # items.append(self.order_items_tree.item(item))
            self.order_items_tree.delete(item)
        # print(f"ITEMS: {items}")
        self.order_amount.set("Total Cost:\tN$0.00")
        self.order_save_update.set("Save Order")
        # self.notebook.select(self.order_frame)

    
    def create_order(self):
        try:
            customer_id = self.customers_dict[self.order_customer_cbx.get()][0]
        except Exception as e:
            error_message = messagebox.showerror(
            message="Invalid customer entered.",
            detail=e,
            title='Error'
        )
            return error_message
        
        try:
            order_date=datetime.strptime(self.order_date_ent.get(), '%Y/%m/%d').date()
            new_order_id = db.add_order(
                self.session, 
                order_date=order_date,
                description=self.order_description_ent.get(),
                customer_id=customer_id,
                is_paid=self.is_paid.get(),
                notes=self.order_notes_txt.get("1.0", END)
            )
            print(f"NEW ORDER ID: {new_order_id}")
        except Exception as e:
            error_message = messagebox.showerror(
            message="Oops! Something went wrong. Order could not be created.",
            detail=e,
            title='Error'
        )
            return error_message
            
        if self.order_items_tree.get_children(): # If there are items on the list
            print("Order Contains Item")
            try:
                items = []
                for item in self.order_items_tree.get_children():
                    items.append(self.order_items_tree.item(item))
                for item in items:
                    db.add_order_item(
                        self.session,
                        order_id=new_order_id,
                        product_id=item["values"][0],
                        quantity=item["values"][4],
                        description=item["values"][3]
                    )
            except Exception as e:
                messagebox.showwarning(
                message="Alert! Something went wrong. Some items might not be added to the Order.",
                detail=e,
                title='Error'
            )
        order_items = self.session.query(Product, OrderItem).join(OrderItem).filter(OrderItem.order_id == new_order_id).all()
        self.order_id_ent.state(["!disabled"])
        self.order_id_ent.delete(0, END)
        print(f"NEW order ID: {new_order_id}")
        self.order_id_ent.insert(0, new_order_id)
        print(f"New order id: {new_order_id}")
        self.order_id_ent.state(["disabled"])
        self.update_item_list_tree(order_items)
        self.order_save_update.set("Update Order")
        if self.is_paid.get():
            self.order_customer_cbx.state(["disabled"])
            self.order_description_ent.state(["disabled"])
            self.order_date_ent.state(["disabled"])
            self.order_paid_chk.state(["!disabled"])
            self.order_paid_chk.invoke()
            self.order_paid_chk.state(["disabled"])
            self.order_input_product_cbx.state(["disabled"])
            self.order_input_description_ent.state(["disabled"])
            self.order_input_quantity_spx.state(["disabled"])
            self.order_input_add_btn.state(["disabled"])
            self.order_save_update_btn.state(["disabled"])
            self.clear_order_items_btn.state(["!disabled"])
            self.reset_order_btn.state(["!disabled"])
            self.order_input_delete_btn.state(["disabled"])
        success_message = messagebox.showinfo(
            message='Order was successfully created!',
            title='Success'
        )
        return success_message    
        
    
    def update_order(self):
        order_id = self.order_id_ent.get()
        description = self.order_description_ent.get()
        is_paid = self.is_paid.get()
        notes = self.order_notes_txt.get("1.0", END)
        try:
            db.update_order(
                self.session,
                pk=order_id,
                description=description,
                is_paid=is_paid, 
                notes=notes)
        except Exception as e:
            error_message = messagebox.showerror(
            message="Oops! Order update encountered an error.",
            detail=e,
            title='Error'
        )
            return error_message 
        if self.order_items_tree.get_children(): # If there are items on the list
            items = []
            item_ids = set()
            old_items = self.session.query(OrderItem).filter(OrderItem.order_id==order_id).all()
            print(f"Old ites: {old_items}")
            old_item_ids = [item.order_item_id for item in old_items]
            for item in self.order_items_tree.get_children():
                items.append(self.order_items_tree.item(item))
                item_ids.add(self.order_items_tree.item(item)["values"][1])
            for item in items:
                if not item["values"][1]: # If it's new item (has no id)
                    print(f"New order item: {item}")
                    try:
                        db.add_order_item(
                            self.session,
                            order_id=order_id,
                            product_id=item["values"][0],
                            quantity=item["values"][4],
                            description=item["values"][3]
                        )
                    except Exception as e:
                        error_message = messagebox.showerror(
                            message="Error adding item",
                            detail=e,
                            title='Error'
                        )
                        return error_message
                else:
                    try:
                        db.update_order_item(
                            self.session, 
                            pk=item["values"][1],
                            quantity=item["values"][4],
                            description=item["values"][3]
                        )
                    except Exception as e:
                        error_message = messagebox.showerror(
                            message="Oops! Some items could not be updated.",
                            detail=e,
                            title='Error'
                        )
                        return error_message
            for id in old_item_ids:
                if id not in item_ids:
                    db.delete_order_item(self.session, pk=id)
            order_items = self.session.query(Product, OrderItem).join(OrderItem).filter(OrderItem.order_id == order_id).all()
            self.update_item_list_tree(order_items)
            self.order_save_update.set("Update Order")
            if self.is_paid.get():
                self.order_customer_cbx.state(["disabled"])
                self.order_description_ent.state(["disabled"])
                self.order_date_ent.state(["disabled"])
                self.order_paid_chk.state(["disabled"])
                self.order_input_product_cbx.state(["disabled"])
                self.order_input_description_ent.state(["disabled"])
                self.order_input_quantity_spx.state(["disabled"])
                self.order_input_add_btn.state(["disabled"])
                self.order_save_update_btn.state(["disabled"])
                self.clear_order_items_btn.state(["!disabled"])
                self.reset_order_btn.state(["!disabled"])
                self.order_input_delete_btn.state(["disabled"])
            success_message = messagebox.showinfo(
                message='Order was successfully updated!',
                title='Success'
            )
            return success_message
    
    def create_or_update_order(self):
        if self.is_paid.get():
            if not messagebox.askyesno(
                message='Paid orders cannot be edited after saving. Do you want to continue saving this order?',
                icon='question',
                title='Save Order'
            ):
                return
        order_id = self.order_id_ent.get()
        if order_id == "New":
            self.create_order()
        else:
            self.update_order()

    def populate_fields(self, order):
        """Populate order detail fields with the currect order details"""
        order_id = order.order_id
        order_items = self.session.query(Product, OrderItem).join(OrderItem).filter(OrderItem.order_id == order_id).all()
        self.reset_order_input_fields()
        self.order_id_ent.state(["!disabled"])
        self.order_id_ent.delete(0, END)
        self.order_id_ent.insert(0, order_id)
        self.order_id_ent.state(["disabled"])
        self.order_customer_cbx.state(["!disabled"])
        self.order_customer_cbx.delete(0, END)
        self.order_customer_cbx.set(order.customer_id)
        self.order_customer_cbx.state(["disabled"])
        self.order_description_ent.state(["!disabled"])
        self.order_description_ent.delete(0, END)
        self.order_description_ent.insert(0, order.description)
        self.order_date_ent.state(["!disabled"])
        self.order_date_ent.delete(0, END)
        self.order_date_ent.insert(0, str(order.order_date).replace("-", "/"))
        self.order_date_ent.state(["disabled"])
        self.order_paid_chk.state(["!disabled"])
        self.is_paid.set(value=order.is_paid)
        self.order_notes_txt.delete("1.0", END)
        self.order_notes_txt.insert("1.0", order.notes)
        self.order_input_product_cbx.state(["!disabled"])
        self.order_input_description_ent.state(["!disabled"])
        self.order_input_quantity_spx.state(["!disabled"])
        self.order_save_update_btn.state(["!disabled"])
        self.clear_order_items_btn.state(["!disabled"])
        self.reset_order_btn.state(["!disabled"])
        self.order_input_add_btn.state(["!disabled"])
        if order.is_paid:
            self.order_customer_cbx.state(["disabled"])
            self.order_description_ent.state(["disabled"])
            self.order_date_ent.state(["disabled"])
            self.order_paid_chk.state(["disabled"])
            self.order_input_product_cbx.state(["disabled"])
            self.order_input_description_ent.state(["disabled"])
            self.order_input_quantity_spx.state(["disabled"])
            self.order_input_add_btn.state(["disabled"])
            self.order_save_update_btn.state(["disabled"])
            self.clear_order_items_btn.state(["disabled"])
            self.reset_order_btn.state(["disabled"])
            self.order_input_delete_btn.state(["disabled"])
        self.update_item_list_tree(order_items)
        self.order_save_update.set("Update Order")

    def clear_order_items(self):
        """Clear all order items from the treeview"""
        order_amount = Money("0.00", NAD)
        for item in self.order_items_tree.get_children():
            self.order_items_tree.delete(item)
        self.order_amount.set(f"Total Cost:\tN${order_amount.amount}")

    def reset_order(self):
        """Reset the current active order to the last saved state"""
        order_id = self.order_id_ent.get()
        if order_id == "New":
            messagebox.showerror(
                message='An unsaved order cannot be reset!',
                title='Info'
            )
            return
        order = db.get_orders(self.session, pk=order_id)
        self.populate_fields(order)

    def reuse_order(self):
        """Generate a new order from the active order"""
        order_id = self.order_id_ent.get()
        if order_id == "New":
            messagebox.showerror(
                message='An unsaved order cannot be reused!',
                title='Info'
            )
            return
        order = db.get_orders(self.session, pk=order_id)
        order_items = self.session.query(Product, OrderItem).join(OrderItem).filter(OrderItem.order_id == order_id).all()
        self.open_blank_order_form()
        self.order_customer_cbx.state(["!disabled"])
        self.order_description_ent.insert(0, order.description)
        self.is_paid.set(value=order.is_paid)
        self.order_notes_txt.insert("1.0", order.notes)
        self.update_item_list_tree(order_items)

    def update_item_list_tree(self, order_items):
        order_amount = Money("0.00", NAD)
        for item in self.order_items_tree.get_children():
            self.order_items_tree.delete(item)
        for product,item in order_items:
            unit_price = Money(product.price, NAD)
            total_price = unit_price*item.quantity
            self.order_items_tree.insert('', 'end', iid=f"{product.product_id}",
                values=(
                    product.product_id,
                    item.order_item_id,
                    product.product_name,
                    item.description,
                    item.quantity,
                    unit_price.amount,
                    total_price.amount
                    )
                )
            order_amount += total_price
        self.order_amount.set(f"Total Cost:\tN${order_amount.amount}")

    def reset_order_input_fields(self):
        self.order_input_product_cbx.set("")
        self.order_input_description_ent.delete(0,END)
        self.order_input_quantity_spx.delete(0,END)