from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from quote_invoice.db import operations as db

class ProductDetailsTab():
    def __init__(self, notebook, parent_frame, session):
        """Configure the products and services form tab"""
        self.notebook =notebook
        self.session = session
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
            text="Products & Services",
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0, sticky=(N, S, W, E))
        #-------------------------------TOP FRAME ENDS--------------------------------------#

        #-------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(
            parent_frame,
            borderwidth=5, 
            # relief="solid"
        )
        self.mid_frame.grid(column=0, row=1, columnspan=2, sticky=(S, N, W, E))

        # Entries:
        self.search_ent = ttk.Entry(
            self.mid_frame,
        )
        self.search_ent.grid(column=10, row=2, pady=2, padx=2, sticky=(S, N, W, E))

        # Comboboxes
        self.search_option_cbx = ttk.Combobox(
            self.mid_frame,
            width=38,
            values=("Product ID", "SKU", "Barcode", "Product Name"),
        )
        self.search_option_cbx.grid(column=9, row=2, pady=2, padx=2, sticky=(S, N, E))

        # Buttons:

        self.search_btn = ttk.Button(
            self.mid_frame, 
            text="Search Product",
            style="btns.TButton",
            padding=(10, 21),
            command=self.search_product
        )
        self.search_btn.grid(column=11, row=2, pady=2, padx=2, sticky=(S, N, W, E))

         # Treeviews:
        self.products_tree = ttk.Treeview(self.mid_frame, show='headings', height=10)
        self.products_tree.bind('<ButtonRelease-1>', self.select_record)
        # Define Our Columns
        self.products_tree['columns'] = (
            "ID", # product_id
            "SKU",
            "Barcode",
            "Product Name",
            "Description",
            "Price",
            "Quantity", 
            "Taxable"
        )

        self.products_tree['displaycolumns'] = (
            "ID", # product_id
            "SKU",
            "Barcode",
            "Product Name",
            "Description",
            "Price",
            "Quantity", 
            "Taxable"
        )

        # Format Our Columns
        self.products_tree.column("ID", width=50, anchor=CENTER)
        self.products_tree.column("SKU", width=100, anchor=CENTER)
        self.products_tree.column("Barcode", width=100, anchor=CENTER)
        self.products_tree.column("Product Name", width=200, anchor=W)
        self.products_tree.column("Description", width=600, anchor=W)
        self.products_tree.column("Price", width=100, anchor=E)
        self.products_tree.column("Quantity", width=100, anchor=CENTER)
        self.products_tree.column("Taxable", width=50, anchor=CENTER)

        # Create Headings
        self.products_tree.heading("ID", text="ID", anchor=CENTER)
        self.products_tree.heading("SKU", text="SKU", anchor=CENTER)
        self.products_tree.heading("Barcode", text="Barcode", anchor=CENTER)
        self.products_tree.heading("Product Name", text="Product Name", anchor=W)
        self.products_tree.heading("Description", text="Description", anchor=W)
        self.products_tree.heading("Price", text="Unit Price", anchor=E)
        self.products_tree.heading("Quantity", text="In Stock", anchor=CENTER)
        self.products_tree.heading("Taxable", text="Taxable", anchor=CENTER)
        self.products_tree.grid(column=0, columnspan=12, row=0, sticky=(N, S, W, E))
        
        # Scrollbars:
        y_scroll = ttk.Scrollbar(self.mid_frame, orient=VERTICAL, command=self.products_tree.yview)
        x_scroll = ttk.Scrollbar(self.mid_frame, orient=HORIZONTAL, command=self.products_tree.xview)
        y_scroll.grid(column=12, row=0, sticky=(N, S))
        x_scroll.grid(column=0, columnspan=12, row=1, sticky=(E, W))
        self.products_tree['yscrollcommand'] = y_scroll.set
        self.products_tree['xscrollcommand'] = x_scroll.set

        #-------------------------------MID FRAME ENDS--------------------------------------#

        #-------------------------------BOTTOM FRAME----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            parent_frame, 
            borderwidth=5, 
            relief="solid"
        )
        self.bottom_frame.grid(column=0, row=2, columnspan=3, sticky=(N, W, E, S))
        self.bottom_frame.columnconfigure(0, weight=5)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=1)
        self.bottom_frame.columnconfigure(3, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        self.bottom_frame.rowconfigure(2, weight=1)
        self.bottom_frame.rowconfigure(3, weight=1)
        self.bottom_frame.rowconfigure(4, weight=1)
        self.bottom_frame.rowconfigure(5, weight=1)
        self.bottom_frame.rowconfigure(6, weight=1)
        self.bottom_frame.rowconfigure(7, weight=1)
        self.bottom_frame.rowconfigure(8, weight=1)
        self.bottom_frame.rowconfigure(9, weight=1)
        self.bottom_frame.rowconfigure(10, weight=1)
        self.bottom_frame.rowconfigure(11, weight=1)
        self.bottom_frame.rowconfigure(12, weight=1)

        for child in self.bottom_frame.winfo_children():
            child.grid_configure(padx=2, pady=5)

        # Labels:
        self.id_lbl = ttk.Label(
            self.bottom_frame,
            text="Product ID",
            anchor=W,
            style="txt.TLabel",
        )
        self.id_lbl.grid(column=0, row=0, sticky=(W, ))

        self.sku_lbl = ttk.Label(
            self.bottom_frame,
            text="SKU",
            anchor=W,
            style="txt.TLabel",
        )
        self.sku_lbl.grid(column=0, row=1, sticky=(W, ))

        self.barcode_lbl = ttk.Label(
            self.bottom_frame,
            text="Barcode",
            anchor=W,
            style="txt.TLabel",
        )
        self.barcode_lbl.grid(column=0, row=2, sticky=(W, ))

        self.product_name_lbl = ttk.Label(
            self.bottom_frame,
            text="Product Name",
            anchor=W,
            style="txt.TLabel",
        )
        self.product_name_lbl.grid(column=0, row=3, sticky=(W, ))

        self.description_lbl = ttk.Label(
            self.bottom_frame,
            text="Description",
            anchor=W,
            style="txt.TLabel",
        )
        self.description_lbl.grid(column=0, row=4, sticky=(W, ))

        self.price_lbl = ttk.Label(
            self.bottom_frame,
            text="Price",
            anchor=W,
            style="txt.TLabel",
        )
        self.price_lbl.grid(column=0, row=5, sticky=(W, ))

        self.quantity_lbl = ttk.Label(
            self.bottom_frame,
            text="Quantity",
            anchor=W,
            style="txt.TLabel",
        )
        self.quantity_lbl.grid(column=0, row=6, sticky=(W, ))

        self.is_taxable_lbl = ttk.Label(
            self.bottom_frame,
            text="Taxable",
            anchor=W,
            style="txt.TLabel",
        )
        self.is_taxable_lbl.grid(column=0, row=7, sticky=(W, ))

        # Entries:
        self.id_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            style="txt.TEntry",
        )
        self.id_ent.insert(0, "New")
        self.id_ent.state(["disabled"])
        self.id_ent.grid(column=1, columnspan=2, row=0, sticky=(N, S, E, W))

        self.sku_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            style="txt.TEntry",
        )
        self.sku_ent.grid(column=1, columnspan=2, row=1, sticky=(N, S, E, W))

        self.barcode_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            style="txt.TEntry",
        )
        self.barcode_ent.grid(column=1, columnspan=2, row=2, sticky=(N, S, E, W))

        self.product_name_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            style="txt.TEntry",
        )
        self.product_name_ent.grid(column=1, columnspan=2, row=3, sticky=(N, S, E, W))

        self.description_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            style="txt.TEntry",
        )
        self.description_ent.grid(column=1, columnspan=2, row=4, sticky=(N, S, E, W))

        self.price_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            style="txt.TEntry",
        )
        self.price_ent.grid(column=1, columnspan=2, row=5, sticky=(N, S, E, W))

        self.quantity_ent = ttk.Entry(
            self.bottom_frame,
            width=40,
            # textvariable="",
            # anchor="",
            style="txt.TEntry",
        )
        self.quantity_ent.grid(column=1, columnspan=2, row=6, sticky=(N, S, E, W))

        # Checkboxes
        self.is_taxable =  BooleanVar()
        self.is_taxable_chk = ttk.Checkbutton(
            self.bottom_frame,
            # text='Taxable',
            variable=self.is_taxable,
            onvalue=1,
            offvalue=0
            # style="heading.TLabel",
        )
        self.is_taxable_chk.grid(column=1, row=7, sticky=(N, S, E, W))

        # Buttons:
        self.save_btn = ttk.Button(
            self.bottom_frame,
            text="Save Product",
            style="btns.TButton",
            padding=5,
            command=self.create_or_update_product
        )
        self.save_btn.grid(column=3, row=0, rowspan=2, sticky=(N, S, E, W))

        self.new_product_btn = ttk.Button(
            self.bottom_frame,
            text="New Product",
            style="btns.TButton",
            padding=5,
            command=self.open_blank_product_form
        )
        self.new_product_btn.grid(column=3, row=2, rowspan=2, sticky=(N, S, E, W))
        
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#
        self.open_blank_product_form()
        self.update_item_list_tree()

    def update_item_list_tree(self, query=None):
        """Update products treeview with items from the database"""
        if query:
            products = query
        else:
            products = db.get_products(self.session)
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        for product in products:
            self.products_tree.insert('', 'end', iid=f"{product.product_id}",
                values=(
                    product.product_id,
                    product.sku,
                    product.barcode,
                    product.product_name,
                    product.description,
                    f"N${product.price}",
                    product.quantity,
                    # product.taxable
                    )
                )

    def select_record(self, event):
        record = self.products_tree.focus()
        selected_item = self.products_tree.item(record)
        product = db.get_products(self.session, pk=selected_item['values'][0])
        self.populate_fields(product)

    def open_blank_product_form(self):
        self.update_item_list_tree()
        self.id_ent.state(["!disabled"])
        self.id_ent.delete(0, END)
        self.id_ent.insert(0, "New")
        self.id_ent.state(["disabled"])
        self.sku_ent.delete(0, END)
        self.barcode_ent.delete(0, END)
        self.product_name_ent.delete(0, END)
        self.description_ent.delete(0, END)
        self.price_ent.delete(0, END)
        self.quantity_ent.delete(0, END)
        self.is_taxable.set(value=1)
        self.is_taxable_chk.state(["disabled"])
        self.save_btn.configure(text="Save Product")
        # self.disable_buttons()

    def create_or_update_product(self):
        product_id = self.id_ent.get()
        if product_id == "New":
            try:
                db.add_product(
                self.session, 
                sku=self.sku_ent.get(),
                barcode=self.barcode_ent.get(), 
                product_name=self.product_name_ent.get(), 
                description=self.description_ent.get(), 
                price=self.price_ent.get(), 
                quantity=self.quantity_ent.get(), 
                # is_taxable=self.is_taxable.get()
            )
                self.open_blank_product_form()
                success_message = messagebox.showinfo(
                message='New product was successfully added!',
                title='Success'
            )
                return success_message
            except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! An error occurred while adding the product.",
                detail=e,
                title='Error'
            )
                return error_message
        else:
            try:
                product = db.get_products(self.session, product_id)
                db.update_product(
                    self.session,
                    pk=product.product_id,
                    sku=self.sku_ent.get(),
                    barcode=self.barcode_ent.get(), 
                    product_name=self.product_name_ent.get(), 
                    description=self.description_ent.get(), 
                    price=self.price_ent.get(), 
                    quantity=self.quantity_ent.get(), 
                    # is_taxable=self.is_taxable.get()
                )
                self.open_blank_product_form()
                success_message = messagebox.showinfo(
                message='Product was successfully updated!',
                title='Success'
            )
                return success_message
            except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! An error occured while updating the product.",
                detail=e,
                title='Error'
            )
                return error_message 
            
    def populate_fields(self, product):
        self.id_ent.state(["!disabled"])
        self.id_ent.delete(0, END)
        self.id_ent.insert(0, product.product_id)
        self.id_ent.state(["disabled"])
        self.sku_ent.delete(0, END)
        self.sku_ent.insert(0, product.sku)
        self.barcode_ent.delete(0, END)
        self.barcode_ent.insert(0, product.barcode)
        self.product_name_ent.delete(0, END)
        self.product_name_ent.insert(0, product.product_name)
        self.description_ent.delete(0, END)
        self.description_ent.insert(0, product.description)
        self.price_ent.delete(0, END)
        self.price_ent.insert(0, product.price)
        self.quantity_ent.delete(0, END)
        self.quantity_ent.insert(0, product.quantity)
        self.is_taxable.set(value=1)
        self.is_taxable_chk.state(["disabled"])
        self.save_btn.configure(text="Update Product")

    def search_product(self):
        search_option = self.search_option_cbx.get()
        search_value = self.search_ent.get()
        if search_option == "Product ID":
            self.search_by_product_id(search_value)
        elif search_option == "SKU":
            self.search_by_sku(search_value)
        elif search_option == "Barcode":
            self.search_by_barcode(search_value)
        else:
            self.search_by_product_name(search_value)
            
    def search_by_product_id(self, product_id=""):
        if not product_id:
            error_message = messagebox.showerror(
                message="Cannot search with a blank Product ID.",
                title='Error'
            )
            return error_message
        try:
            product_id = int(product_id)
        except ValueError as e:
            error_message = messagebox.showerror(
            message="Invalid Product ID.",
            detail="Please ensure that you entered an integer value for Product ID.",
            title='Error'
        )
            return error_message
        try:
            product = db.get_products(self.session, pk=product_id)
            if product:
                self.update_item_list_tree(query=[product])
            else:
                info_message = messagebox.showinfo(
                message=f"No record with Product ID {product_id} was found.",
                title='Info'
            )
                return info_message
        except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! An error occured while getting or listing the product",
                detail=e,
                title='Error'
            )
                return error_message
        
    def search_by_sku(self, sku=""):
        try:
            products = db.get_products(self.session, sku=sku)
            if not products:
                info_message = messagebox.showinfo(
                message=f"No record matching the search value was found.",
                title='Info'
            )
                return info_message
            self.update_item_list_tree(query=products)
        except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! An error occured while getting or listing products",
                detail=e,
                title='Error'
            )
                return error_message
        
    def search_by_barcode(self, barcode=""):
        try:
            products = db.get_products(self.session, barcode=barcode)
            if not products:
                info_message = messagebox.showinfo(
                message=f"No record matching the search value was found.",
                title='Info'
            )
                return info_message
            self.update_item_list_tree(query=products)
        except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! An error occured while getting or listing products",
                detail=e,
                title='Error'
            )
                return error_message
        
    def search_by_product_name(self, product_name=""):
        try:
            products = db.get_products(self.session, product_name=product_name)
            if not products:
                info_message = messagebox.showinfo(
                message=f"No record matching the search value was found.",
                title='Info'
            )
                return info_message
            self.update_item_list_tree(products)
        except Exception as e:
                error_message = messagebox.showerror(
                message="Oops! An error occured while getting or listing products",
                detail=e,
                title='Error'
            )
                return error_message