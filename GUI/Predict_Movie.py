import tkinter as tk
import pandas as pd
from tkinter import filedialog, Label, Button, Entry, StringVar
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo
from time import strftime
import App as APP
import glob
# ------------------------Import Package CONTROL------------------------
import sys
sys.path.insert(0, 'CONTROL')
from CONTROL_getInfo import CONTROL_getInfo

class Predicit_Movie(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.CONTROL_getInfo = CONTROL_getInfo()
        # set bg cho page predict
        path=glob.glob('img/BG_predict.png')
        self.bg = tk.PhotoImage(file = path)
        self.my_Label = tk.Label(self, image= self.bg)
        self.my_Label.place(relwidth= 1, relheight= 1)
        
        self.initUI()
        
    def initUI(self):

        self.panel_Left()
        self.panel_Right()
        
    def panel_Left(self):
        #set label title
        self.title_Predict = tk.Label(self, text="Predict Movie", font=self.controller.title_font)
        
        # set list chọn dataset
        self.list_Database = tk.StringVar()
        self.list_Database.set("Select database")
        self.option_Database = self.CONTROL_getInfo.get_list_Table()
        self.option_Menu_Database = tk.OptionMenu(self, self.list_Database,*self.option_Database, command=self.select_Database)
         
        #button go back đã được setup
        self.button_Go_Back = tk.Button(self, text="Go back to index",
                           command=lambda: APP.SampleApp.show_frame(self.controller,"Index"))
        
        # set list chọn user
        self.list_Users = tk.StringVar()
        self.list_Users.set("Select users")
        self.option_Users = ['A','B','C']
        self.option_Menu_Users = tk.OptionMenu(self,self.list_Users,*self.option_Users,command=self.select_User)
        
        #set list chọn film
        self.list_Films = tk.StringVar()
        self.list_Films.set("Select films")
        self.option_Film = ['A','X','S']
        self.option_Menu_Film = tk.OptionMenu(self,self.list_Films,*self.option_Film,command=self.select_Film)   
        
        
        #set button dự đoán.
        self.button_Predict = tk.Button(self, text="Start Predict",command=self.perdict_System)
        
        # set vị trí của các label, list, button.
        self.title_Predict.place(x = int(self.winfo_screenwidth()/2.2), y=10)
        self.option_Menu_Database.place(x = int(self.winfo_screenwidth()/4), y = 100)
        self.option_Menu_Users.place(x = int(self.winfo_screenwidth()/2), y = 100)
        self.option_Menu_Film.place(x = int(self.winfo_screenwidth()/1.5), y = 100)
        self.button_Go_Back.place(x = int(self.winfo_screenwidth()/20), y = int(self.winfo_screenheight()/1.2))
        self.button_Predict.place(x = int(self.winfo_screenwidth()/1.2), y = int(self.winfo_screenheight()/1.2))
    

    def panel_Right(self):
        #set ô text page predict
        self.bottom_Display_Perdict = tk.Text(self,width=int(self.winfo_screenwidth()/15),height= int(self.winfo_screenheight()/24))
        self.bottom_Display_Perdict.place(x = int(self.winfo_screenwidth()/4), y = int(self.winfo_screenheight()/5))
        
    # sự kiện cho list chọn database
    def select_Database(self,selection):
        print(selection)
        return 0
    
    #sự kiện cho list chọn user
    def select_User(self,selection):
        print(selection)
        return 0  
    
    #sự kiện cho list chọn film
    def select_Film(self,selection):
        print(selection)
        return 0
    
    #sự kiện cho button dự đoán.    
    def perdict_System(self):
        return 0