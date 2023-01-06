import tkinter as tk
import pandas as pd
from tkinter import filedialog, Label, Button, Entry, StringVar
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo
# ------------------------Import Package GUI------------------------
import sys
sys.path.insert(0, 'GUI')
from GUI_import import GUI_import

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background = "white")
        self.parent = parent
        self.GUI_import = GUI_import(root)
        self.initUI()  
    
    def initUI(self):
        self.parent.title("Recommendation System Application")
        self.panel_Left()
        self.panel_Top()
        self.panel_Bottom()

        
    def panel_Left(self):
        self.left = tk.Label(root, text="Select data with CSV file")
        self.button = tk.Button(root, text="Add new data", command=self.GUI_import.open_import)
        
        self.normalization = tk.Button(root, text="Data normalization",command=self.data_Normalization)
        
        self.runSystem = tk.Button(root, text="Run System",command=self.run_Recommendation_System)
        self.menu= StringVar()
        self.menu.set("Select methods")
        self.drop= tk.OptionMenu(root, self.menu,"Machine learning", "Statistical")
        
        self.t1 = tk.Text(root,width=20, height=4)
        self.left.place(x = 10, y = 10)
        self.button.place(x = 10,y = 30)
        self.t1.place(x = 10,y = 60)
        self.normalization.place(x = 10, y = 150)
        self.drop.place(x = 10, y = 190)
        self.runSystem.place(x = 160, y = 700)
        
    def panel_Top(self):
        self.top = tk.Label(root,text="Detail Dataset")
        self.top.place(x = 900, y = 10)
    
    def panel_Bottom(self):
        self.bottom = tk.Text(root,width=int(width_value/10),height= int(height_value/18))
        self.bottom.place(x = 250, y = 40)
        
        
    
    def data_Normalization(self):
        return 0  
    
    def run_Recommendation_System(self):
        return 0    
    
    
if __name__ == "__main__":
    root = tk.Tk()
    width_value = root.winfo_screenwidth()
    height_value = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (width_value,height_value))
    app = App(root)
    root.resizable(False, False)
    root.mainloop()