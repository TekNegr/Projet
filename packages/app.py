from .GUI import GUI
from .dbhandler import DBHandler
import os
import tkinter as tk
from tkinter import ttk, messagebox

class App : 
    def __init__(self):
        self.dbH = DBHandler()
        self.GUI = GUI(self.dbH)
        self.GUI.run()