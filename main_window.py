from tkinter import *
from tkinter import ttk


class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Quote & Invoice")

        # Styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("notebook.TNotebook.Tab", padding=10, font=(None, 16))
        style.configure("home_btns.TButton", font=(None, 24))
        style.configure("heading.TLabel", font=(None, 31))
        style.configure(
            "main_menu.TLabel", 
            font=(None, 24), 
            background="blue",
            foreground="white"
        )

        # Create a Notebook and Frames
        self.notebook = ttk.Notebook(self.root, style="notebook.TNotebook",)
        self.home_frame = ttk.Frame(self.notebook)
        self.customer_list_frame = ttk.Frame(self.notebook)
        self.customer_form_frame = ttk.Frame(self.notebook)
        self.quotations_frame = ttk.Frame(self.notebook)
        self.orders_frame = ttk.Frame(self.notebook)

        # Add tabs/pages to the Notebook
        self.notebook.add(self.home_frame, text="Home")
        self.notebook.add(self.customer_list_frame, text="Customer List")
        self.notebook.add(self.customer_form_frame, text="Customer Form")
        self.notebook.add(self.quotations_frame, text="Quotations")
        self.notebook.add(self.orders_frame, text="Orders/Invoices")
        
        # Grid Notebook
        self.notebook.grid(column=0, row=0, columnspan=2, rowspan=12, sticky=(N, W, E, S))


    def setup_home_tab(self):
        # Frames
        top_frame = ttk.Frame(
            self.home_frame,
            borderwidth=5, 
            # relief="solid"
        )
        mid_frame = ttk.Frame(
            self.home_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.home_frame,
            borderwidth=5, 
            # relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(W, E, S))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Quote & Invoice v0.0.1",
            anchor="center",
            style="heading.TLabel",
        )

        main_menu_lbl = ttk.Label(
            mid_frame,
            text="Main Menu",
            anchor="center",
            style="main_menu.TLabel",
            padding=(180,2)
        )

        creator_lbl = ttk.Label(
            bottom_frame,
            text="Created by Festus Abiatar",
            anchor="e",
        )

        heading_lbl.grid(row=0)
        main_menu_lbl.grid(column=0, row=0, columnspan=2)
        creator_lbl.grid(column=1, row=0, sticky=(S, E))

        # Buttons
        customer_list_btn = ttk.Button(
            mid_frame,
            text="Customer List",
            style="home_btns.TButton",
            padding=26
        )
        customer_form_btn = ttk.Button(
            mid_frame, 
            text="Customer Form",
            style="home_btns.TButton",
            padding=(15, 26)
        )
        quotations_btn = ttk.Button(
            mid_frame, 
            text="Quotations",
            style="home_btns.TButton",
            padding=26
        )
        orders_invoies_btn = ttk.Button(
            mid_frame, 
            text="Orders/Invoices",
            style="home_btns.TButton",
            padding=(15, 26)
        )

        customer_list_btn.grid(column=0, row=1, sticky=E)
        customer_form_btn.grid(column=0, row=2, sticky=E)
        quotations_btn.grid(column=1, row=1, sticky=W)
        orders_invoies_btn.grid(column=1, row=2, sticky=W)

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.rowconfigure(1, weight=1)

        for child in mid_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def setup_customer_list_tab(self):
        # Frames
        top_frame = ttk.Frame(
            self.customer_list_frame,
            borderwidth=5, 
            relief="solid"
        )
        mid_frame = ttk.Frame(
            self.customer_list_frame, 
            borderwidth=5, 
            relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.customer_list_frame,
            borderwidth=5, 
            relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # LABELS
        heading_lbl = ttk.Label(
            top_frame,
            text="Customer List",
            anchor="center",
            style="heading.TLabel",
        )

        heading_lbl.grid(row=0)

        # Buttons
        open_customer_btn = ttk.Button(
            bottom_frame,
            text="Open Selected Record",
            # style="home_btns.TButton",
            padding=21
        )
        add_customer_btn = ttk.Button(
            bottom_frame, 
            text="Add New Customer",
            # style="home_btns.TButton",
            padding=(10, 21)
        )

        open_customer_btn.grid(column=0, row=1, sticky=E)
        add_customer_btn.grid(column=1, row=1, sticky=E)

        # Treeview
        tree = ttk.Treeview(mid_frame, show='headings', height=20)
        
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
            "First Name", 
            "Last Name", 
            "Entity Name", 
            "Locality", 
            "Customer Since"
        )

        # Format Our Columns
        tree.column("ID", anchor=CENTER)
        tree.column("First Name", anchor=W)
        tree.column("Last Name", anchor=W)
        tree.column("Entity Name", anchor=W)
        tree.column("Locality", anchor=W)
        tree.column("Customer Since", anchor=E)

        # Create Headings
        tree.heading("ID", text="ID", anchor=CENTER)
        tree.heading("First Name", text="First Name", anchor=W)
        tree.heading("Last Name", text="Last Name", anchor=W)
        tree.heading("Entity Name", text="Entity Name", anchor=W)
        tree.heading("Locality", text="Locality", anchor=W)
        tree.heading("Customer Since", text="Customr Since", anchor=E)

        # Insert the data in Treeview widget
        tree.insert('', 'end', values=('1', 'Joe', 'Nash', "Tomarx", "Windhoek", "26/10/2022"))
        tree.insert('', 'end', values=('2', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('3', 'Estilla', 'Roffe'))
        tree.insert('', 'end', values=('4', 'Percy', 'Andrews'))
        tree.insert('', 'end', values=('5', 'Stephan', 'Heyward'))
        tree.insert('', 'end', values=('6', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('1', 'Joe', 'Nash', "Tomarx", "Windhoek", "26/10/2022"))
        tree.insert('', 'end', values=('2', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('3', 'Estilla', 'Roffe'))
        tree.insert('', 'end', values=('4', 'Percy', 'Andrews'))
        tree.insert('', 'end', values=('5', 'Stephan', 'Heyward'))
        tree.insert('', 'end', values=('6', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('1', 'Joe', 'Nash', "Tomarx", "Windhoek", "26/10/2022"))
        tree.insert('', 'end', values=('2', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('3', 'Estilla', 'Roffe'))
        tree.insert('', 'end', values=('4', 'Percy', 'Andrews'))
        tree.insert('', 'end', values=('5', 'Stephan', 'Heyward'))
        tree.insert('', 'end', values=('6', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('1', 'Joe', 'Nash', "Tomarx", "Windhoek", "26/10/2022"))
        tree.insert('', 'end', values=('2', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('3', 'Estilla', 'Roffe'))
        tree.insert('', 'end', values=('4', 'Percy', 'Andrews'))
        tree.insert('', 'end', values=('5', 'Stephan', 'Heyward'))
        tree.insert('', 'end', values=('6', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('1', 'Joe', 'Nash', "Tomarx", "Windhoek", "26/10/2022"))
        tree.insert('', 'end', values=('2', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('3', 'Estilla', 'Roffe'))
        tree.insert('', 'end', values=('4', 'Percy', 'Andrews'))
        tree.insert('', 'end', values=('5', 'Stephan', 'Heyward'))
        tree.insert('', 'end', values=('6', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('1', 'Joe', 'Nash', "Tomarx", "Windhoek", "26/10/2022"))
        tree.insert('', 'end', values=('2', 'Emily', 'Mackmohan'))
        tree.insert('', 'end', values=('3', 'Estilla', 'Roffe'))
        tree.insert('', 'end', values=('4', 'Percy', 'Andrews'))
        tree.insert('', 'end', values=('5', 'Stephan', 'Heyward'))
        tree.insert('', 'end', values=('6', 'Emily', 'Mackmohan'))

        tree.grid(column=0, row=0, sticky=(N, S, W, E))

        

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=1)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)

    def setup_customer_form_tab(self):
        # Frames
        top_frame = ttk.Frame(
            self.customer_form_frame,
            borderwidth=5, 
            # relief="solid"
        )
        mid_frame = ttk.Frame(
            self.customer_form_frame, 
            borderwidth=5, 
            relief="solid"
        )
        bottom_frame = ttk.Frame(
            self.customer_form_frame,
            borderwidth=5, 
            # relief="solid"
        )

        top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W))
        bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

        # Labels
        heading_lbl = ttk.Label(
            top_frame,
            text="Customer Details",
            anchor="center",
            style="heading.TLabel",
        )
        id_lbl = ttk.Label(
            mid_frame,
            text="Customer ID",
            anchor=W,
            # style="heading.TLabel",
        )
        type_lbl = ttk.Label(
            mid_frame,
            text="Customer Tpe",
            anchor=W,
            # style="heading.TLabel",
        )
        f_name_lbl = ttk.Label(
            mid_frame,
            text="First Name",
            anchor=W,
            # style="heading.TLabel",
        )
        l_name_lbl = ttk.Label(
            mid_frame,
            text="Last Name",
            anchor=W,
            # style="heading.TLabel",
        )
        entity_lbl = ttk.Label(
            mid_frame,
            text="Entity Name",
            anchor=W,
            # style="heading.TLabel",
        )
        email_lbl = ttk.Label(
            mid_frame,
            text="Email",
            anchor=W,
            # style="heading.TLabel",
        )
        phone_lbl = ttk.Label(
            mid_frame,
            text="Phone",
            anchor=W,
            # style="heading.TLabel",
        )
        address_lbl = ttk.Label(
            mid_frame,
            text="Address",
            anchor=W,
            # style="heading.TLabel",
        )
        town_lbl = ttk.Label(
            mid_frame,
            text="Town",
            anchor=W,
            # style="heading.TLabel",
        )
        country_lbl = ttk.Label(
            mid_frame,
            text="Country",
            anchor=W,
            # style="heading.TLabel",
        )
        since_lbl = ttk.Label(
            mid_frame,
            text="Customer Since",
            anchor=W,
            # style="heading.TLabel",
        )
        notes_lbl = ttk.Label(
            mid_frame,
            text="Notes",
            anchor=E,
            # style="heading.TLabel",
        )

        heading_lbl.grid(row=0, sticky=(N, S, W, E))
        id_lbl.grid(column=0, row=1, sticky=(W, ))
        type_lbl.grid(column=0, row=2, sticky=(W, ))
        f_name_lbl.grid(column=0, row=3, sticky=(W, ))
        l_name_lbl.grid(column=0, row=4, sticky=(W, ))
        entity_lbl.grid(column=0, row=5, sticky=(W, ))
        email_lbl.grid(column=0, row=6, sticky=(W, ))
        phone_lbl.grid(column=0, row=7, sticky=(W, ))
        address_lbl.grid(column=0, row=8, sticky=(W, ))
        town_lbl.grid(column=0, row=9, sticky=(W, ))
        country_lbl.grid(column=0, row=10, sticky=(W, ))
        since_lbl.grid(column=0, row=11, sticky=(W, ))
        notes_lbl.grid(column=4, row=0, sticky=(E, ))

        # Entries
        id_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        id_ent.state(["disabled"])

        f_name_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        l_name_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        entity_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        email_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        phone_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        address_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        town_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        country_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        since_ent = ttk.Entry(
            mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        # Comboboxes
        type_cbx = ttk.Combobox(
            mid_frame,
            width=38,
            values=("Person", "Entity")
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        type_cbx.state(["readonly"])

        # Texts
        notes_txt = Text(
            mid_frame,
            width=35, 
            height=9,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )

        id_ent.grid(column=1, row=1)
        type_cbx.grid(column=1, row=2)
        f_name_ent.grid(column=1, row=3)
        l_name_ent.grid(column=1, row=4)
        entity_ent.grid(column=1, row=5)
        email_ent.grid(column=1, row=6)
        phone_ent.grid(column=1, row=7)
        address_ent.grid(column=1, row=8)
        town_ent.grid(column=1, row=9)
        country_ent.grid(column=1, row=10)
        since_ent.grid(column=1, row=11)
        notes_txt.grid(column=2, columnspan=3,row=1, rowspan=5)

        # Buttons
        save_btn = ttk.Button(
            mid_frame,
            text="Save Record",
            # style="home_btns.TButton",
            padding=5
        )
        new_customer_btn = ttk.Button(
            mid_frame,
            text="New Customer",
            # style="home_btns.TButton",
            padding=5
        )
        orders_btn = ttk.Button(
            mid_frame, 
            text="Orders",
            # style="home_btns.TButton",
            padding=5
        )
        contacts_btn = ttk.Button(
            mid_frame, 
            text="Contacts",
            # style="home_btns.TButton",
            padding=5
        )

        save_btn.grid(column=0, columnspan=5, row=11, sticky=(E, W))
        new_customer_btn.grid(column=2, row=6, sticky=(N, S, E, W))
        orders_btn.grid(column=3, row=6, sticky=(N, S, E, W))
        contacts_btn.grid(column=4, row=6, sticky=(N, S, E, W))

        # Configure rows and columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)

        mid_frame.columnconfigure(0, weight=5)
        mid_frame.columnconfigure(1, weight=1)
        mid_frame.columnconfigure(2, weight=1)
        mid_frame.columnconfigure(3, weight=1)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)
        mid_frame.rowconfigure(2, weight=1)
        mid_frame.rowconfigure(3, weight=1)
        mid_frame.rowconfigure(4, weight=1)
        mid_frame.rowconfigure(5, weight=1)
        mid_frame.rowconfigure(6, weight=1)
        mid_frame.rowconfigure(7, weight=1)
        mid_frame.rowconfigure(8, weight=1)
        mid_frame.rowconfigure(9, weight=1)
        mid_frame.rowconfigure(10, weight=1)
        mid_frame.rowconfigure(11, weight=1)

        for child in mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=5)

    def configure_rows_columns(self):
        # Root
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)

        self.home_frame.columnconfigure(0, weight=1)
        self.home_frame.columnconfigure(1, weight=1)
        self.home_frame.rowconfigure(0, weight=1)
        self.home_frame.rowconfigure(1, weight=1)
        self.home_frame.rowconfigure(2, weight=1)

        self.customer_list_frame.columnconfigure(0, weight=1)
        self.customer_list_frame.columnconfigure(1, weight=1)
        self.customer_list_frame.rowconfigure(0, weight=1)
        self.customer_list_frame.rowconfigure(1, weight=1)
        self.customer_list_frame.rowconfigure(2, weight=1)

        self.customer_form_frame.columnconfigure(0, weight=1)
        self.customer_form_frame.columnconfigure(1, weight=1)
        self.customer_form_frame.rowconfigure(0, weight=1)
        self.customer_form_frame.rowconfigure(1, weight=1)
        self.customer_form_frame.rowconfigure(2, weight=1)
