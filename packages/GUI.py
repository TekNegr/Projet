#############################################################################################
#                                                                                           #
#                                     DEFINITION                                            #
#                                                                                           #
#############################################################################################
import os
import tkinter as tk
from tkinter import ttk, messagebox
from packages import Screens, DBHandler

#############################################################################################
#                                                                                           #
#                                         CODE                                              #
#                                                                                           #
#############################################################################################

class GUI:
    def __init__(self, DBH : DBHandler) :
        self.root = tk.Tk()
        self.root.title("NASAAAAAAAAAAAAAAAAAH")
        self.root.minsize(400, 300)
        self.screen_manager = Screens.ScreenManager(self)
        self.screen_manager.show_screen("HomeScreen")
        self.dbH = DBH
        
    
    def run(self):
        print("running API...")
        self.root.mainloop()