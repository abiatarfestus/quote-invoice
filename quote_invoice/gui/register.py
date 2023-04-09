import re
from tkinter import *
from tkinter import messagebox, ttk

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from quote_invoice.common.constants import DB_PATH
from quote_invoice.db import operations as db
from quote_invoice.db.models import User

Base = declarative_base()
register_icon_path = r"quote_invoice\assets\icons8-sign-up-64.png"


class UserRegistration:
    def __init__(self, parent, user_type="staff"):
        self.popup = Toplevel()
        w = 450
        h = 380
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)
        self.popup.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.parent = parent
        self.user_type = user_type
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.popup.title("Register")
        self.popup.resizable(False, False)
        self.logo = PhotoImage(file=register_icon_path)
        self.popup.iconphoto(False, self.logo)
        self.popup.grab_set()

        # Labels:
        self.register_lbl = ttk.Label(
            self.popup,
            text="User Registration",
            anchor="center",
            style="heading2.TLabel",
        )
        self.register_lbl.grid(column=0, columnspan=3, row=0, sticky=(N, S, W, E))

        self.username_lbl = ttk.Label(self.popup, text="Username:", anchor=W)
        self.username_lbl.grid(column=0, row=1, sticky=(N, S, W, E))

        self.password1_lbl = ttk.Label(self.popup, text="Password:", anchor=W)
        self.password1_lbl.grid(column=0, row=2, sticky=(N, S, W, E))

        self.password2_lbl = ttk.Label(self.popup, text="Confirm Password:", anchor=W)
        self.password2_lbl.grid(column=0, row=3, sticky=(N, S, W, E))

        self.first_name_lbl = ttk.Label(self.popup, text="First Name:", anchor=W)
        self.first_name_lbl.grid(column=0, row=4, sticky=(N, S, W, E))

        self.last_name_lbl = ttk.Label(self.popup, text="Last Name:", anchor=W)
        self.last_name_lbl.grid(column=0, row=5, sticky=(N, S, W, E))

        self.email_lbl = ttk.Label(self.popup, text="Email Address:", anchor=W)
        self.email_lbl.grid(column=0, row=6, sticky=(N, S, W, E))

        # Checkboxes:
        self.is_admin = BooleanVar()
        self.is_admin_chk = ttk.Checkbutton(
            self.popup,
            text="Is Admin:",
            variable=self.is_admin,
            onvalue=1,
            offvalue=0,
        )
        self.is_admin_chk.grid(column=0, row=7, sticky=(N, S, W, E))
        self.is_admin_chk.state(["!disabled"])
        if self.user_type == "admin":
            self.is_admin.set(value=1)
        else:
            self.is_admin.set(value=0)
            self.email_ent.state(["!disabled"])
        self.is_admin_chk.state(["disabled"])

        # Entries:
        self.username_ent = ttk.Entry(self.popup, width=40)
        self.username_ent.grid(column=1, columnspan=2, row=1, sticky=(N, S, E, W))

        self.password1_ent = ttk.Entry(self.popup, width=40, show="*")
        # self.id_ent.insert(0, "New")
        self.password1_ent.grid(column=1, columnspan=2, row=2, sticky=(N, S, E, W))

        self.password2_ent = ttk.Entry(self.popup, width=40, show="*")
        # self.id_ent.insert(0, "New")
        self.password2_ent.grid(column=1, columnspan=2, row=3, sticky=(N, S, E, W))

        self.first_name_ent = ttk.Entry(self.popup, width=40)
        self.first_name_ent.grid(column=1, columnspan=2, row=4, sticky=(N, S, E, W))

        self.last_name_ent = ttk.Entry(self.popup, width=40)
        self.last_name_ent.grid(column=1, columnspan=2, row=5, sticky=(N, S, E, W))

        self.email_ent = ttk.Entry(self.popup, width=40)
        self.email_ent.grid(column=1, columnspan=2, row=6, sticky=(N, S, E, W))

        # Buttons:
        self.register_btn = ttk.Button(
            self.popup, text="Register", padding=5, command=self.register
        )
        self.register_btn.grid(column=2, row=8, sticky=(E, W))

        for child in self.popup.winfo_children():
            child.grid_configure(padx=5, pady=5)

        engine = create_engine(DB_PATH)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def register(self):
        username = self.username_ent.get().strip()
        password1 = self.password1_ent.get().strip()
        password2 = self.password2_ent.get().strip()
        first_name = self.first_name_ent.get().strip().capitalize()
        last_name = self.last_name_ent.get().strip().capitalize()
        email = self.email_ent.get().strip()
        is_admin = self.is_admin.get()
        valid, message = self.validate_registration(
            username=username, password1=password1, password2=password2, email=email
        )

        if not valid:
            error_message = ttk.Label(
                self.popup, text=message, style="ErrorLabel.TLabel", anchor=CENTER
            )
            error_message.grid(column=1, columnspan=2, row=7, sticky=(E, W))
            return
        try:
            new_user = db.add_user(
                session=self.session,
                username=username,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_admin=is_admin,
            )
            messagebox.showinfo(message="User successfully added!", title="Success")
            self.parent.is_authenticated = True
            self.parent.authenticated_user = new_user
            self.parent.authenticated_user_name.set(f"User: {new_user.username}")
            self.parent.login_out.set("Logout")
            self.popup.destroy()
            self.parent.grab_set()
        except NameError as e:
            error_message = messagebox.showerror(
                message="An error occured:", detail=e, title="Error"
            )
            return error_message

    def validate_registration(self, username, password1, password2, email):
        if password1 != password2:
            return (False, "Passwords do not match!")
        elif len(password1) < 8:
            return (False, "Password cannot be less than 8 characters!")
        elif len(username) < 4:
            return (False, "Username cannot be less than 4 characters!")
        elif not self.validate_email(email):
            return (False, "Invalid email address entered!")
        return (True, "Valid registration.")

    def validate_email(self, email):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if re.search(regex, email):
            return True
        else:
            return False

    def on_closing(self):
        if self.user_type == "staff":
            self.parent.destroy()
            self.parent.destroy()
        else:
            if not messagebox.askyesno(
                message="Would like to quit the application?",
                icon="question",
                title="Quit Application",
            ):
                return
            self.popup.destroy()
            self.parent.destroy()
