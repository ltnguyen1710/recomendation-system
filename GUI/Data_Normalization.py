import tkinter as tk
import pandas as pd
from tkinter import filedialog, Label, Button, Entry, StringVar
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo
# ------------------------Import Package GUI------------------------
import sys
sys.path.insert(0, 'GUI')
from GUI_import import GUI_import
import App as APP

class Data_Normalization(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Data Normalization", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.initUI()
    
    def initUI(self):
        self.panel_Left()
        self.panel_Top()
        self.panel_Bottom()

        
    def panel_Left(self):
        self.left = tk.Label(self, text="Select data with CSV file")
        
        # chọn tập dữ liệu từ máy tính
        self.button = tk.Button(self, text="Add new data", command="")
        
        # button chuẩn hóa dữ liệu
        self.normalization = tk.Button(self, text="Data normalization",command=self.data_Normalization)
       
        # button chay hệ thống
        self.runSystem = tk.Button(self, text="Run System",command=self.run_Recommendation_System)
        
        # button quay về page index
        self.button_back = tk.Button(self, text="Go back to index",
                           command=lambda: APP.SampleApp.show_frame(self.controller,'Index'))
        # chọn định chuẩn dữ liệu
        self.menu= tk.StringVar()
        self.menu.set("Select methods")
        self.drop= tk.OptionMenu(self, self.menu,"Machine learning", "Statistical")
        
        # chọn vị trí của các button, label và text
        self.t1 = tk.Text(self,width=20, height=4)
        self.left.place(x = 10, y = 10)
        self.button.place(x = 10,y = 30)
        self.t1.place(x = 10,y = 60)
        self.normalization.place(x = 10, y = 150)
        self.drop.place(x = 10, y = 190)
        self.runSystem.place(x = 160, y = 700)
        self.button_back.place(x = 50, y = 700)
        
    def panel_Top(self):
        self.top = tk.Label(self,text="Detail Dataset")
        self.top.place(x = 900, y = 10)
    
    def panel_Bottom(self):
        # hiện thị ô text
        self.bottom = tk.Text(self,width=int(self.winfo_screenwidth()/10),height= int(self.winfo_screenheight()/18))
        self.bottom.place(x = 250, y = 40)
        
    # sự kiện của button chuẩn hóa dữ liệu
    def data_Normalization(self):
        return 0
    
    # sự kiện của button chạy hệ thống
    def run_Recommendation_System(self):
        return 0
