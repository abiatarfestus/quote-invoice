from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from quote_invoice.common.constants import DB_PATH
from sqlalchemy.ext.declarative import declarative_base
from quote_invoice.db.models import User

Base = declarative_base()


class UserAuthentication:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        
        self.popup = Toplevel()
        self.popup.title("Login")
        self.popup.grab_set()

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
        for child in self.popup.winfo_children():
            child.grid_configure(padx=2, pady=5)
        
        engine = create_engine(DB_PATH)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def login(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        
        user = self.session.query(User).filter_by(username=username, password=password).first()
        if user:
            self.popup.destroy()
            self.parent.grab_set()
        else:
            error_message = ttk.Label(self.popup, text="Incorrect username or password")
            error_message.pack()
    
    def register(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            error_message = ttk.Label(self.popup, text="Username already exists")
            error_message.pack()
        else:
            new_user = User(username=username, password=password)
            self.session.add(new_user)
            self.session.commit()
            self.popup.destroy()
            self.parent.grab_set()
