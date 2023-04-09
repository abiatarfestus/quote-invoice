# # from tkinter import *
# # from tkinter import ttk
# # from turtle import bgcolor


# # class MainWindow:
# #     def __init__(self, root):

# #         root.title("Quote & Invoice")

# #         self.top_frame = ttk.Frame(
# #             root,
# #             # padding="3 3 12 12",
# #             borderwidth=5,
# #             # relief="solid"
# #         )
# #         self.mid_frame = ttk.Frame(
# #             root,
# #             # padding="3 3 12 12",
# #             borderwidth=5,
# #             relief="solid"
# #         )
# #         self.bottom_frame = ttk.Frame(
# #             root,
# #             # padding="3 3 12 12",
# #             borderwidth=5,
# #             # relief="solid"
# #         )
# #         self.top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
# #         self.mid_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))
# #         self.bottom_frame.grid(column=0, row=4, columnspan=2, sticky=(N, W, E, S))
# #         root.columnconfigure(0, weight=1)
# #         root.columnconfigure(1, weight=1)
# #         root.rowconfigure(0, weight=1)
# #         root.rowconfigure(1, weight=1)
# #         root.rowconfigure(2, weight=1)
# #         root.rowconfigure(3, weight=1)
# #         root.rowconfigure(4, weight=1)

# #         # self.feet = StringVar()
# #         # feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
# #         # feet_entry.grid(column=2, row=1, sticky=(W, E))
# #         # self.meters = StringVar()

# #         # ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)
# #         # ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# #         # ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
# #         # ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)


# #         # Styles
# #         s = ttk.Style()
# #         s.configure("home_btns.TButton", font=(None, 24))
# #         s.configure("heading.TLabel", font=(None, 31))
# #         s.configure(
# #             "main_menu.TLabel",
# #             font=(None, 24),
# #             background="blue",
# #             foreground="white"
# #         )

# #         # LABELS
# #         # ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
# #         self.heading_lbl = ttk.Label(
# #             self.top_frame,
# #             text="Quote & Invoice v0.0.1",
# #             anchor="center",
# #             style="heading.TLabel",
# #         )

# #         self.main_menu_lbl = ttk.Label(
# #             self.mid_frame,
# #             text="Main Menu",
# #             anchor="center",
# #             style="main_menu.TLabel",
# #             padding=(180,2)
# #         )

# #         # Buttons
# #         self.customer_list_btn = ttk.Button(
# #             self.mid_frame,
# #             text="Customer List",
# #             style="home_btns.TButton",
# #             padding=26
# #         )
# #         self.customer_form_btn = ttk.Button(
# #             self.mid_frame,
# #             text="Customer Form",
# #             style="home_btns.TButton",
# #             padding=(15, 26)
# #         )
# #         self.quotations_btn = ttk.Button(
# #             self.mid_frame,
# #             text="Quotations",
# #             style="home_btns.TButton",
# #             padding=26
# #         )
# #         self.orders_invoies_btn = ttk.Button(
# #             self.mid_frame,
# #             text="Orders/Invoices",
# #             style="home_btns.TButton",
# #             padding=(15, 26)
# #         )

# #         # Placement
# #         self.heading_lbl.grid(row=0)
# #         self.main_menu_lbl.grid(column=0, row=0, columnspan=2)
# #         self.customer_list_btn.grid(column=0, row=1, sticky=E)
# #         self.customer_form_btn.grid(column=0, row=2, sticky=E)
# #         self.quotations_btn.grid(column=1, row=1, sticky=W)
# #         self.orders_invoies_btn.grid(column=1, row=2, sticky=W)

# #         self.top_frame.columnconfigure(0, weight=1)
# #         self.top_frame.rowconfigure(0, weight=1)

# #         self.mid_frame.columnconfigure(0, weight=1)
# #         self.mid_frame.columnconfigure(1, weight=1)
# #         self.mid_frame.rowconfigure(0, weight=1)
# #         self.mid_frame.rowconfigure(1, weight=1)
# #         # self.mid_frame.rowconfigure(2, weight=1)
# #         # self.mid_frame.rowconfigure(3, weight=1)
# #         # self.mid_frame.rowconfigure(4, weight=1)

# #         for child in self.mid_frame.winfo_children():
# #             child.grid_configure(padx=5, pady=5)

# #         # feet_entry.focus()
# #         # root.bind("<Return>", self.calculate)

# #     # def calculate(self, *args):
# #     #     try:
# #     #         value = float(self.feet.get())
# #     #         self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
# #     #     except ValueError:
# #     #         pass


# # from sqlalchemy import create_engine
# # from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# # # Global Variables
# # SQLITE                  = 'sqlite'
# # # MYSQL                   = 'mysql'
# # # POSTGRESQL              = 'postgresql'
# # # MICROSOFT_SQL_SERVER    = 'mssqlserver'

# # # Table Names
# # USERS           = 'users'
# # ADDRESSES       = 'addresses'


# # class MyDatabase:
# #     # http://docs.sqlalchemy.org/en/latest/core/engines.html
# #     DB_ENGINE = {
# #         SQLITE: 'sqlite:///{DB}',
# #         # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
# #         # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
# #         # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
# #     }

# #     # Main DB Connection Ref Obj
# #     db_engine = None

# #     def __init__(self, dbtype, username='', password='', dbname=''):
# #         dbtype = dbtype.lower()

# #         if dbtype in self.DB_ENGINE.keys():
# #             engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

# #             self.db_engine = create_engine(engine_url)
# #             print(self.db_engine)

# #         else:
# #             print("DBType is not found in DB_ENGINE")

# #     def create_db_tables(self):
# #         metadata = MetaData()
# #         users = Table(USERS, metadata,
# #                       Column('id', Integer, primary_key=True),
# #                       Column('first_name', String),
# #                       Column('last_name', String)
# #                       )

# #         address = Table(ADDRESSES, metadata,
# #                         Column('id', Integer, primary_key=True),
# #                         Column('user_id', None, ForeignKey('users.id')),
# #                         Column('email', String, nullable=False),
# #                         Column('address', String)
# #                         )

# #         try:
# #             metadata.create_all(self.db_engine)
# #             print("Tables created")
# #         except Exception as e:
# #             print("Error occurred during Table creation!")
# #             print(e)

# #     # Insert, Update, Delete
# #     def execute_query(self, query=''):
# #         if query == '' : return

# #         print (query)
# #         with self.db_engine.connect() as connection:
# #             try:
# #                 connection.execute(query)
# #             except Exception as e:
# #                 print(e)


# #     def print_all_data(self, table='', query=''):
# #         query = query if query != '' else "SELECT * FROM '{}';".format(table)
# #         print(query)

# #         with self.db_engine.connect() as connection:
# #             try:
# #                 result = connection.execute(query)
# #             except Exception as e:
# #                 print(e)
# #             else:
# #                 for row in result:
# #                     print(row) # print(row[0], row[1], row[2])
# #                 result.close()

# #         print("\n")

# #     # Examples

# #     def sample_query(self):
# #         # Sample Query
# #         query = "SELECT first_name, last_name FROM {TBL_USR} WHERE " \
# #                 "last_name LIKE 'M%';".format(TBL_USR=USERS)
# #         self.print_all_data(query=query)

# #         # Sample Query Joining
# #         query = "SELECT u.last_name as last_name, " \
# #                 "a.email as email, a.address as address " \
# #                 "FROM {TBL_USR} AS u " \
# #                 "LEFT JOIN {TBL_ADDR} as a " \
# #                 "WHERE u.id=a.user_id AND u.last_name LIKE 'M%';" \
# #             .format(TBL_USR=USERS, TBL_ADDR=ADDRESSES)
# #         self.print_all_data(query=query)

# #     def sample_delete(self):
# #         # Delete Data by Id
# #         query = "DELETE FROM {} WHERE id=3".format(USERS)
# #         self.execute_query(query)
# #         self.print_all_data(USERS)

# #         # Delete All Data
# #         '''
# #         query = "DELETE FROM {}".format(USERS)
# #         self.execute_query(query)
# #         self.print_all_data(USERS)
# #         '''

# #     def sample_insert(self):
# #         # Insert Data
# #         query = "INSERT INTO {}(id, first_name, last_name) " \
# #                 "VALUES (3, 'Terrence','Jordan');".format(USERS)
# #         self.execute_query(query)
# #         self.print_all_data(USERS)

# #     def sample_update(self):
# #         # Update Data
# #         query = "UPDATE {} set first_name='XXXX' WHERE id={id}"\
# #             .format(USERS, id=3)
# #         self.execute_query(query)
# #         self.print_all_data(USERS)


# # def setup_customer_list_tab(notebook, parent_frame, session):
# #         """Configure the customer list tab"""
# #         #-------------------------------------TOP FRAME-----------------------------------#
# #         # Frames:
# #         top_frame = ttk.Frame(
# #             parent_frame,
# #             borderwidth=5,
# #             relief="solid"
# #         )
# #         top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
# #         top_frame.columnconfigure(0, weight=1)
# #         top_frame.rowconfigure(0, weight=1)

# #         # Labels:
# #         heading_lbl = ttk.Label(
# #             top_frame,
# #             text="Customer List",
# #             anchor="center",
# #             style="heading.TLabel",
# #         )
# #         heading_lbl.grid(column=0, row=0, sticky=(S, N, W, E))
# #         #-------------------------------TOP FRAME ENDS--------------------------------------#

# #         #-------------------------------MID FRAME-------------------------------------------#
# #         # Frames:
# #         mid_frame = ttk.Frame(
# #             parent_frame,
# #             borderwidth=5,
# #             relief="solid"
# #         )
# #         mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
# #         mid_frame.columnconfigure(0, weight=1)
# #         mid_frame.columnconfigure(1, weight=1)
# #         mid_frame.rowconfigure(0, weight=1)
# #         mid_frame.rowconfigure(1, weight=1)

# #         # Treeviews:
# #         tree = ttk.Treeview(mid_frame, show='headings', height=20)
# #         tree.bind('<ButtonRelease-1>', select_record)

# #         # Define columns:
# #         tree["columns"] = (
# #             "ID",
# #             "Customer Type",
# #             "First Name",
# #             "Last Name",
# #             "Entity Name",
# #             "Customer Name",
# #             "Email",
# #             "Phone",
# #             "Address",
# #             "Town",
# #             "Country",
# #             "Customer Since",
# #             "Notes"
# #         )

# #         # Columns to display:
# #         tree["displaycolumns"] = (
# #             "ID",
# #             "Customer Name",
# #             "Town",
# #             "Phone",
# #             "Email",
# #             "Customer Since"
# #         )

# #         # Format columns:
# #         tree.column("ID", anchor=CENTER)
# #         tree.column("Customer Name", anchor=W)
# #         tree.column("Town", anchor=W)
# #         tree.column("Phone", anchor=W)
# #         tree.column("Email", anchor=W)
# #         tree.column("Customer Since", anchor=E)

# #         # Add headings:
# #         tree.heading("ID", text="ID", anchor=CENTER)
# #         tree.heading("Customer Name", text="Customer Name", anchor=W)
# #         tree.heading("Town", text="Town", anchor=W)
# #         tree.heading("Phone", text="Phone", anchor=W)
# #         tree.heading("Email", text="Email", anchor=W)
# #         tree.heading("Customer Since", text="Customr Since", anchor=E)

# #         # Insert the data in Treeview widget
# #         customers = session.query(Customer).order_by(Customer.customer_id).all()
# #         print(f"TOTAL CUSTOMERS: {len(customers)}")
# #         # for i in range(1, total_customers+1):
# #         for customer in customers:
# #             if customer.first_name and customer.last_name:
# #                 customer_name = f"{customer.last_name} {customer.first_name}"
# #             else:
# #                 customer_name = customer.entity_name
# #             tree.insert('', 'end', iid=f"{customer.customer_id}",
# #             values=(
# #                 f"{customer.customer_id}",
# #                 customer.customer_type,
# #                 customer.first_name,
# #                 customer.last_name,
# #                 customer.entity_name,
# #                 customer_name,
# #                 customer.email,
# #                 customer.phone,
# #                 customer.address,
# #                 customer.town,
# #                 customer.country,
# #                 customer.customer_since,
# #                 customer.notes
# #                 )
# #             )
# #         tree.grid(column=0, row=0, sticky=(N, S, W, E))

# #         # Scrollbars:
# #         y_scroll = ttk.Scrollbar(mid_frame, orient=VERTICAL, command=tree.yview)
# #         x_scroll = ttk.Scrollbar(mid_frame, orient=HORIZONTAL, command=tree.xview)
# #         y_scroll.grid(column=1, row=0, sticky=(N, S, W, E))
# #         x_scroll.grid(column=0, row=1, sticky=(E, W))
# #         tree['yscrollcommand'] = y_scroll.set
# #         tree['xscrollcommand'] = x_scroll.set
# #         #-------------------------------MID FRAME ENDS---------------------------------------#

# #         #-------------------------------BOTTOM FRAME-----------------------------------------#
# #         # Frames:
# #         bottom_frame = ttk.Frame(
# #             parent_frame,
# #             borderwidth=5,
# #             relief="solid"
# #         )
# #         bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

# #         # Entries:
# #         search_ent = ttk.Entry(
# #             bottom_frame,
# #         )
# #         search_ent.grid(column=3, row=1, sticky=(S, N, W, E))

# #         # Comboboxes:
# #         search_option_cbx = ttk.Combobox(
# #             bottom_frame,
# #             width=38,
# #             values=("Customer ID", "Other Variables"),
# #         )
# #         search_option_cbx.grid(column=2, row=1, padx=2, sticky=(S, N, W, E))

# #         # Buttons:
# #         open_customer_btn = ttk.Button(
# #             bottom_frame,
# #             text="Open Selected Record",
# #             # style="home_btns.TButton",
# #             padding=21,
# #             command=view_customer
# #         )
# #         add_customer_btn = ttk.Button(
# #             bottom_frame,
# #             text="Add New Customer",
# #             # style="home_btns.TButton",
# #             padding=(10, 21),
# #             command=open_blank_customer_form
# #         )
# #         search_customer_btn = ttk.Button(
# #             bottom_frame,
# #             text="Search Customer",
# #             # style="home_btns.TButton",
# #             padding=(10, 21),
# #             command=search_customer
# #         )
# #         open_customer_btn.grid(column=0, row=1, sticky=E)
# #         add_customer_btn.grid(column=1, row=1, sticky=E)
# #         search_customer_btn.grid(column=4, row=1, sticky=E)
# #         #-------------------------------BOTTOM FRAME ENDS------------------------------------#

# #         selected_customer = None

# #         def select_record(event):
# #             global selected_customer
# #             print("Record selected")
# #             record = tree.focus()
# #             selected_customer = tree.item(record)

# #         def open_blank_customer_form():
# #             customer_details.new_customer()
# #         #     id_ent.state(["!disabled"])
# #         #     id_ent.delete(0, END)
# #         #     id_ent.insert(0, "New")
# #         #     id_ent.state(["disabled"])
# #         #     type_cbx.set("")
# #         #     first_name_ent.delete(0, END)
# #         #     last_name_ent.delete(0, END)
# #         #     entity_ent.delete(0, END)
# #         #     email_ent.delete(0, END)
# #         #     phone_ent.delete(0, END)
# #         #     address_ent.delete(0, END)
# #         #     town_ent.delete(0, END)
# #         #     country_ent.delete(0, END)
# #         #     since_ent.delete(0, END)
# #         #     notes_txt.delete("1.0", END)
# #             notebook.select(customer_frame)

# #         def view_customer():
# #             print(f"SELECTED RECORD: {selected_customer}")
# #             customer = selected_customer
# #             if not selected_customer:
# #                 error_message = messagebox.showerror(
# #                     message='No record is selected!',
# #                     title='Error'
# #                 )
# #                 return error_message
# #             customer_details.populate(customer)
# #             # id_ent.state(["!disabled"])
# #             # id_ent.delete(0, END)
# #             # id_ent.insert(0, customer['values'][0])
# #             # id_ent.state(["disabled"])
# #             # type_cbx.set(customer['values'][1])
# #             # first_name_ent.delete(0, END)
# #             # first_name_ent.insert(0, customer['values'][2])
# #             # last_name_ent.delete(0, END)
# #             # last_name_ent.insert(0, customer['values'][3])
# #             # entity_ent.delete(0, END)
# #             # entity_ent.insert(0, customer['values'][4])
# #             # email_ent.delete(0, END)
# #             # email_ent.insert(0, customer['values'][6])
# #             # phone_ent.delete(0, END)
# #             # phone_ent.insert(0, customer['values'][7])
# #             # address_ent.delete(0, END)
# #             # address_ent.insert(0, customer['values'][8])
# #             # town_ent.delete(0, END)
# #             # town_ent.insert(0, customer['values'][9])
# #             # country_ent.delete(0, END)
# #             # country_ent.insert(0, customer['values'][10])
# #             # since_ent.delete(0, END)
# #             # since_ent.insert(0, customer['values'][11])
# #             # notes_txt.delete("1.0", END)
# #             # notes_txt.insert("1.0", customer['values'][12])
# #             notebook.select(customer_frame)

# #         def search_customer(session):
# #             search_option = search_option_cbx.get()
# #             search_value = search_ent.get()
# #             if search_option == "Customer ID":
# #                 customer_id = search_value
# #                 if not customer_id:
# #                     error_message = messagebox.showerror(
# #                         message="Cannot search with blank Customer ID.",
# #                         title='Error'
# #                     )
# #                     return error_message
# #                 try:
# #                     customer_id = int(customer_id)
# #                     try:
# #                         customer = db.get_customers(session, pk=customer_id)
# #                         if customer:
# #                             if customer.first_name and customer.last_name:
# #                                 customer_name = f"{customer.last_name} {customer.first_name}"
# #                             else:
# #                                 customer_name = customer.entity_name
# #                             for item in tree.get_children():
# #                                 tree.delete(item)
# #                             tree.insert('', 'end', iid=f"{customer.customer_id}",
# #                             values=(
# #                                 f"{customer.customer_id}",
# #                                 customer.customer_type,
# #                                 customer.first_name,
# #                                 customer.last_name,
# #                                 customer.entity_name,
# #                                 customer_name,
# #                                 customer.email,
# #                                 customer.phone,
# #                                 customer.address,
# #                                 customer.town,
# #                                 customer.country,
# #                                 customer.customer_since,
# #                                 customer.notes
# #                                 )
# #                             )
# #                         else:
# #                             info_message = messagebox.showinfo(
# #                             message="No matching record was found.",
# #                             title='Info'
# #                         )
# #                             return info_message
# #                     except Exception as e:
# #                             error_message = messagebox.showerror(
# #                             message="Oops! Something went wrong.",
# #                             detail=e,
# #                             title='Error'
# #                         )
# #                             return error_message
# #                 except Exception as e:
# #                     error_message = messagebox.showerror(
# #                     message="Invalid Customer ID.",
# #                     detail=e,
# #                     title='Error'
# #                 )
# #                     return error_message
# #             else:
# #                 try:
# #                     customers = db.get_customers(session, other_fields=search_value)
# #                     if not customers:
# #                         info_message = messagebox.showinfo(
# #                             message="No matching record was found.",
# #                             title='Info'
# #                             )
# #                         return info_message
# #                     for item in tree.get_children():
# #                         tree.delete(item)
# #                     for customer in customers:
# #                         if customer.first_name and customer.last_name:
# #                             customer_name = f"{customer.last_name} {customer.first_name}"
# #                         else:
# #                             customer_name = customer.entity_name
# #                         tree.insert('', 'end', iid=f"{customer.customer_id}",
# #                         values=(
# #                             f"{customer.customer_id}",
# #                             customer.customer_type,
# #                             customer.first_name,
# #                             customer.last_name,
# #                             customer.entity_name,
# #                             customer_name,
# #                             customer.email,
# #                             customer.phone,
# #                             customer.address,
# #                             customer.town,
# #                             customer.country,
# #                             customer.customer_since,
# #                             customer.notes
# #                             )
# #                         )
# #                 except Exception as e:
# #                     error_message = messagebox.showerror(
# #                     message="Oops! Something went wrong.",
# #                     detail=e,
# #                     title='Error'
# #                 )
# #                     return error_message


# # def update_order(self):
# #         order_id = self.order_id_ent.get()
# #         try:
# #             order_date=datetime.strptime(self.order_date_ent.get(), '%Y/%m/%d').date()
# #         except Exception as e:
# #             error_message = messagebox.showerror(
# #             message="Invalid date entered.",
# #             detail=e,
# #             title='Error'
# #         )
# #             return error_message
# #         # try:
# #         #     customer_id = self.customers_dict[self.order_customer_cbx.get()][0]
# #         # except Exception as e:
# #         #     error_message = messagebox.showerror(
# #         #     message="Invalid customer entered.",
# #         #     detail=e,
# #         #     title='Error'
# #         # )
# #         #     return error_message
# #         description = self.order_description_ent.get()
# #         is_paid = self.is_paid.get()
# #         notes = self.order_notes_txt.get("1.0", END)
# #         try:
# #             db.update_order(
# #                 self.session,
# #                 pk=order_id,
# #                 # order_date=order_date,
# #                 description=description,
# #                 # customer_id=customer_id,
# #                 is_paid=is_paid,
# #                 notes=notes)
# #         except Exception as e:
# #             error_message = messagebox.showerror(
# #             message="Oops! Order update encountered an error.",
# #             detail=e,
# #             title='Error'
# #         )
# #             return error_message
# #         if self.order_items_tree.get_children(): # If there are items on the list
# #             items = []
# #             item_ids = set()
# #             old_items = self.session.query(OrderItem).filter(OrderItem.order_id==order_id).all()
# #             old_item_ids = [item.order_item_id for item in old_items]
# #             for item in self.order_items_tree.get_children():
# #                 items.append(self.order_items_tree.item(item))
# #                 item_ids.add(self.order_items_tree.item(item)["values"][1])
# #             # print(f"ITEM IDs: {item_ids}")
# #             # print(f"OLD ITEM IDs: {old_item_ids}")
# #             for item in items:
# #                 if not item["values"][1]: # If it's new item (has no id)
# #                     db.add_order_item(
# #                         self.session,
# #                         order_id=order_id,
# #                         product_id=item["values"][0],
# #                         quantity=item["values"][4],
# #                         description=item["values"][3]
# #                     )
# #                 else:
# #                     try:
# #                         db.update_order_item(
# #                             self.session,
# #                             pk=item["values"][1],
# #                             quantity=item["values"][4],
# #                             description=item["values"][3]
# #                         )
# #                     except Exception as e:
# #                         error_message = messagebox.showerror(
# #                             message="Oops! Some items could not be updated.",
# #                             detail=e,
# #                             title='Error'
# #                         )
# #                         return error_message
# #             for id in old_item_ids:
# #                 if id not in item_ids:
# #                     db.delete_order_item(self.session, pk=id)
# #             # Update item list
# #             order_items = self.session.query(Product, OrderItem).join(OrderItem).filter(OrderItem.order_id == order_id).all()
# #             order_amount = Money("0.00", NAD)
# #             for item in self.order_items_tree.get_children():
# #                 self.order_items_tree.delete(item)
# #             for product,item in order_items:
# #                 unit_price = Money(product.price, NAD)
# #                 total_price = unit_price*item.quantity
# #                 self.order_items_tree.insert('', 'end', iid=f"{product.product_id}",
# #                     values=(
# #                         product.product_id,
# #                         item.order_item_id,
# #                         product.product_name,
# #                         item.description,
# #                         item.quantity,
# #                         unit_price.amount,
# #                         total_price.amount
# #                         )
# #                     )
# #                 order_amount += total_price
# #             self.order_amount.set(f"Total Cost:\tN${order_amount.amount}")
# #             self.order_save_update.set("Update Order")
# #             # self.notebook.select(self.order_frame)
# #             if self.is_paid.get(): # or order['values'][5] == "True":
# #                 self.order_customer_cbx.state(["disabled"])
# #                 self.order_description_ent.state(["disabled"])
# #                 self.order_date_ent.state(["disabled"])
# #                 # self.order_paid_chk.state(["!disabled"])
# #                 # self.order_paid_chk.invoke()
# #                 self.order_paid_chk.state(["disabled"])
# #                 self.order_input_product_cbx.state(["disabled"])
# #                 self.order_input_description_ent.state(["disabled"])
# #                 self.order_input_quantity_spx.state(["disabled"])
# #                 self.order_input_add_btn.state(["disabled"])
# #                 self.order_save_update_btn.state(["disabled"])
# #                 self.change_to_order_btn.state(["disabled"])
# #                 # self.mark_closed_btn.state(["disabled"])
# #                 self.order_input_delete_btn.state(["disabled"])
# #             success_message = messagebox.showinfo(
# #                 message='Order was successfully updated!',
# #                 title='Success'
# #             )
# #             return success_message

# # admin_user = session.query(User).filter_by(is_admin=True ).first()
# #     if is_admin: # Check if a staff user is being changed to admin
# #         if pk != admin_user.user_id:
# #             raise Exception("An Admin user already exist. This version does not support change a user from staff to admin.")

# Initializer
# from tkinter import *
# from tkinter import ttk
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# # from quote_invoice.data import db_data
# from .home import HomeTab
# from .login import UserAuthentication
# from .customer_list import CustomerListTab
# from .quotation_list import QuotationListTab
# from .customer_details import CustomerDetailsTab
# from .product_details import ProductDetailsTab
# from .quote_details import QuoteDetailsTab
# from .order_list import OrderListTab
# from .style import style
# from .order_details import OrderDetailsTab
# from quote_invoice.common.constants import DB_PATH, LOGO_PATH

# def get_connection():
#     return create_engine(DB_PATH)

# # class DatabaseOps():
# engine = get_connection()
# Session = sessionmaker()
# Session.configure(bind=engine)
# session = Session()


# class Window():
#     """ Initialize the main window of the application"""
#     def __init__(self, root):
#         self.root = root
#         self.is_authenticated = False
#         self.authenticated_user = None
#         self.authenticated_user_name = "Logged Out"
#         self.root.title("Quote & Invoice")
#         self.root.option_add('*tearOff', FALSE)
#         self.selected_customer = None
#         self.selected_quotation = None
#         self.selected_order = None
#         self.selected_quote = None
#         self.selected_order = None
#         self.logo = PhotoImage(file=LOGO_PATH)
#         self.root.iconphoto(False, self.logo)
#         self.style = style()
#         self.create_notebook()
#         self.configure_rows_columns()
#         self.home_tab = self.setup_home_tab()
#         self.order_details_tab = self.setup_order_tab()
#         self.order_list_tab = self.setup_order_list_tab()
#         self.quote_details_tab = self.setup_quote_tab()
#         self.quotation_list_tab = self.setup_quotation_list_tab()
#         self.customer_details_tab = self.setup_customer_tab()
#         self.customer_list_tab = self.setup_customer_list_tab()
#         self.product_details_tab = self.setup_product_tab()
#         if not self.is_authenticated:
#             user = UserAuthentication(self.root, DB_PATH)


#     def create_notebook(self):
#         """Create a Notebook and Frames"""
#         self.notebook = ttk.Notebook(self.root, style="notebook.TNotebook",)
#         self.home_frame = ttk.Frame(self.notebook)
#         self.customer_list_frame = ttk.Frame(self.notebook)
#         self.customer_frame = ttk.Frame(self.notebook)
#         self.quotation_list_frame = ttk.Frame(self.notebook)
#         self.quotation_frame = ttk.Frame(self.notebook)
#         self.order_list_frame = ttk.Frame(self.notebook)
#         self.order_frame = ttk.Frame(self.notebook)
#         self.product_frame = ttk.Frame(self.notebook)
#         self.report_frame = ttk.Frame(self.notebook)

#         # Add tabs/pages to the Notebook
#         self.notebook.add(self.home_frame, text="Home")
#         self.notebook.add(self.customer_list_frame, text="Customers")
#         self.notebook.add(self.customer_frame, text="Customer Details")
#         self.notebook.add(self.quotation_list_frame, text="Quotations")
#         self.notebook.add(self.quotation_frame, text="Quote Details")
#         self.notebook.add(self.order_list_frame, text="Orders")
#         self.notebook.add(self.order_frame, text="Order Details")
#         self.notebook.add(self.product_frame, text="Products & Services")
#         self.notebook.add(self.report_frame, text="Reports")

#         # Grid Notebook
#         self.notebook.grid(column=0, row=0, columnspan=2, rowspan=12, sticky=(N, W, E, S))

#     def configure_rows_columns(self):
#         """Configure the rows and columns resizing behaviour"""
#         # Root
#         self.root.columnconfigure(0, weight=1)
#         self.root.columnconfigure(1, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         self.root.rowconfigure(1, weight=1)
#         self.root.rowconfigure(2, weight=1)
#         self.root.rowconfigure(3, weight=1)
#         self.root.rowconfigure(4, weight=1)

#         self.home_frame.columnconfigure(0, weight=1)
#         self.home_frame.columnconfigure(1, weight=1)
#         self.home_frame.rowconfigure(0, weight=1)
#         self.home_frame.rowconfigure(1, weight=1)
#         self.home_frame.rowconfigure(2, weight=1)

#         self.customer_list_frame.columnconfigure(0, weight=1)
#         self.customer_list_frame.columnconfigure(1, weight=1)
#         self.customer_list_frame.rowconfigure(0, weight=1)
#         self.customer_list_frame.rowconfigure(1, weight=1)
#         self.customer_list_frame.rowconfigure(2, weight=1)

#         self.customer_frame.columnconfigure(0, weight=1)
#         self.customer_frame.columnconfigure(1, weight=1)
#         self.customer_frame.rowconfigure(0, weight=1)
#         self.customer_frame.rowconfigure(1, weight=1)
#         self.customer_frame.rowconfigure(2, weight=1)

#         self.quotation_list_frame.columnconfigure(0, weight=1)
#         self.quotation_list_frame.columnconfigure(1, weight=1)
#         self.quotation_list_frame.rowconfigure(0, weight=1)
#         self.quotation_list_frame.rowconfigure(1, weight=1)
#         self.quotation_list_frame.rowconfigure(2, weight=1)

#         self.quotation_frame.columnconfigure(0, weight=1)
#         self.quotation_frame.columnconfigure(1, weight=1)
#         self.quotation_frame.rowconfigure(0, weight=1)
#         self.quotation_frame.rowconfigure(1, weight=1)
#         self.quotation_frame.rowconfigure(2, weight=1)

#         self.order_list_frame.columnconfigure(0, weight=1)
#         self.order_list_frame.columnconfigure(1, weight=1)
#         self.order_list_frame.rowconfigure(0, weight=1)
#         self.order_list_frame.rowconfigure(1, weight=1)
#         self.order_list_frame.rowconfigure(2, weight=1)

#         self.order_frame.columnconfigure(0, weight=1)
#         self.order_frame.columnconfigure(1, weight=1)
#         self.order_frame.rowconfigure(0, weight=1)
#         self.order_frame.rowconfigure(1, weight=1)
#         self.order_frame.rowconfigure(2, weight=1)

#         self.product_frame.columnconfigure(0, weight=1)
#         self.product_frame.columnconfigure(1, weight=1)
#         self.product_frame.rowconfigure(0, weight=1)
#         self.product_frame.rowconfigure(1, weight=1)
#         self.product_frame.rowconfigure(2, weight=1)

#         self.report_frame.columnconfigure(0, weight=1)
#         self.report_frame.columnconfigure(1, weight=1)
#         self.report_frame.rowconfigure(0, weight=1)
#         self.report_frame.rowconfigure(1, weight=1)
#         self.report_frame.rowconfigure(2, weight=1)


#     def setup_home_tab(self):
#         home_tab = HomeTab(self.root, self.home_frame)
#         return home_tab

#     def setup_customer_tab(self):
#         customer_details_tab = CustomerDetailsTab(
#             self.notebook,
#             self.customer_frame,
#             self.quotation_list_tab,
#             self.order_list_tab,
#             session)
#         return customer_details_tab

#     def setup_customer_list_tab(self):
#         customer_list_tab = CustomerListTab(
#             self.notebook,
#             self.customer_list_frame,
#             self.customer_details_tab,
#             session
#         )
#         return customer_list_tab

#     def setup_quote_tab(self):
#         quote_details_tab = QuoteDetailsTab(
#             self.notebook,
#             self.quotation_frame,
#             self.order_details_tab,
#             session)
#         return quote_details_tab

#     def setup_quotation_list_tab(self):
#         quotation_list_tab = QuotationListTab(
#             self.notebook,
#             self.quotation_list_frame,
#             self.quote_details_tab,
#             session
#         )
#         return quotation_list_tab
#     # Pass customer_details_tab object to the list_tab object, enables calling customer_details_tab methods from list
#     def setup_order_tab(self):
#         order_details_tab = OrderDetailsTab(self.notebook, self.order_frame, session)
#         return order_details_tab

#     def setup_order_list_tab(self):
#         order_list_tab = OrderListTab(
#             self.notebook,
#             self.order_list_frame,
#             self.order_details_tab,
#             session
#         )
#         return order_list_tab

#     def setup_product_tab(self):
#         product_details_tab = ProductDetailsTab(
#             self.notebook,
#             self.product_frame,
#             session)
#         return product_details_tab

# https://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy


# class PasswordHash(object):
#     def __init__(self, hash_):
#         assert len(hash_) == 60, "bcrypt hash should be 60 chars."
#         assert hash_.count("$"), 'bcrypt hash should have 3x "$".'
#         self.hash = str(hash_)
#         self.rounds = int(self.hash.split("$")[2])

#     def __eq__(self, candidate):
#         """Hashes the candidate string and compares it to the stored hash."""
#         if isinstance(candidate, str):
#             candidate = candidate.encode("utf8")
#             return bcrypt.hashpw(candidate, self.hash) == self.hash
#         return False

#     def __repr__(self):
#         """Simple object representation."""
#         return "<{}>".format(type(self).__name__)

#     @classmethod
#     def new(cls, password, rounds):
#         """Creates a PasswordHash from the given password."""
#         if isinstance(password, str):
#             password = password.encode("utf8")
#         return cls(bcrypt.hashpw(password, bcrypt.gensalt(rounds)))


# class Password(TypeDecorator):
#     """Allows storing and retrieving password hashes using PasswordHash."""

#     impl = Text

#     def __init__(self, rounds=12, **kwds):
#         self.rounds = rounds
#         super(Password, self).__init__(**kwds)

#     def process_bind_param(self, value, dialect):
#         """Ensure the value is a PasswordHash and then return its hash."""
#         return self._convert(value).hash

#     def process_result_value(self, value, dialect):
#         """Convert the hash to a PasswordHash, if it's non-NULL."""
#         if value is not None:
#             return PasswordHash(value)

#     def validator(self, password):
#         """Provides a validator/converter for @validates usage."""
#         return self._convert(password)

#     def _convert(self, value):
#         """Returns a PasswordHash from the given string.

#         PasswordHash instances or None values will return unchanged.
#         Strings will be hashed and the resulting PasswordHash returned.
#         Any other input will result in a TypeError.
#         """
#         if isinstance(value, PasswordHash):
#             return value
#         elif isinstance(value, str):
#             return PasswordHash.new(value, self.rounds)
#         elif value is not None:
#             raise TypeError("Cannot convert {} to a PasswordHash".format(type(value)))