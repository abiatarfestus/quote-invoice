from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class FolderSettingsTab():
    def __init__(self, parent_frame):
        # self.parent_window = parent_window
        self.parent_frame = parent_frame 
        #-------------------------------------TOP FRAME-----------------------------------#
        # Frames:
        self.top_frame = ttk.Frame(
            self.parent_frame,
            borderwidth=5, 
            # relief="solid"
        )
        self.top_frame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        
        # Labels:
        self.heading_lbl = ttk.Label(
            self.top_frame,
            text="Folder Settings",
            anchor="center",
            style="heading2.TLabel",
        )
        self.heading_lbl.grid(row=0, sticky=(N, S, W, E))
        #-------------------------------TOP FRAME ENDS--------------------------------------#

        #-------------------------------MID FRAME-------------------------------------------#
        # Frames:
        self.mid_frame = ttk.Frame(
            self.parent_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        self.mid_frame.grid(row=1, sticky=(N, W, E, S))
        # Labels:
        self.quote_template_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Template:",
            anchor=W,
            # style="heading.TLabel",
        )
        self.quote_template_lbl.grid(column=0, row=0, sticky=(W, ))

        self.quote_output_folder_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Output Folder:",
            anchor=W,
            # style="heading.TLabel",
        )
        self.quote_output_folder_lbl.grid(column=0, row=1, sticky=(W, ))

        self.invoice_template_lbl = ttk.Label(
            self.mid_frame,
            text="Invoice Template:",
            anchor=W,
            # style="heading.TLabel",
        )
        self.invoice_template_lbl.grid(column=0, row=2, sticky=(W, ))

        self.invoice_output_folder_lbl = ttk.Label(
            self.mid_frame,
            text="Invoice Output Folder:",
            anchor=W,
            # style="heading.TLabel",
        )
        self.invoice_output_folder_lbl.grid(column=0, row=3, sticky=(W, ))

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

        self.quote_output_folder_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.quote_output_folder_ent.grid(column=1, columnspan=2, row=1, sticky=(N, S, E, W))

        self.invoice_template_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        # self.id_ent.insert(0, "New")
        self.invoice_template_ent.grid(column=1, columnspan=2, row=2, sticky=(N, S, E, W))

        self.invoice_output_folder_ent = ttk.Entry(
            self.mid_frame,
            width=40,
            # textvariable="",
            # anchor="",
            # style="heading.TLabel",
        )
        self.invoice_output_folder_ent.grid(column=1, columnspan=2, row=3, sticky=(N, S, E, W))


        # Buttons:
        self.select_quote_template_btn = ttk.Button(
            self.mid_frame,
            text="Select Quote Template",
            # style="home_btns.TButton",
            padding=5,
            command=self.set_quote_template
        )
        self.select_quote_template_btn.grid(column=3, row=0, sticky=(E, W))

        self.select_quote_output_folder_btn = ttk.Button(
            self.mid_frame,
            text="Select Quote Output Folder",
            # style="home_btns.TButton",
            padding=5,
            command=self.set_quote_output_folder
        )
        self.select_quote_output_folder_btn.grid(column=3, row=1, sticky=(N, S, E, W))

        self.select_invoice_template_btn = ttk.Button(
            self.mid_frame,
            text="Select Invoice Template",
            # style="home_btns.TButton",
            padding=5,
            command=self.set_invoice_template
        )
        self.select_invoice_template_btn.grid(column=3, row=2, sticky=(E, W))

        self.select_invoice_output_folder_btn = ttk.Button(
            self.mid_frame,
            text="Select Invoice Output Folder",
            # style="home_btns.TButton",
            padding=5,
            command=self.set_invoice_output_folder
        )
        self.select_invoice_output_folder_btn.grid(column=3, row=3, sticky=(N, S, E, W))

        # Buttons:
        self.save_btn = ttk.Button(
            self.mid_frame, 
            text="Save",
            # style="home_btns.TButton",
            padding=5,
            # command=self.save_changes
        )
        self.save_btn.grid(column=0, columnspan=2, row=4, pady=2, sticky=(N, S, E, W))

        self.cancel_btn = ttk.Button(
            self.mid_frame, 
            text="Cancel",
            # style="home_btns.TButton",
            padding=5,
            command=self.close_window
        )
        self.cancel_btn.grid(column=2, columnspan=2, row=4, pady=2, sticky=(N, S, E, W))
        
        #-------------------------------MID FRAME ENDS---------------------------------------#

        #-------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            self.parent_frame,
            borderwidth=5, 
            # relief="solid"
        )
        self.bottom_frame.grid(row=2, sticky=(N, W, E, S))
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#

    def set_quote_template(self):
        file_path = filedialog.askopenfilename()
        self.quote_template_ent.delete(0, END)
        self.quote_template_ent.insert(0, file_path)
        self.parent_frame.master.master.lift()           
        print(file_path)

    def set_quote_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.quote_output_folder_ent.delete(0, END)
        self.quote_output_folder_ent.insert(0, folder_path)
        self.parent_frame.master.master.lift()     
        print(folder_path)

    def set_invoice_template(self):
        file_path = filedialog.askopenfilename()
        self.invoice_template_ent.delete(0, END)
        self.invoice_template_ent.insert(0, file_path)
        self.parent_frame.master.master.lift()           
        print(file_path)

    def set_invoice_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.invoice_output_folder_ent.delete(0, END)
        self.invoice_output_folder_ent.insert(0, folder_path)
        self.parent_frame.master.master.lift()     
        print(folder_path)

    def close_window(self):
        self.parent_frame.master.master.destroy()