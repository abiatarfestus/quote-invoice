from tkinter import *
from tkinter import ttk
from tkinter import filedialog


# filename = filedialog.askopenfilename()
# filename = filedialog.asksaveasfilename()
# dirname = filedialog.askdirectory()

class SettingsWindow():
    def __init__(self, parent):
        self.window = Toplevel(parent)    
        #-------------------------------------TOP FRAME-----------------------------------#
        # Frames:
        self.top_frame = ttk.Frame(
            self.window,
            borderwidth=5, 
            # relief="solid"
        )
        self.top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        
        # Labels:
        self.heading_lbl = ttk.Label(
            self.top_frame,
            text="Directories Settings",
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0, sticky=(N, S, W, E))
        #-------------------------------TOP FRAME ENDS--------------------------------------#

        #-------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(
            self.window, 
            borderwidth=5, 
            # relief="solid"
        )
        self.mid_frame.grid(row=1, sticky=(N, W, E, S))
        # Labels:
        self.id_lbl = ttk.Label(
            self.mid_frame,
            text="Quotation Template",
            anchor=W,
            # style="heading.TLabel",
        )
        self.id_lbl.grid(column=0, row=0, sticky=(W, ))

        self.type_lbl = ttk.Label(
            self.mid_frame,
            text="Output Folder",
            anchor=W,
            # style="heading.TLabel",
        )
        self.type_lbl.grid(column=0, row=1, sticky=(W, ))

        # Entries:
        self.quote_template_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        # self.id_ent.insert(0, "New")
        self.quote_template_ent.grid(column=1, columnspan=2, row=0, sticky=(N, S, E, W))

        self.output_folder_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.output_folder_ent.grid(column=1, columnspan=2, row=1, sticky=(N, S, E, W))

        # Buttons:
        self.select_template_btn = ttk.Button(
            self.mid_frame,
            text="Select Template",
            # style="home_btns.TButton",
            padding=5,
            # command=self.select_template
        )
        self.select_template_btn.grid(column=3, row=0, sticky=(E, W))

        self.select_output_folder_btn = ttk.Button(
            self.mid_frame,
            text="Select Output Folder",
            # style="home_btns.TButton",
            padding=5,
            # command=self.select_output_folder
        )
        self.select_output_folder_btn.grid(column=3, row=1, sticky=(N, S, E, W))

        # Buttons:
        self.save_btn = ttk.Button(
            self.mid_frame, 
            text="Save",
            # style="home_btns.TButton",
            padding=5,
            # command=self.save_changes
        )
        self.save_btn.grid(column=0, columnspan=2, row=2, pady=2, sticky=(N, S, E, W))

        self.cancel_btn = ttk.Button(
            self.mid_frame, 
            text="Cancel",
            # style="home_btns.TButton",
            padding=5,
            # command=self.view_customer_orders
        )
        self.cancel_btn.grid(column=2, columnspan=2, row=2, pady=2, sticky=(N, S, E, W))
        
        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            self.window,
            borderwidth=5, 
            # relief="solid"
        )
        self.bottom_frame.grid(row=2, sticky=(N, W, E, S))

        # # Buttons:
        # self.save_btn = ttk.Button(
        #     self.bottom_frame, 
        #     text="Save",
        #     # style="home_btns.TButton",
        #     padding=5,
        #     # command=self.save_changes
        # )
        # self.save_btn.grid(row=0, sticky=(N, S, E, W))

        # self.cancel_btn = ttk.Button(
        #     self.bottom_frame, 
        #     text="Cancel",
        #     # style="home_btns.TButton",
        #     padding=5,
        #     # command=self.view_customer_orders
        # )
        # self.cancel_btn.grid(column=3, columnspan=3, row=0, sticky=(N, S, E, W))
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#