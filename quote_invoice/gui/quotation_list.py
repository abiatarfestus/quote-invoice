
class QuotationListTab():
    def __init__(self):
        # Frames
        top_frame = ttk.Frame(
            self.quotation_list_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.quotation_list_frame, 
            borderwidth=5, 
            relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.quotation_list_frame,
            borderwidth=5, 
            relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Quotation List",
            anchor="center",
            style="heading.TLabel",
        )

        heading_lbl.grid(row=0)

        # ENTRIES
        self.quote_search_ent = ttk.Entry(
            bottom_frame,
        )
        self.quote_search_ent.grid(column=3, row=1, sticky=(S, N, W, E))

        # COMBOBOXES
        
        self.quote_search_option_cbx = ttk.Combobox(
            bottom_frame,
            width=38,
            values=("Quote ID", "Customer ID", "Other Variables"),
        )
        self.quote_search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

        def select_record(event):
            # print("Record selected")
            record = tree.focus()
            self.selected_quotation = tree.item(record)
        
        def open_blank_quote_form():
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
            self.quote_notes_txt.delete("1.0", END)
            self.quote_input_product_cbx.state(["!disabled"])
            self.quote_input_description_ent.state(["!disabled"])
            self.quote_input_quantity_spx.state(["!disabled"])
            self.quote_input_add_btn.state(["!disabled"])
            self.quote_save_update_btn.state(["!disabled"])
            self.change_to_order_btn.state(["!disabled"])
            self.mark_closed_btn.state(["!disabled"])
            for item in self.quote_items_tree.get_children():
                self.quote_items_tree.delete(item)
            self.quote_amount.set("Total Cost:\tN$0.00")
            self.quote_save_update.set("Save Quotation")
            self.notebook.select(self.quotation_frame)
        
        def view_quotation():
            # print(f"SELECTED RECORD: {self.selected_quotation}")
            quotation = self.selected_quotation
            if not self.selected_quotation:
                error_message = messagebox.showerror(
                    message='No record is selected!',
                    title='Error'
                )
                return error_message
            # Get quote items from datatbase
            quote_id = quotation['values'][0]
            quote_amount = Money("0.00", NAD)
            quote_items = session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == quotation['values'][0]).all()
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
            self.notebook.select(self.quotation_frame)

        def search_quotation():
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
                        quotation = db.get_quotations(session, pk=quote_id)
                        if quotation:
                            for item in tree.get_children():
                                tree.delete(item)
                            tree.insert('', 'end', iid=f"{quotation.quote_id}",
                            values=(
                                f"{quotation.quote_id}",
                                customer_id_name_dict[quotation.customer_id],
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
                        quotations = db.get_quotations(session, customer_id=customer_id)
                        if quotations:
                            for item in tree.get_children():
                                tree.delete(item)
                            for quote in quotations:
                                tree.insert('', 'end', iid=f"{quote.quote_id}",
                                values=(
                                    f"{quote.quote_id}",
                                    customer_id_name_dict[quote.customer_id],
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
                    quotations = db.get_quotations(session, other_fields=search_value)
                    if not quotations:
                        info_message = messagebox.showinfo(
                            message="No matching record was found.",
                            title='Info'
                            )
                        return info_message
                    for item in tree.get_children():
                        tree.delete(item)
                    for quote in quotations:
                        tree.insert('', 'end', iid=f"{quote.quote_id}",
                        values=(
                            f"{quote.quote_id}",
                            customer_id_name_dict[quote.customer_id],
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




        # Buttons
        open_quotation_btn = ttk.Button(
            bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21,
            command=view_quotation
        )
        add_quotation_btn = ttk.Button(
            bottom_frame, 
            text="Add New Quotation",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=open_blank_quote_form
        )
        search_quotation_btn = ttk.Button(
            bottom_frame, 
            text="Search Quotation",
            # style="home_btns.TButton",
            padding=(10, 21),
            command=search_quotation
        )

        open_quotation_btn.grid(column=0, row=1, sticky=E)
        add_quotation_btn.grid(column=1, row=1, sticky=E)
        search_quotation_btn.grid(column=4, row=1, sticky=E)

        # Treeview
        tree = ttk.Treeview(mid_frame, show='headings', height=20)
        tree.bind('<ButtonRelease-1>', select_record)
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
        x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
        y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
        x_scroll.grid(column=0, row=1, sticky=(E, W))
        tree['yscrollcommand'] = y_scroll.set
        tree['xscrollcommand'] = x_scroll.set


        # Define Our Columns
        tree['columns'] = (
            "ID",
            "Customer",
            "Description",
            "Quote Date",
            "Accepted", 
            "Closed",
            "Notes"
        )

        tree['displaycolumns'] = (
            "ID",
            "Customer",
            "Description",
            "Quote Date",
            "Accepted", 
            "Closed"
        )

        # Format Our Columns
        tree.column("ID", anchor=CENTER)
        tree.column("Customer", anchor=W)
        tree.column("Description", anchor=W)
        tree.column("Quote Date", anchor=E)
        tree.column("Accepted", anchor=CENTER)
        tree.column("Closed", anchor=CENTER)
        tree.column("Notes", anchor=W)

        # Create Headings
        tree.heading("ID", text="ID", anchor=CENTER)
        tree.heading("Customer", text="Customer", anchor=W)
        tree.heading("Description", text="Description", anchor=W)
        tree.heading("Quote Date", text="Quote Date", anchor=E)
        tree.heading("Accepted", text="Accepted", anchor=CENTER)
        tree.heading("Closed", text="Closed", anchor=CENTER)
        tree.heading("Notes", text="Notes", anchor=W)

        customers = session.query(Customer).all()
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
        customer_id_name_dict = dict()
        for name in tuple(self.customers_dict):
            customer_id_name_dict.update({self.customers_dict[name][0]:name })
        # print(f"CUSTOMER_ID_NAME DICT: {customer_id_name_dict}")

        quotations = session.query(Quotation).order_by(Quotation.quote_date).all()
        # print(f"TOTAL QUOTATIONS: {len(quotations)}")
        for quote in quotations:
            tree.insert('', 'end', iid=f"{quote.quote_id}",
            values=(
                f"{quote.quote_id}",
                customer_id_name_dict[quote.customer_id],
                quote.description,
                quote.quote_date,
                quote.is_accepted,
                quote.is_closed,
                quote.notes
                )
            )

        tree.grid(column=0, row=0, sticky=(N, S, W, E))

        

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)