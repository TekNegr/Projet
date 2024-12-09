#############################################################################################
#                                                                                           #
#                                     DEFINITION                                            #
#                                                                                           #
#############################################################################################
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os 
#from API_v2.FRONT import API_GUI

#############################################################################################
#                                                                                           #
#                                         CODE                                              #
#                                                                                           #
#############################################################################################

class DBHandler :
    def __init__(self):
        self.TrainDf = pd.DataFrame()
        self.TestDf = pd.DataFrame()
        self.RULDf = pd.DataFrame()
        self.data_types = ["Train", "Test", "RUL"] 
        # self.chosen_data : str = "Train"
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        for type in self.data_types:
            self.load_data(type)
    
    def load_data(self, data_type):
        
        if data_type in ["Train", "Test"]:
            column_names = ['ID', 'Cycle', 'OP1', 'OP2', 'OP3'] + [f'S{i}' for i in range(1, 27)]
        elif data_type == "RUL":
            column_names = ['RUL']
        
        for filename in self.get_filenames(data_type):
            file_path = os.path.join(self.current_directory, filename)
            fd_number = self.get_FD_nb(filename)
            df = pd.read_csv(file_path, sep='\s+', header=None, names = column_names)
            df['FD'] = fd_number
            if data_type == "Train":
                self.TrainDf = pd.concat([self.TrainDf, df], ignore_index=True)
            elif data_type == "Test":
                self.TestDf = pd.concat([self.TestDf, df], ignore_index=True)
            elif data_type == "RUL":
                self.RULDf = pd.concat([self.RULDf, df], ignore_index=True)
    
    def get_filenames(self, data_type: str):
        return [f"data/{data_type}_FD00{d}.txt" for d in range(1, 5)]
    
    def get_FD_nb(self, filename: str):
        return int(filename.split('_FD')[1].split('.')[0])