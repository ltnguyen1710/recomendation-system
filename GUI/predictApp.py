import tkinter as tk
import pandas as pd
from tkinter import filedialog, Label, Button, Entry, StringVar
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo
from time import strftime


class predictApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background = "white")
        self.parent = parent
        self.initUI()  
    
    def initUI(self):
        self.parent.title("Predict Application")
        self.panel_Left()
        self.panel_Right()


        
    def panel_Left(self):
        self.left = tk.Label(root, text="Select the following attributes",font=("Arial", 15))
        
        self.list_Database = StringVar()
        self.list_Database.set("Select database")
        self.option_Database = ['X','Y','C','Z']
        self.option_Menu_Database = tk.OptionMenu(root, self.list_Database,*self.option_Database, command=self.select_Database)
         
        
    
        self.list_Users = StringVar()
        self.list_Users.set("Select users")
        self.option_Users = ['A','B','C']
        self.option_Menu_Users = tk.OptionMenu(root,self.list_Users,*self.option_Users,command=self.select_User)
        
        self.list_Films = StringVar()
        self.list_Films.set("Select films")
        self.option_Film = ['A','X','S']
        self.option_Menu_Film = tk.OptionMenu(root,self.list_Films,*self.option_Film,command=self.select_Film)   
        
        
        
        self.button_Predict = tk.Button(root, text="Start Predict",command=self.perdict_System)
        
        self.left.place(x = int(width_value/14), y = int(height_value/40))
        self.option_Menu_Database.place(x = int(width_value/60), y = 100)
        self.option_Menu_Users.place(x = int(width_value/8), y = 100)
        self.option_Menu_Film.place(x = int(width_value/4.5), y = 100)
        self.button_Predict.place(x = int(width_value/3), y = int(height_value/1.5))
    

    def panel_Right(self):
        self.top_Label_Perdict = tk.Label(root,text="Perdict",font=("Arial", 15))
        self.top_Label_Perdict.place(x = int(width_value/1.58), y = int(height_value/40))
        self.bottom_Display_Perdict = tk.Text(root,width=int(width_value/15),height= int(height_value/25))
        self.bottom_Display_Perdict.place(x = int(width_value/2.5), y = int(height_value/10))
        
    
    def select_Database(self):
        return 0
    
    def select_User(self):
        return 0    
    
    def select_Film(self):
        return 0
        
    def perdict_System(self):
        return 0
        
    
if __name__ == "__main__":
    root = tk.Tk()
    width_value = root.winfo_screenwidth()
    height_value = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (width_value,height_value))
    app = predictApp(root)
    root.resizable(False, False)
    root.mainloop()