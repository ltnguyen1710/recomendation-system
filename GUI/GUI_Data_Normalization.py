import tkinter as tk
import pandas as pd
from pandastable import Table
from tkinter.messagebox import showinfo
from tkinter import messagebox

# ------------------------Import Package GUI------------------------
import GUI_import as guiImport
import GUI_Result
import App as APP
# ------------------------Import Package CONTROL------------------------
import sys
sys.path.insert(0, 'CONTROL')

class Data_Normalization(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.GUI_Import = guiImport.GUI_import(self)
        self.table = pd.DataFrame()
        self.initUI()

    def initUI(self):
        self.panel_Left()
        self.panel_Top()
        self.panel_Bottom()

    def panel_Left(self):
        self.left = tk.Label(self, text="Select data with CSV file")

        # chọn tập dữ liệu từ máy tính
        self.button = tk.Button(self, text="Import data", command=lambda: self.set_table(self.GUI_Import.import_data()))

        # button quay về page index
        self.button_back = tk.Button(self, text="Go back to menu",
                                     command=lambda: APP.SampleApp.show_frame(self.controller, 'GUI_index'))


        # chọn vị trí của các button, label và text
        self.left.place(x=10, y=10)
        self.button.place(x=10, y=30)
        self.button_back.place(x=10, y=self.winfo_screenheight()*0.9)
        # self.button_back.config(height= 20, width= 20)
        



    def panel_Top(self):
        self.label = tk.Label(self, text="Import Data For System",
                              font=self.controller.title_font)
        self.label.place(x=int(self.winfo_screenwidth()/2.2), y=5)

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
                        text="Clear table", height=10, width=20, command=self.clear_table)
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
        try:
            df = self.table.model.df
        except:
            messagebox.showinfo("Alert", 'Please Import Data...')
        finally:
            return df

    def refresh_table(self):
        """
        Tải lại Table 
        - Input: None
        - Output: None
        """
        
        
        self.table.redraw()

        
    def clear_table(self):
        """
        Xóa Table 
        - Input: None
        - Output: None
        """
        self.table.clearTable()

        
    # sự kiện cho list chọn database
    # def data_Normalization(self):
    #     df = self.get_currentTable()
    #     print(df.dtypes)
    #     select_methods = self.list_methods.get()
    #     if(select_methods=="Machine learning"):
    #         self.set_table(self.CONTROL_ML.Test(df).fillna(value=''))
    #         # self.set_table(self.CONTROL_ML.Test(df))
    #         self.alert_Normalization()
    #     elif(select_methods=="Statistical"):
    #         # self.CONTROL_Sta.Test()
    #         df_prepare = self.CONTROL_Sta.prepare(df)
    #         print(df_prepare.dtypes)
    #         df_label = self.CONTROL_Sta.label_for_non_date_dtype(df_prepare)
    #         df_label = self.CONTROL_Sta.label_for_date_dtype(df_label)
    #         self.CONTROL_Sta.calculate_correof(df_prepare)
    #         print(self.CONTROL_Sta.corrcoef)
    #         # self.GUI_Result = GUI_Result.GUI_Result(self)
    #         self.GUI_Result.df_result = self.CONTROL_Sta.corrcoef.copy()
    #         self.GUI_Result.open_import()
    
    # # sự kiện của button chạy hệ thống
    # def run_Recommendation_System(self):
    #     return 0

    def alert_Normalization(self):
        showinfo('Alert', self.CONTROL_ML.alert())
        self.refresh_table()