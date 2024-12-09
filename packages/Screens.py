#############################################################################################
#                                                                                           #
#                                     DEFINITION                                            #
#                                                                                           #
#############################################################################################
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from API_v2.FRONT import API_GUI

#############################################################################################
#                                                                                           #
#                                         CODE                                              #
#                                                                                           #
#############################################################################################

class ScreenManager:
    def __init__(self, gui):
        from packages import GUI

        self.gui : GUI  = gui # Reference to the main GUI
        self.current_screen = None
        self.screens = {
            "HomeScreen": HomeScreen,
            "ReadScreen": StatsReaderScreen
        }

    def show_screen(self, screen_name:str):
        """Transition to a specific screen."""
        print(f"showing screen:{screen_name}")
        if self.current_screen:
            self.current_screen.destroy()  # Remove current screen
        screen_class = self.screens.get(screen_name)
         
        if screen_class:
            print(f"{screen_name} selected")
            self.current_screen = screen_class(self)  # Instantiate the screen class
            self.current_screen.pack()  # Pack the new screen
            print(f"Packing {self.current_screen}...")
        else:
            print(f"Screen {screen_name} not found.")

        
class BaseScreen(tk.Frame):
    """A base class for all screens."""
    def __init__(self, manager: ScreenManager):
        
        super().__init__(manager.gui.root)
        
        self.manager = manager
        
    def getScreenHeader(self, Screen_title:str):
        """Create a header for the screen."""
        self.header = tk.Frame(self)
        homeBtn = tk.Button(self.header, text="Home", command=self.goHome)
        headerTitle = tk.Label(self.header, text = Screen_title)
        homeBtn.pack(side=tk.LEFT, padx=10)
        headerTitle.pack(side=tk.RIGHT, padx=10)
        return self.header
        
    def goHome(self):
        self.manager.show_screen("HomeScreen")
   
    def setup_widgets(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def refresh_screen(self):
        print("Refreshing page...")
        for widget in self.winfo_children():  # Destroy all existing widgets
            widget.destroy()
        self.setup_widgets()
        
class HomeScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)
        self.setup_widgets()
        
        
    def setup_widgets(self):
        label = tk.Label(self, text="RAAAAAAAAAH LES TURBOS FANS!!!")
        label.pack(pady=10)
        
        
        btn_read = tk.Button(self, text="Go to Stats Reader screen", command=lambda: self.manager.show_screen("ReadScreen"))
        btn_read.pack(pady=10)
        
        
     
              
class StatsReaderScreen(BaseScreen):
    def __init__(self, manager,datastr:str="Table", data_type:str = "Train"):
        super().__init__(manager)
        self.data_Visu = tk.StringVar(value=datastr)
        self.datas = ["Train", "Test", "RUL"]
        self.data_type = data_type if data_type in self.datas else "Train"
        self.chosen_format = datastr
        self.columns = []
        self.setup_widgets()
    
    def create_selector(self):
        selector_label = tk.Label(self, text="Select Data Visualisor:")
        selector_label.pack(pady=5)
        
        data_Visus = ["Table", "Plot", "Predictions", "interpretation"]
        self.Visuselector = ttk.Combobox(self, textvariable=self.data_Visu, values=data_Visus)
        self.Visuselector.bind("<<ComboboxSelected>>", self.on_data_Visu_selected)
        self.Visuselector.pack(pady=5)
        
                
    def on_data_Visu_selected(self, event):
        self.chosen_format = self.data_Visu.get()
        self.refresh_screen()
        
    def setup_widgets(self):
        self.getScreenHeader("Stats reader Screen").pack(pady=10)
        self.create_selector()
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(pady=10)
       
        self.update_columns()
        
        
        self.setup_visus()
        self.setup_btn_frame()
        
        
    def populate_table(self, data):
        if self.chosen_format == "Table" or self.chosen_format == "Prediciton":
            for row in self.tree.get_children():
                self.tree.delete(row)
            for index, row in data.iterrows():
                self.tree.insert("", "end", values=row.tolist())
            
    def update_columns(self):
        if self.data_type in self.datas:
            if self.data_type == "Train":
                self.columns = ('FD','ID', 'Cycle', 'OP1', 'OP2', 'OP3',f'S{i}' for i in range(1, 27))
            elif self.data_type == "Test":
                self.columns = ("Jockey", "Rank", "starts", "Win", "Place", "Show", "Win%", "Top3%")
            elif self.data_type == "RUL":
                self.columns = ("RUL")
            else:
                self.columns = []
     
    def refresh_screen(self):
        super().refresh_screen()
        self.update_columns()
        data = self.fetch_data(self.data_type.get()) 
        if data is not None and not data.empty:
            self.populate_table(data)
        else:
            self.populate_table(pd.DataFrame(columns=self.columns)) 
   
    def setup_btn_frame(self):
        self.btn_frame = tk.Frame(self)
        
        if self.chosen_format =="Table" or self.chosen_format == "Predictions":
            pass
        
        elif self.chosen_format =="Plot":
            pass
        
        
        elif self.chosen_format =="Interpretation":
            pass
        
        self.btn_frame.pack(pady=10)
        pass
   
    def setup_visus(self, plt_cv:FigureCanvasTkAgg=None): 
        if self.chosen_format== "Table" or self.chosen_format == "Predictions":
            self.setup_table_view()  
        elif self.chosen_format == "Plot" and plt_cv:
            self.setup_plot_view(plt_cv)
        elif self.chosen_format == "Interpretation":
            pass
        
    def setup_table_view(self):
        """Setup the table view."""
        messagebox.showinfo("DEBBUGGER", f"Setting up table of {self.chosen_format}")
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill =tk.Y)    
       
      
    def setup_plot_view(self, plot : FigureCanvasTkAgg):
        pass
    
    
    def setup_interpretation_view(self):
        pass

           
    def fetch_data(self, data_type):
        if data_type=="Train":
            return self.manager.gui.dbH.TrainDf
        elif data_type=="Test":
            return self.manager.gui.dbH.TestDf
        elif data_type=="RUL":
            return self.manager.gui.dbH.RULDf
        
        
