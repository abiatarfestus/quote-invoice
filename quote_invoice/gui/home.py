from datetime import datetime, date
import random
from quote_invoice.db import operations as db
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from faker import Faker
from moneyed import Money, NAD
from sqlalchemy import and_, or_, create_engine, select
from sqlalchemy.orm import sessionmaker
from quote_invoice.db.models import Customer, Order, OrderItem, Quotation, QuotationItem, Product

class HomeTab():
    def __init__(self, notebook, parent_frame):
        """Configure the home tab page"""
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
            text="Quote & Invoice v0.0.1",
            anchor="center",
            style="heading.TLabel",
        )
        self.heading_lbl.grid(row=0)
        #-------------------------------TOP FRAME ENDS--------------------------------------#
        
        #-------------------------------MID FRAME-------------------------------------------#
        self.mid_frame = ttk.Frame(
            parent_frame, 
            borderwidth=5, 
            # relief="solid"
        )
        self.mid_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        self.mid_frame.columnconfigure(0, weight=1)
        self.mid_frame.columnconfigure(1, weight=1)
        self.mid_frame.rowconfigure(0, weight=1)
        self.mid_frame.rowconfigure(1, weight=1)

        # Labels:
        self.main_menu_lbl = ttk.Label(
            self.mid_frame,
            text="Main Menu",
            anchor="center",
            style="main_menu.TLabel",
            padding=(180,2)
        )
        self.main_menu_lbl.grid(column=0, row=0, columnspan=2)

        # Buttons:
        self.customer_list_btn = ttk.Button(
            self.mid_frame,
            text="Customer List",
            style="home_btns.TButton",
            padding=26
        )
        self.customer_list_btn.grid(column=0, row=1, sticky=E)

        self.customer_btn = ttk.Button(
            self.mid_frame, 
            text="Customer Details",
            style="home_btns.TButton",
            padding=(15, 26)
        )
        self.customer_btn.grid(column=0, row=2, sticky=E)

        self.quotations_btn = ttk.Button(
            self.mid_frame, 
            text="Quotations",
            style="home_btns.TButton",
            padding=26
        )
        self.quotations_btn.grid(column=1, row=1, sticky=W)

        self.orders_invoies_btn = ttk.Button(
            self.mid_frame, 
            text="Orders/Invoices",
            style="home_btns.TButton",
            padding=(15, 26)
        )
        self.orders_invoies_btn.grid(column=1, row=2, sticky=W)

        for child in self.mid_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
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
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        
        # Labels:
        self.creator_lbl = ttk.Label(
            self.bottom_frame,
            text="Created by Festus Abiatar",
            anchor="e",
        )
        self.creator_lbl.grid(column=1, row=0, sticky=(S, E))
        #-------------------------------BOTTOM FRAME ENDS------------------------------------#