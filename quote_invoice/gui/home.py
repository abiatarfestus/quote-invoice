from tkinter import *
from tkinter import ttk
from quote_invoice.gui.settings.settings import SettingsWindow

class HomeTab():
    def __init__(self, root, parent_frame):
        """Configure the home tab page"""
        self.root = root
        self.main_logo = PhotoImage(file='main_logo.png')
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
            # text="Quote & Invoice v0.0.1",
            image=self.main_logo,
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0)
        #-------------------------------TOP FRAME ENDS--------------------------------------#
        
        #-------------------------------MID FRAME-------------------------------------------#
        # self.mid_frame = ttk.Frame(
        #     parent_frame, 
        #     borderwidth=5, 
        #     # relief="solid"
        # )
        # self.mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        # self.mid_frame.columnconfigure(0, weight=1)
        # self.mid_frame.columnconfigure(1, weight=1)
        # self.mid_frame.rowconfigure(0, weight=1)
        # self.mid_frame.rowconfigure(1, weight=1)

        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        self.bottom_frame = ttk.Frame(
            parent_frame,
            borderwidth=5, 
            # relief="solid"
        )
        self.bottom_frame.grid(column=0, row=2, columnspan=2, sticky=(W, E, S))
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
            text="Loggen in User: None",
            anchor="w",
        )
        self.user_lbl.grid(column=0, row=0, sticky=(S, W))

        self.creator_lbl = ttk.Label(
            self.bottom_frame,
            text="Created by Festus Abiatar",
            anchor="e",
        )
        self.creator_lbl.grid(column=4, row=1, sticky=(S, E))
        
        # Buttons:
        self.login_logout_btn = ttk.Button(
            self.bottom_frame, 
            text="Login",
            style="home_btns.TButton",
            # padding=(15, 26)
        )
        self.login_logout_btn.grid(column=1, row=0, sticky=(N, S, E, W))

        
        self.help_btn = ttk.Button(
            self.bottom_frame, 
            text="Help",
            style="home_btns.TButton",
            # padding=(15, 26)
        )
        self.help_btn.grid(column=2, row=0, sticky=(N, S, E, W))

        self.settings_btn = ttk.Button(
            self.bottom_frame, 
            text="Settings",
            style="home_btns.TButton",
            # padding=(15, 26),
            command=self.open_settings
        )
        self.settings_btn.grid(column=3, row=0, sticky=(N, S, E, W))

        self.exit_btn = ttk.Button(
            self.bottom_frame, 
            text="Exit",
            style="home_btns.TButton",
            # padding=(15, 26)
        )
        self.exit_btn.grid(column=4, row=0, sticky=(N, S, E, W))

        for child in self.bottom_frame.winfo_children():
            child.grid_configure(padx=2, pady=5)
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#

    def open_settings(self):
        # settings_menu = Menu(win)
        SettingsWindow(self.root)