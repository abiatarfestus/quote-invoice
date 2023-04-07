from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from quote_invoice.db import operations as db
from quote_invoice.common.constants import DB_PATH
from sqlalchemy.ext.declarative import declarative_base
from quote_invoice.db.models import User
from .register import UserRegistration

Base = declarative_base()


 



class UserAuthentication:
    engine = create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    

    def __init__(self, parent, db_path):
        self.popup = Toplevel()
        w = 380 # Width 
        h = 180 # Height 
        screen_width = self.popup.winfo_screenwidth()  # Width of the screen
        screen_height = self.popup.winfo_screenheight() # Height of the screen
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.session = self.Session()
        self.parent = parent
        self.db_path = db_path
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.popup.title("Login")
        self.popup.grab_set()
        self.popup.resizable(False, False)
        self.admin_user = db.get_admin_user(self.session) # Get admin user from the database

        # Labels:
        self.login_lbl = ttk.Label(
            self.popup,
            text="Login",
            anchor="center",
            style="heading2.TLabel",
        )
        self.login_lbl.grid(column=1, columnspan=3, row=0, sticky=(N, S, W, E))

        self.username_lbl = ttk.Label(
            self.popup,
            text="Username:",
            anchor=W
        )
        self.username_lbl.grid(column=0, row=1, sticky=(N, S, W, E))

        self.password_lbl = ttk.Label(
            self.popup,
            text="Password:",
            anchor=W
        )
        self.password_lbl.grid(column=0, row=2, sticky=(N, S, W, E))
        
        # Entries:
        self.username_ent = ttk.Entry(
            self.popup,
            width=40
        )
        self.username_ent.grid(column=1, columnspan=2, row=1, sticky=(N, S, E, W))
        
        self.password_ent = ttk.Entry(
            self.popup,
            width=40,
            show="*"
        )
        # self.id_ent.insert(0, "New")
        self.password_ent.grid(column=1, columnspan=2, row=2, sticky=(N, S, E, W))

        # Buttons:
        self.login_btn = ttk.Button(
            self.popup,
            text="Login",
            padding=5,
            command=self.login
        )
        self.login_btn.grid(column=1, row=3, sticky=(E, W))

        self.register_btn = ttk.Button(
            self.popup,
            text="Register",
            padding=5,
            command=self.register
        )
        self.register_btn.grid(column=2, row=3, sticky=(E, W))
        if self.admin_user: # If there's an admin user in the database
            self.register_btn.state(["disabled"])

        for child in self.popup.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
    
    def login(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        
        user = self.session.query(User).filter_by(username=username, password=password).first()
        if user:
            self.popup.destroy()
            self.parent.grab_set()
            self.parent.is_authenticated = True
            self.parent.authenticated_user = user
            self.parent.authenticated_user_name = user.username
        else:
            error_message = ttk.Label(
                self.popup,
                text="Incorrect username or password",
                style="ErrorLabel.TLabel",
                anchor=CENTER
            )
            error_message.grid(column=1, columnspan=2, row=4, sticky=(E, W))
            self.login()
    
    def register(self):
        self.popup.destroy()
        self.parent.grab_set()
        user_registration = UserRegistration(self.parent, user_type="admin")
    
    def on_closing(self):
        if not messagebox.askyesno(
            message="Would like to quit the application?",
            icon='question',
            title='Quit Application'
        ):
            return
        self.popup.destroy()
        self.parent.destroy()


