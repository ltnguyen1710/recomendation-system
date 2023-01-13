import tkinter as tk

from pandastable import Table
from tkinter.messagebox import showinfo

# ------------------------Import Package GUI------------------------
import GUI_import as guiImport
import App as APP
# ------------------------Import Package CONTROL------------------------
import sys
sys.path.insert(0, 'CONTROL')
from CONTROL_ML_Normalization import CONTROL_ML_Normalization
from CONTROL_Statistical_Normalization import CONTROL_Statistical_Normalization

class Data_Normalization(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.GUI_Import = guiImport.GUI_import(self)
        self.CONTROL_ML = CONTROL_ML_Normalization()
        self.CONTROL_Sta = CONTROL_Statistical_Normalization()
        self.initUI()

    def initUI(self):
        self.panel_Left()
        self.panel_Top()
        self.panel_Bottom()

    def panel_Left(self):
        self.left = tk.Label(self, text="Select data with CSV file")

        # chọn tập dữ liệu từ máy tính
        self.button = tk.Button(self, text="Import data", command=lambda: self.set_table(self.GUI_Import.import_data()))

        # button chuẩn hóa dữ liệu
        self.normalization = tk.Button(
            self, text="Data normalization", command=self.data_Normalization)

        # button chay hệ thống
        self.runSystem = tk.Button(
            self, text="Run System", command=self.run_Recommendation_System)

        # button quay về page index
        self.button_back = tk.Button(self, text="Go back to index",
                                     command=lambda: APP.SampleApp.show_frame(self.controller, 'GUI_index'))
        # chọn định chuẩn dữ liệu
        self.list_methods = tk.StringVar()
        self.list_methods.set("Select methods")
        self.drop = tk.OptionMenu(
            self, self.list_methods, "Machine learning", "Statistical")

        # chọn vị trí của các button, label và text
        self.t1 = tk.Text(self, width=20, height=4)
        self.left.place(x=10, y=10)
        self.button.place(x=10, y=30)
        self.t1.place(x=10, y=60)
        self.drop.place(x=10, y=150)
        self.normalization.place(x=10, y=190)
        self.runSystem.place(x=160, y=700)
        self.button_back.place(x=50, y=700)



    def panel_Top(self):
        self.label = tk.Label(self, text="Data Normalization",
                              font=self.controller.title_font)
        self.label.place(x=int(self.winfo_screenwidth()/2.2), y=10)

    def panel_Bottom(self):

        # Để mặc định là Frame để display dễ hơn dạng Text

        # Frame Table
        self.bottom = tk.Frame(self,background='#DCDCDC')
        self.bottom.place(x=self.winfo_screenwidth()*0.18, y=self.winfo_screenheight()*0.05, width=self.winfo_screenwidth() *
                          0.8, height=self.winfo_screenheight()*0.82)
        # Frame Button option
        self.bottom_button_function = tk.Frame(self,background='#DCDCDC')
        self.bottom_button_function.place(
            x=self.winfo_screenwidth()*0.18, y=self.winfo_screenheight()*0.9, width=self.winfo_screenwidth()*0.8, height=self.winfo_screenheight()*0.05)
        # Button Add data into Database
        button_add_data = tk.Button(self.bottom_button_function, text="Add data", height=10, width=20,
                                    command=lambda: self.GUI_Import.open_import(self.get_currentTable()))
        button_add_data.pack(side='left', expand='YES')
        # Button Refresh table
        refresh_table = tk.Button(self.bottom_button_function, text="Refresh table", height=10, width=20,
                                  command=self.refresh_table)
        refresh_table.pack(side='left', expand='YES')                          
        # Button None --- Chưa biết làm gì để dô cho có 
        btt = tk.Button(self.bottom_button_function,
                        text="Button 3", height=10, width=20)
        btt.pack(side='left', expand='YES')
    def set_table(self,data):
        """
        Hiển thị Dataframe lên giao diện
        - Input: Dataframe: data
        - Output: None
        """
        self.table = Table(self.bottom, dataframe=data, showstatusbar=True)
        self.table.show()

    # Lấy dữ liệu table đang hiển thị
    def get_currentTable(self):
        """
        Lấy dữ liệu Dataframe đang hiển thị
        - Input: None
        - Output: Dataframe: data
        """
        df = self.table.model.df
        return df

    def refresh_table(self):
        """
        Tải lại Table 
        - Input: None
        - Output: None
        """
        self.table.redraw()
    
    # sự kiện cho list chọn database
    def data_Normalization(self):
        df = self.get_currentTable()
        select_methods = self.list_methods.get()
        if(select_methods=="Machine learning"):
            self.CONTROL_ML.Test(df)
            self.alert_Normalization()
        elif(select_methods=="Statistical"):
            self.CONTROL_Sta.Test()
    
    # sự kiện của button chạy hệ thống
    def run_Recommendation_System(self):
        return 0

    def alert_Normalization(self):
        showinfo('Alert', self.CONTROL_ML.alert())
        self.refresh_table()