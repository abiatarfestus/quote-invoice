from tkinter import *
from tkinter import messagebox, ttk

from quote_invoice.db.models import Settings
from quote_invoice.db.operations import (
    add_settings,
    get_settings,
    update_general_settings,
)


class GeneralSettingsTab:
    def __init__(self, session, parent_frame):
        self.session = session
        self.parent_frame = parent_frame
        # -------------------------------------TOP FRAME-----------------------------------#
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
        # -------------------------------TOP FRAME ENDS--------------------------------------#

        # -------------------------------MID FRAME-------------------------------------------#
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
        self.vat_rate_lbl.grid(column=0, row=0, sticky=(W,))

        self.quote_validity_lbl = ttk.Label(
            self.mid_frame,
            text="Quote Validity Period (days):",
            anchor=W,
            # style="heading.TLabel",
        )
        self.quote_validity_lbl.grid(column=0, row=1, sticky=(W,))

        # Spinboxes:
        self.vat_rate_spx = ttk.Spinbox(
            self.mid_frame, from_=0.0, to=100.0, format="%.2f", increment=0.01
        )
        # self.vat_rate_spx.state(['readonly'])
        self.vat_rate_spx.grid(column=1, columnspan=2, row=0, sticky=(S, N, E, W))

        self.quote_validity_spx = ttk.Spinbox(
            self.mid_frame,
            from_=1,
            to=100,
        )
        # self.quote_validity_spx.state(['readonly'])
        self.quote_validity_spx.grid(column=1, columnspan=2, row=1, sticky=(S, N, E, W))

        # Buttons:
        self.save_btn = ttk.Button(
            self.mid_frame,
            text="Save",
            # style="home_btns.TButton",
            padding=5,
            command=self.add_or_update_settings,
        )
        self.save_btn.grid(column=0, row=2, pady=2, sticky=(N, S, E, W))

        self.cancel_btn = ttk.Button(
            self.mid_frame,
            text="Cancel",
            # style="home_btns.TButton",
            padding=5,
            command=self.close_window,
        )
        self.cancel_btn.grid(column=1, columnspan=2, row=2, pady=2, sticky=(N, S, E, W))

        for child in self.mid_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)

        # -------------------------------MID FRAME ENDS---------------------------------------#

        # -------------------------------BOTTOM FRAME-----------------------------------------#
        # Frames:
        self.bottom_frame = ttk.Frame(
            self.parent_frame,
            borderwidth=5,
            # relief="solid"
        )
        self.bottom_frame.grid(column=0, row=2, sticky=(N, W, E, S))
        # -------------------------------BOTTOM FRAME ENDS------------------------------------#
        self.populate_settings()

    def populate_settings(self):
        settings = get_settings(self.session)
        # print(f"CURRENT SETTINGS: {settings}")
        if settings:
            self.vat_rate_spx.insert(0, settings.vat_rate)
            self.quote_validity_spx.insert(0, settings.quote_validity)

    def close_window(self):
        self.parent_frame.master.master.destroy()

    def add_or_update_settings(self):
        try:
            vat_rate = float(self.vat_rate_spx.get())
            quote_validity = int(self.quote_validity_spx.get())
        except ValueError:
            messagebox.showerror(
                message="Value Error: Please ensure that VAT rate is a float and quote validity is an integer.",
                title="Error",
            )
        settings = get_settings(self.session)
        if not settings:
            try:
                # print("CALLING ADD SETTINGS FROM GENERAL")
                add_settings(
                    self.session, vat_rate=vat_rate, quote_validity=quote_validity
                )
                messagebox.showinfo(
                    message="Settings successfully created!", title="Success"
                )
            except Exception as e:
                messagebox.showerror(message=e, title="Error")
        else:
            try:
                # print("CALLING UPDATE SETTINGS FROM GENERAL")
                update_general_settings(self.session, vat_rate, quote_validity)
                messagebox.showinfo(
                    message="Settings successfully updated!", title="Success"
                )
            except Exception as e:
                messagebox.showerror(message=e, title="Error")
        self.parent_frame.master.master.lift()
