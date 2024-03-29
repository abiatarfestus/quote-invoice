import os
from tkinter import *
from tkinter import messagebox, ttk

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from quote_invoice.common.constants import DB_PATH, HELP_ICON_PATH
from quote_invoice.db import operations as db
from quote_invoice.db.models import User

from .register import UserRegistration

Base = declarative_base()
login_icon_path = r"quote_invoice\assets\icons8-login-rounded-48.png"


class UserAuthentication:
    engine = create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    def __init__(self, parent, db_path):
        self.popup = Toplevel()
        w = 380  # Width
        h = 200  # Height
        screen_width = self.popup.winfo_screenwidth()  # Width of the screen
        screen_height = self.popup.winfo_screenheight()  # Height of the screen
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)
        self.popup.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.session = self.Session()
        self.parent = parent
        self.db_path = db_path
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.popup.title("Login")
        self.logo = PhotoImage(file=login_icon_path)
        self.help = PhotoImage(file=HELP_ICON_PATH)
        self.popup.iconphoto(False, self.logo)
        self.popup.grab_set()
        self.popup.resizable(False, False)
        self.admin_user = db.get_admin_user(
            self.session
        )  # Get admin user from the database

        # Labels:
        self.login_lbl = ttk.Label(
            self.popup,
            text="Login",
            anchor="center",
            style="heading2.TLabel",
        )
        self.login_lbl.grid(column=1, columnspan=2, row=0, sticky=(N, S, W, E))

        self.username_lbl = ttk.Label(self.popup, text="Username:", anchor=W)
        self.username_lbl.grid(column=0, row=1, sticky=(N, S, W, E))

        self.password_lbl = ttk.Label(self.popup, text="Password:", anchor=W)
        self.password_lbl.grid(column=0, row=2, sticky=(N, S, W, E))

        # Entries:
        self.username_ent = ttk.Entry(self.popup, width=40)
        self.username_ent.grid(column=1, columnspan=2, row=1, sticky=(N, S, E, W))

        self.password_ent = ttk.Entry(self.popup, width=40, show="*")
        # self.id_ent.insert(0, "New")
        self.password_ent.grid(column=1, columnspan=2, row=2, sticky=(N, S, E, W))

        # Buttons:
        self.help_btn = ttk.Button(
            self.popup,
            image=self.help,
            padding=5,
            command=lambda: os.startfile("Help.pdf"),
            style="Help.TButton",
        )
        self.help_btn.grid(column=2, row=0, sticky=E)

        self.login_btn = ttk.Button(
            self.popup, text="Login", padding=5, command=self.login
        )
        self.login_btn.grid(column=1, row=3, sticky=(E, W))

        self.register_btn = ttk.Button(
            self.popup, text="Register", padding=5, command=self.register
        )
        self.register_btn.grid(column=2, row=3, sticky=(E, W))
        if self.admin_user:  # If there's an admin user in the database
            self.register_btn.state(["disabled"])

        for child in self.popup.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def login(self):
        username = self.username_ent.get()
        password = self.password_ent.get()

        user = self.session.query(User).filter_by(username=username).first()
        if user:
            if user.check_password(password):
                self.parent.auth_data["is_authenticated"] = True
                self.parent.auth_data["user"] = user
                self.parent.auth_data["user_name"].set(f"User: {user.username}")
                self.parent.auth_data["button_text"].set("Logout")
                self.popup.destroy()
                self.parent.grab_set()
            else:
                error_message = ttk.Label(
                    self.popup,
                    text="Incorrect username or password",
                    style="ErrorLabel.TLabel",
                    anchor=CENTER,
                )
                error_message.grid(column=1, columnspan=2, row=4, sticky=(E, W))
        else:
            error_message = ttk.Label(
                self.popup,
                text="Incorrect username or password",
                style="ErrorLabel.TLabel",
                anchor=CENTER,
            )
            error_message.grid(column=1, columnspan=2, row=4, sticky=(E, W))

    def register(self):
        self.popup.destroy()
        self.parent.grab_set()
        UserRegistration(self.parent, user_type="admin")

    def on_closing(self):
        if not messagebox.askyesno(
            message="Would like to quit the application?",
            icon="question",
            title="Quit Application",
        ):
            return
        self.popup.destroy()
        self.parent.destroy()
