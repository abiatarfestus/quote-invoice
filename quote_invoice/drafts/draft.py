from tkinter import *
from tkinter import ttk
from turtle import bgcolor


class MainWindow:
    def __init__(self, root):

        root.title("Quote & Invoice")

        self.top_frame = ttk.Frame(
            root, 
            # padding="3 3 12 12", 
            borderwidth=5, 
            # relief="solid"
        )
        self.mid_frame = ttk.Frame(
            root, 
            # padding="3 3 12 12", 
            borderwidth=5, 
            relief="solid"
        )
        self.bottom_frame = ttk.Frame(
            root, 
            # padding="3 3 12 12", 
            borderwidth=5, 
            # relief="solid"
        )
        self.top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        self.mid_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))
        self.bottom_frame.grid(column=0, row=4, columnspan=2, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)

        # self.feet = StringVar()
        # feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        # feet_entry.grid(column=2, row=1, sticky=(W, E))
        # self.meters = StringVar()

        # ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)
        # ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        # ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        # ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        

        # Styles
        s = ttk.Style()
        s.configure("home_btns.TButton", font=(None, 24))
        s.configure("heading.TLabel", font=(None, 31))
        s.configure(
            "main_menu.TLabel", 
            font=(None, 24), 
            background="blue",
            foreground="white"
        )

        # LABELS
        # ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        self.heading_lbl = ttk.Label(
            self.top_frame,
            text="Quote & Invoice v0.0.1",
            anchor="center",
            style="heading.TLabel",
        )

        self.main_menu_lbl = ttk.Label(
            self.mid_frame,
            text="Main Menu",
            anchor="center",
            style="main_menu.TLabel",
            padding=(180,2)
        )

        # Buttons
        self.customer_list_btn = ttk.Button(
            self.mid_frame,
            text="Customer List",
            style="home_btns.TButton",
            padding=26
        )
        self.customer_form_btn = ttk.Button(
            self.mid_frame, 
            text="Customer Form",
            style="home_btns.TButton",
            padding=(15, 26)
        )
        self.quotations_btn = ttk.Button(
            self.mid_frame, 
            text="Quotations",
            style="home_btns.TButton",
            padding=26
        )
        self.orders_invoies_btn = ttk.Button(
            self.mid_frame, 
            text="Orders/Invoices",
            style="home_btns.TButton",
            padding=(15, 26)
        )

        # Placement
        self.heading_lbl.grid(row=0)
        self.main_menu_lbl.grid(column=0, row=0, columnspan=2)
        self.customer_list_btn.grid(column=0, row=1, sticky=E)
        self.customer_form_btn.grid(column=0, row=2, sticky=E)
        self.quotations_btn.grid(column=1, row=1, sticky=W)
        self.orders_invoies_btn.grid(column=1, row=2, sticky=W)

        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        self.mid_frame.columnconfigure(0, weight=1)
        self.mid_frame.columnconfigure(1, weight=1)
        self.mid_frame.rowconfigure(0, weight=1)
        self.mid_frame.rowconfigure(1, weight=1)
        # self.mid_frame.rowconfigure(2, weight=1)
        # self.mid_frame.rowconfigure(3, weight=1)
        # self.mid_frame.rowconfigure(4, weight=1)

        for child in self.mid_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # feet_entry.focus()
        # root.bind("<Return>", self.calculate)

    # def calculate(self, *args):
    #     try:
    #         value = float(self.feet.get())
    #         self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    #     except ValueError:
    #         pass


    


from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# Global Variables
SQLITE                  = 'sqlite'
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'
# MICROSOFT_SQL_SERVER    = 'mssqlserver'

# Table Names
USERS           = 'users'
ADDRESSES       = 'addresses'


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
        # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url)
            print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        users = Table(USERS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('first_name', String),
                      Column('last_name', String)
                      )

        address = Table(ADDRESSES, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id', None, ForeignKey('users.id')),
                        Column('email', String, nullable=False),
                        Column('address', String)
                        )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return

        print (query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)


    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row) # print(row[0], row[1], row[2])
                result.close()

        print("\n")

    # Examples

    def sample_query(self):
        # Sample Query
        query = "SELECT first_name, last_name FROM {TBL_USR} WHERE " \
                "last_name LIKE 'M%';".format(TBL_USR=USERS)
        self.print_all_data(query=query)

        # Sample Query Joining
        query = "SELECT u.last_name as last_name, " \
                "a.email as email, a.address as address " \
                "FROM {TBL_USR} AS u " \
                "LEFT JOIN {TBL_ADDR} as a " \
                "WHERE u.id=a.user_id AND u.last_name LIKE 'M%';" \
            .format(TBL_USR=USERS, TBL_ADDR=ADDRESSES)
        self.print_all_data(query=query)

    def sample_delete(self):
        # Delete Data by Id
        query = "DELETE FROM {} WHERE id=3".format(USERS)
        self.execute_query(query)
        self.print_all_data(USERS)

        # Delete All Data
        '''
        query = "DELETE FROM {}".format(USERS)
        self.execute_query(query)
        self.print_all_data(USERS)
        '''

    def sample_insert(self):
        # Insert Data
        query = "INSERT INTO {}(id, first_name, last_name) " \
                "VALUES (3, 'Terrence','Jordan');".format(USERS)
        self.execute_query(query)
        self.print_all_data(USERS)

    def sample_update(self):
        # Update Data
        query = "UPDATE {} set first_name='XXXX' WHERE id={id}"\
            .format(USERS, id=3)
        self.execute_query(query)
        self.print_all_data(USERS)
