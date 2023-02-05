
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import askyesno
from pandastable import Table
import time


# ------------------------Import Package CONTROL------------------------
import sys
sys.path.insert(0, 'CONTROL')
from CONTROL_import import CONTROL_import


class GUI_Result(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self)
        self.single_import = None
        self.CONTROL_import = CONTROL_import()
        self.df_result = pd.DataFrame()
        self.root = root
        # self.root.bind("<<PhishDoneEvent>>", self.report_done)

    def generate_reports(self):
        table_name = self.input_name_table.get(1.0, "end-1c")

        self.CONTROL_import.add_data(table_name, self.data_to_addinto_DTB)

    def run_report(self):
        self.generate_reports()
        # yes, this is using tkinter in a thread, but some tkinter methods are ok to use in threads
        self.root.event_generate("<<PhishDoneEvent>>")

    # def import_data(self):
    #     """
    #     Giao diện tải lên file .csv
    #     - Input: None
    #     - Output: Dataframe: data
    #     """
    #     # Định dạng file Import .CSV
    #     filetypes = (
    #         ('text files', '*.csv'),
    #         ('All files', '*.*')
    #     )
    #     # Mở giao diện chọn file
    #     filenames = fd.askopenfilenames(
    #         title='Open files',
    #         initialdir='/',
    #         filetypes=filetypes)
    #     path = ''.join(filenames)  # Convert Filenames to Str
    #     df = pd.read_csv(path)
    #     return df

    def close_import(self):
        """
        Kiểm soát cửa sổ bật lên là DUY NHẤT với biến self.single_import
        """
        self.single_import
        self.single_import.destroy()
        self.single_import = None

    def open_import(self):
        """
        Kiểm soát cửa sổ bật lên là DUY NHẤT với biến self.single_import
        """
        self.single_import
        if self.single_import is None:
            self.single_import = Toplevel(self.root)
            self.window_height = self.winfo_screenheight()
            self.window_width = self.winfo_screenwidth()
            self.single_import.title("Result")

            # ----------- Mở cửa sổ chính giữa màn hình-----------

            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()
            # Coordinates of the upper left corner of the window to make the window appear in the center
            x_cordinate = int((self.screen_width/2) - (self.window_width/2))
            y_cordinate = int((self.screen_height/2) - (self.window_height/2))

            self.single_import.geometry("{}x{}+{}+{}".format(self.window_width,
                                                             self.window_height, x_cordinate, y_cordinate))
            # ----------- Mở cửa sổ chính giữa màn hình-----------

            # Frame Table
            # self.bottom = tk.Frame(self.single_import, background='#DCDCDC')
            # self.bottom.place(x=self.winfo_screenwidth()*0.18, y=self.winfo_screenheight()*0.2, width=self.winfo_screenwidth() *
            #                 0.6, height=self.winfo_screenheight()*0.7)

            # set list chọn Features
            self.list_Features = tk.StringVar()
            self.list_Features.set("Select features")
            self.option_Features = self.df_result.columns.tolist()
            self.option_Menu_Features = tk.OptionMenu(
                self.single_import, self.list_Features, *self.option_Features, command=self.select_Feature)

            self.bottom_Display_Perdict = tk.Text(self.single_import, width=int(
            self.winfo_screenwidth()/15), height=int(self.winfo_screenheight()/24))
            self.bottom_Display_Perdict.place(
            x=int(self.winfo_screenwidth()/4), y=int(self.winfo_screenheight()/5))
            # Button_add__data
            # self.confirm_button = Button(
            #     self.single_import,
            #     text='Add data',
            #     command=lambda: self.confirm()

            # )

            # label_table_name = ttk.Label(
            #     self.single_import, text="Input table name: ")
            # label_table_name.grid(column=0, row=0, sticky='w', padx=5, pady=5)

            # self.input_name_table = Text(
            #     self.single_import, height=2, width=25)
            # self.input_name_table.grid(
            #     column=0, row=1, sticky='w', padx=5, pady=5)

            # self.confirm_button.grid(
            #     column=0, row=2, sticky='w', padx=85, pady=10)
            self.option_Menu_Features.grid( column=0, row=1, sticky='w', padx=5, pady=5)

            self.root.bind("<<PhishDoneEvent>>", self.report_done)
            # assign to closing button [X]
            self.single_import.protocol("WM_DELETE_WINDOW", self.close_import)
        else:
            print("Add new already exists")

        # sự kiện cho list chọn user
    def select_Feature(self, *args):
        print(self.list_Features.get())
        # self.chosen_feature = self.CONTROL_getInfo.get_user_info_by_id(self.list_Features.get())
        rank = self.df_result.sort_values(by=[self.list_Features.get()], ascending=False)[
            self.list_Features.get()]
        # self.set_table(pd.DataFrame(rank))
        self.bottom_Display_Perdict.delete(1.0,'end-1c')
        self.bottom_Display_Perdict.insert("end-1c", "Predict result: "+str(rank))
        return 0

    def set_table(self, data):
        """
        Hiển thị Dataframe lên giao diện
        - Input: Dataframe: data
        - Output: None
        """
        self.table = Table(self.bottom, dataframe=data, showstatusbar=True)
        self.table.show()

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
        t1 = threading.Thread(target=self.run_report)
        t1.start()
        self.pbar.start()

    def report_done(self, event=None, *arg):
        self.pbar.stop()
        messagebox.showinfo("Alert", self.CONTROL_import.show_alert())
        self.close_import()
