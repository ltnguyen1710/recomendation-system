from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import pandas as pd
from tkinter import filedialog as fd
from tkinter.messagebox import askyesno
import time
import GUI_Predict_Movie as PM



# ------------------------Import Package CONTROL------------------------
import sys
sys.path.insert(0, 'CONTROL')
from CONTROL_import import CONTROL_import




class GUI_import:
    def __init__(self, root):
        self.single_import = None
        self.CONTROL_import = CONTROL_import()

        self.root = root
        # self.root.bind("<<PhishDoneEvent>>", self.report_done)
    def generate_reports(self):
        table_name = self.input_name_table.get(1.0, "end-1c")
        
        self.CONTROL_import.add_data(table_name,self.data_to_addinto_DTB)

    def run_report(self):
        self.generate_reports()
        self.root.event_generate("<<PhishDoneEvent>>") # yes, this is using tkinter in a thread, but some tkinter methods are ok to use in threads

    def import_data(self):
        """
        Giao diện tải lên file .csv
        - Input: None
        - Output: Dataframe: data
        """
        # Định dạng file Import .CSV
        filetypes = (
            ('text files', '*.csv'),
            ('All files', '*.*')
        )
        # Mở giao diện chọn file
        filenames = fd.askopenfilenames(
            title='Open files',
            initialdir='/',
            filetypes=filetypes)
        path = ''.join(filenames)  # Convert Filenames to Str
        df = pd.read_csv(path)
        
        return df

    def close_import(self):
        """
        Kiểm soát cửa sổ bật lên là DUY NHẤT với biến self.single_import
        """
        self.single_import
        self.single_import.destroy()
        self.single_import = None

    def open_import(self, df):
        """
        Kiểm soát cửa sổ bật lên là DUY NHẤT với biến self.single_import
        """
        if df.empty:
            print('DataFrame is empty!')
        else:
            self.single_import
            if self.single_import is None:
                self.single_import = Toplevel(self.root)
                self.window_height = 250
                self.window_width = 250
                self.single_import.title("Add data")

                # ----------- Mở cửa sổ chính giữa màn hình-----------

                self.screen_width = self.root.winfo_screenwidth()
                self.screen_height = self.root.winfo_screenheight()
                # Coordinates of the upper left corner of the window to make the window appear in the center
                x_cordinate = int((self.screen_width/2) - (self.window_width/2))
                y_cordinate = int((self.screen_height/2) - (self.window_height/2))
                
                self.single_import.geometry("{}x{}+{}+{}".format(self.window_width,
                                                                self.window_height, x_cordinate, y_cordinate))
                # ----------- Mở cửa sổ chính giữa màn hình-----------

                self.data_to_addinto_DTB = df

                # Button_add__data
                self.confirm_button = ttk.Button(
                    self.single_import,
                    text='Add data',
                    command=lambda: self.confirm()
                )

                label_table_name = ttk.Label(
                    self.single_import, text="Input table name: ")
                label_table_name.grid(column=0, row=0, sticky='w', padx=5, pady=5)

                self.input_name_table = Text(
                    self.single_import, height=2, width=25)
                self.input_name_table.grid(
                    column=0, row=1, sticky='w', padx=5, pady=5)

                self.confirm_button.grid(column=0, row=2, sticky='w', padx=85, pady=10)
            
                self.root.bind("<<PhishDoneEvent>>", self.report_done)
                # assign to closing button [X]
                self.single_import.protocol("WM_DELETE_WINDOW", self.close_import)
            else:
                print("Add new already exists")
    
    def confirm(self):
        """
        Xác nhận (Yes-No) thêm dữ liệu vào Database
        - Input: Dataframe: data
        - Output: None
        """
        answer = askyesno(title='Confirmation',
                          message='Are you sure?')
        if answer:
            self.do_reports()

    def do_reports(self):
        # note this makes a new widget with every click ... this is bad. Refactor to reuse the widget. 
        self.pbar = ttk.Progressbar(self.single_import, mode="indeterminate")
        self.pbar.grid(column=0, row=3, sticky='ew', padx=5, pady=5)
        t1 = threading.Thread(target = self.run_report)
        t1.start()
        self.pbar.start()  
    
    def report_done(self, event=None,*arg):
        self.pbar.stop()
        messagebox.showinfo("Alert", self.CONTROL_import.show_alert())
        self.close_import()
