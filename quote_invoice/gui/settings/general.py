from tkinter import *
from tkinter import ttk
from tkinter import filedialog


# filename = filedialog.askopenfilename()
# filename = filedialog.asksaveasfilename()
# dirname = filedialog.askdirectory()

class GeneralSettingsTab():
    def __init__(self, parent_frame):
        # self.settings_window = settings_window
        self.parent_frame = parent_frame 
        #-------------------------------------TOP FRAME-----------------------------------#
        # Frames:
        self.top_frame = ttk.Frame(
            self.parent_frame,
            borderwidth=5, 
            # relief="solid"
        )
        self.top_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        
        # Labels:
        self.heading_lbl = ttk.Label(
            self.top_frame,
            text="General Settings",
            anchor="center",
            style="heading2.TLabel",
        )
        self.heading_lbl.grid(column=0, row=0, sticky=(N, S, W, E))
        #-------------------------------TOP FRAME ENDS--------------------------------------#

        #-------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(
            self.parent_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        self.mid_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        
        # Labels:
        self.vat_rate_lbl = ttk.Label(
            self.mid_frame,
            text="Vat Rate (%):",
            anchor=W,
            # style="heading.TLabel",
        )
        self.vat_rate_lbl.grid(column=0, row=0, sticky=(W, ))

        self.quote_validity_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Validity Period (days):",
            anchor=W,
            # style="heading.TLabel",
        )
        self.quote_validity_lbl.grid(column=0, row=1, sticky=(W, ))

        # Entries:
        # self.vat_rate_ent = ttk.Entry(
        #     self.mid_frame,
        #     width=40,
        #     # textvariable="",
        #     # anchor="",
        #     # style="heading.TLabel",
        # )
        # # self.id_ent.insert(0, "New")
        # self.vat_rate_ent.grid(column=1, columnspan=2, row=0, sticky=(N, S, E, W))

        # self.quote_validity_ent = ttk.Entry(
        #     self.mid_frame,
        #     width=40,
        #     # textvariable="",
        #     # anchor="",
        #     # style="heading.TLabel",
        # )
        # self.quote_validity_ent.grid(column=1, columnspan=2, row=1, sticky=(N, S, E, W))

        # Spinboxes:
        self.vat_rate_spx = ttk.Spinbox(
            self.mid_frame,
            from_=0.0,
            to=100.0,
        )
        self.vat_rate_spx.grid(column=1, columnspan=2, row=0, sticky=(S, N, E, W))

        self.quote_validity_spx = ttk.Spinbox(
            self.mid_frame,
            from_=1,
            to=100,
        )
        self.quote_validity_spx.grid(column=1, columnspan=2, row=1, sticky=(S, N, E, W))

         # Buttons:
        self.save_btn = ttk.Button(
            self.mid_frame, 
            text="Save",
            # style="home_btns.TButton",
            padding=5,
            # command=self.save_changes
        )
        self.save_btn.grid(column=1, row=2, pady=2, sticky=(N, S, E, W))

        self.cancel_btn = ttk.Button(
            self.mid_frame, 
            text="Cancel",
            # style="home_btns.TButton",
            padding=5,
            # command=self.view_customer_orders
        )
        self.cancel_btn.grid(column=2, row=2, pady=2, sticky=(N, S, E, W))
        
        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            self.parent_frame,
            borderwidth=5, 
            # relief="solid"
        )
        self.bottom_frame.grid(column=0, row=2, sticky=(N, W, E, S))

       
        
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#