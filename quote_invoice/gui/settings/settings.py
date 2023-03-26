from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .folder import FolderSettingsTab
from .general import GeneralSettingsTab
from .user import UserSettingsTab

def get_connection():
    return create_engine(f"sqlite:///app_database.db")

# class DatabaseOps():
engine = get_connection()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class SettingsWindow():
    """ Initialize the settings window of the application"""
    def __init__(self, parent):
        self.settings_window = Toplevel(parent)
        self.settings_window.title("Settings")
        # self.root.option_add('*tearOff', FALSE)
        self.logo = PhotoImage(file='settings_icon.png')
        self.settings_window.iconphoto(False, self.logo)
        # self.style = style()
        self.create_notebook()
        self.configure_rows_columns()
        self.general_settings_tab = self.create_general_settings_tab()
        self.folder_settings_tab = self.create_folder_settings_tab()
        # self.user_settings_tab = self.create_user_settings_tab()
    
    def create_notebook(self):
        """Create a Notebook and Frames"""
        self.notebook = ttk.Notebook(self.settings_window, style="notebook.TNotebook",)
        self.general_settings_frame = ttk.Frame(self.notebook)
        self.folder_settings_frame = ttk.Frame(self.notebook)
        self.user_settings_frame = ttk.Frame(self.notebook)

        # Add tabs/pages to the Notebook
        self.notebook.add(self.general_settings_frame, text="General Settings")
        self.notebook.add(self.folder_settings_frame, text="Folder Settings")
        self.notebook.add(self.user_settings_frame, text="User Settings")
        
        # Grid Notebook
        self.notebook.grid(column=0, row=0, sticky=(N, W, E, S))

    def configure_rows_columns(self):
        """Configure the rows and columns resizing behaviour"""
        # Root
        self.settings_window.columnconfigure(0, weight=1)
        self.settings_window.rowconfigure(0, weight=1)

        self.general_settings_frame.columnconfigure(0, weight=1)
        self.general_settings_frame.rowconfigure(0, weight=1)

        self.folder_settings_frame.columnconfigure(0, weight=1)
        self.folder_settings_frame.rowconfigure(0, weight=1)

        self.user_settings_frame.columnconfigure(0, weight=1)
        self.user_settings_frame.rowconfigure(0, weight=1)

    def create_general_settings_tab(self):
        general_settings_tab = GeneralSettingsTab(self.general_settings_frame)
        return general_settings_tab

    def create_folder_settings_tab(self):
        folder_settings_tab = FolderSettingsTab(self.folder_settings_frame)
        return folder_settings_tab
    
    def create_user_settings_tab(self):
        quote_details_tab = UserSettingsTab(self.user_settings_frame)
        return quote_details_tab