from tkinter import *
from tkinter import ttk


class MainWindow:
    def __init__(self, root):

        root.title("Quote & Invoice")

        # Styles
        s = ttk.Style()
        s.configure("notebook.TNotebook.Tab", padding=10, font=(None, 16))
        s.configure("home_btns.TButton", font=(None, 24))
        s.configure("heading.TLabel", font=(None, 31))
        s.configure(
            "main_menu.TLabel", 
            font=(None, 24), 
            background="blue",
            foreground="white"
        )

        # Notebook and Frames
        self.notebook = ttk.Notebook(root, style="notebook.TNotebook",)
        self.home_frame = ttk.Frame(self.notebook)   # first page, which would get widgets gridded into it
        self.customer_list_frame = ttk.Frame(self.notebook)
        self.customer_form_frame = ttk.Frame(self.notebook)
        self.quotations_frame = ttk.Frame(self.notebook)
        self.orders_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.home_frame, text="Home")
        self.notebook.add(self.customer_list_frame, text="Customer List")
        self.notebook.add(self.customer_form_frame, text="Customer Form")
        self.notebook.add(self.quotations_frame, text="Quotations")
        self.notebook.add(self.orders_frame, text="Orders/Invoices")
        
        self.notebook.grid(column=0, row=0, columnspan=2, rowspan=11, sticky=(N, W, E, S))

        # Inside Home Frame
        self.top_frame = ttk.Frame(
            self.home_frame, 
            # padding="3 3 12 12", 
            borderwidth=5, 
            # relief="solid"
        )
        self.mid_frame = ttk.Frame(
            self.home_frame, 
            # padding="3 3 12 12", 
            borderwidth=5, 
            relief="solid"
        )
        self.bottom_frame = ttk.Frame(
            self.home_frame, 
            # padding="3 3 12 12", 
            borderwidth=5, 
            relief="solid"
        )

        self.top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        self.mid_frame.grid(column=0, row=2, columnspan=2, sticky=(SW))
        self.bottom_frame.grid(column=0, row=4, columnspan=2, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)

        self.home_frame.columnconfigure(0, weight=1)
        self.home_frame.columnconfigure(1, weight=1)
        self.home_frame.rowconfigure(0, weight=1)
        self.home_frame.rowconfigure(1, weight=1)
        self.home_frame.rowconfigure(2, weight=1)
        self.home_frame.rowconfigure(3, weight=1)
        self.home_frame.rowconfigure(4, weight=1)

        self.mid_frame.columnconfigure(0, weight=1)
        self.mid_frame.columnconfigure(1, weight=1)
        self.mid_frame.rowconfigure(0, weight=1)
        self.mid_frame.rowconfigure(1, weight=1)
        self.mid_frame.rowconfigure(2, weight=1)
        self.mid_frame.rowconfigure(3, weight=1)
        self.mid_frame.rowconfigure(4, weight=1)

        # LABELS
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

        self.creator_lbl = ttk.Label(
            self.bottom_frame,
            text="Created by Festus Abiatar",
            anchor="center",
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
        self.creator_lbl.grid(row=0, columnspan=12, sticky=E)
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
