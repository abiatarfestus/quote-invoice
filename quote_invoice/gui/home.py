from tkinter import *
from tkinter import messagebox, ttk

from quote_invoice.common.constants import DB_PATH, MAIN_LOGO_PATH
from quote_invoice.gui.settings.settings import SettingsWindow

from .login import UserAuthentication


class HomeTab:
    def __init__(self, parent, parent_frame):
        """Configure the home tab page"""
        self.parent = parent
        self.main_logo = PhotoImage(file=MAIN_LOGO_PATH)
        # self.logged_in_user = self.parent.logged_in_user_name.get()
        # -------------------------------------TOP FRAME-----------------------------------#
        # Frames:
        self.top_frame = ttk.Frame(
            parent_frame,
            borderwidth=5,
            # relief="solid"
        )
        self.top_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        # Labels:
        self.heading_lbl = ttk.Label(
            self.top_frame,
            # text="Quote & Invoice v0.0.1",
            image=self.main_logo,
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0)
        # -------------------------------TOP FRAME ENDS--------------------------------------#

        # -------------------------------MID FRAME-------------------------------------------#

        # -------------------------------MID FRAME ENDS---------------------------------------#

        # -------------------------------BOTTOM FRAME-----------------------------------------#
        self.bottom_frame = ttk.Frame(
            parent_frame,
            borderwidth=5,
            # relief="solid"
        )
        self.bottom_frame.grid(column=0, row=1, sticky=(W, E, S))
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=1)
        self.bottom_frame.columnconfigure(3, weight=1)
        self.bottom_frame.columnconfigure(4, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        # Labels:
        self.user_lbl = ttk.Label(
            self.bottom_frame,
            textvariable=self.parent.auth_data["user_name"],
            anchor="w",
            style="BlueLabel.TLabel",
        )
        self.user_lbl.grid(column=0, row=0, sticky=(W,E))

        self.creator_lbl = ttk.Label(
            self.bottom_frame,
            text="Created by Festus Abiatar",
            anchor="e",
        )
        self.creator_lbl.grid(column=4, row=1, sticky=(S, E))

        # Buttons:
        self.login_logout_btn = ttk.Button(
            self.bottom_frame,
            textvariable=self.parent.auth_data["button_text"],
            # style="Danger.TButton",
            command=self.logout
            # padding=(15, 26)
        )
        # self.login_logout_btn.state(["disabled"])
        self.login_logout_btn.grid(column=1, row=0, sticky=(N, S, E, W))

        self.help_btn = ttk.Button(
            self.bottom_frame,
            text="Help",
            style="btns.TButton",
            # padding=(15, 26)
        )
        # self.help_btn.state(["disabled"])
        self.help_btn.grid(column=2, row=0, sticky=(N, S, E, W))

        self.settings_btn = ttk.Button(
            self.bottom_frame,
            text="Settings",
            style="btns.TButton",
            # padding=(15, 26),
            command=self.open_settings,
        )
        self.settings_btn.grid(column=3, row=0, sticky=(N, S, E, W))

        self.exit_btn = ttk.Button(
            self.bottom_frame,
            text="Exit",
            # style="Danger.TButton",
            command=self.close_window,
        )
        self.exit_btn.grid(column=4, row=0, sticky=(N, S, E, W))

        for child in self.bottom_frame.winfo_children():
            child.grid_configure(padx=2, pady=5)
        # -------------------------------BOTTOM FRAME ENDS------------------------------------#

    def open_settings(self):
        # settings_menu = Menu(win)
        SettingsWindow(self.parent)

    def close_window(self):
        if not messagebox.askyesno(
            message="Are you sure you want to exit?",
            icon="question",
            title="Exit Application",
        ):
            return
        self.parent.destroy()

    def logout(self):
        self.parent.auth_data["is_authenticated"] = False
        self.parent.auth_data["user"] = None
        self.parent.auth_data["user_name"].set("User: Logged Out")
        self.parent.auth_data["button_text"].set("Login")
        user = UserAuthentication(self.parent, DB_PATH)
