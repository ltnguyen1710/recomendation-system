import glob
import App as APP
from time import strftime
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile
from tkinter import filedialog, Label, Button, Entry, StringVar
from pandastable import Table
import pandas as pd
import tkinter as tk
# ------------------------Import Package CONTROL------------------------
import sys
sys.path.insert(0, 'CONTROL')
from CONTROL_getInfo import CONTROL_getInfo
from CF import CF

class Predicit_Movie(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.CONTROL_getInfo = CONTROL_getInfo()
        # set bg cho page predict
        path = glob.glob('img/BG_predict.png')
        self.bg = tk.PhotoImage(file=path)
        self.my_Label = tk.Label(self, image=self.bg)
        self.my_Label.place(relwidth=1, relheight=1)

        self.initUI()

    def initUI(self):

        self.panel_Left()
        # self.panel_Right()

    def panel_Left(self):
        # Frame Table
        self.bottom = tk.Frame(self, background='#DCDCDC')
        self.bottom.place(x=self.winfo_screenwidth()*0.18, y=self.winfo_screenheight()*0.2, width=self.winfo_screenwidth() *
                          0.6, height=self.winfo_screenheight()*0.7)

        # set label title
        self.title_Predict = tk.Label(
            self, text="Predict Movie", font=self.controller.title_font)

        # set list chọn dataset
        self.list_Database = tk.StringVar()
        self.list_Database.set("Select database")
        self.option_Database = self.CONTROL_getInfo.get_list_Table()
        self.option_Menu_Database = tk.OptionMenu(
            self, self.list_Database, *self.option_Database, command=self.select_Database)

        # button go back đã được setup
        self.button_Go_Back = tk.Button(self, text="Go back to index",
                                        command=lambda: APP.SampleApp.show_frame(self.controller, "GUI_index"))

        # set list chọn method
        self.list_Methods = tk.StringVar()
        self.list_Methods.set("Select method")
        self.option_Methods = ['user-user','item-item']
        self.option_Menu_Methods = tk.OptionMenu(
            self, self.list_Methods, *self.option_Methods , command=self.select_Method)

        # set list chọn user
        # self.list_Users = tk.StringVar()
        # self.list_Users.set("Select users")
        # self.option_Users = ['A', 'B', 'C']
        # self.option_Menu_Users = tk.OptionMenu(
        #     self, self.list_Users, *self.option_Users, command=self.select_User)

        # set list chọn film
        # self.list_Films = tk.StringVar()
        # self.list_Films.set("Select films")
        # self.option_Film = ['A', 'X', 'S']
        # self.option_Menu_Film = tk.OptionMenu(
        #     self, self.list_Films, *self.option_Film, command=self.select_Film)

        # set button dự đoán.
        self.button_Predict = tk.Button(
            self, text="Start Predict", command=self.perdict_System)

        # set vị trí của các label, list, button.
        self.title_Predict.place(x=int(self.winfo_screenwidth()/2.2), y=10)
        self.option_Menu_Database.place(
            x=int(self.winfo_screenwidth()/4), y=100)
        self.option_Menu_Methods.place(x=int(self.winfo_screenwidth()/2), y=100)
        # self.option_Menu_Film.place(x=int(self.winfo_screenwidth()/1.5), y=100)
        self.button_Go_Back.place(
            x=int(self.winfo_screenwidth()/20), y=int(self.winfo_screenheight()/1.2))
        self.button_Predict.place(
            x=int(self.winfo_screenwidth()/1.2), y=int(self.winfo_screenheight()/1.2))

    def panel_Right(self):
        # set ô text page predict
        self.bottom_Display_Perdict = tk.Text(self, width=int(
            self.winfo_screenwidth()/15), height=int(self.winfo_screenheight()/24))
        self.bottom_Display_Perdict.place(
            x=int(self.winfo_screenwidth()/4), y=int(self.winfo_screenheight()/5))

    # sự kiện cho list chọn database
    def select_Database(self, selection):
        print(selection)
        sql = "select * from "+str(selection)
        self.chosen_dataset = self.CONTROL_getInfo.query_table(sql)
        self.set_table(self.chosen_dataset.copy())
        # set list user
        # self.user_list = self.CONTROL_getInfo.get_user_info(
        #     self.chosen_dataset.copy())
        # self.option_Users = self.user_list.user_id.values
        # self.option_Menu_Users['menu'].delete(0, 'end')
        # for choice in self.option_Users:
        #     self.option_Menu_Users['menu'].add_command(
        #         label=choice, command=tk._setit(self.list_Users, choice))
        # self.list_Users.trace('w', self.select_User)
        # # set list film
        # self.movie_list = self.CONTROL_getInfo.get_movie_info(
        #     self.chosen_dataset.copy())
        # self.option_Film = self.movie_list.movie_id.values
        # self.option_Menu_Film['menu'].delete(0,'end')
        # for choice in self.option_Film:
        #     self.option_Menu_Film['menu'].add_command(label=choice, command=tk._setit(self.list_Films, choice))
        # self.list_Films.trace('w',self.select_Film)
        return 0

    def set_table(self, data):
        """
        Hiển thị Dataframe lên giao diện
        - Input: Dataframe: data
        - Output: None
        """
        self.table = Table(self.bottom, dataframe=data, showstatusbar=True)
        self.table.show()

    # sự kiện cho list chọn user
    def select_Method(self, *agrs):
        selected = self.list_Methods.get()
        print(selected)
        if selected == 'user-user':
            self.method = 1
        else:
            self.method = 0

    def select_User(self, *args):
        print(self.list_Users.get())
        self.chosen_user = self.CONTROL_getInfo.get_user_info_by_id(
            self.list_Users.get())
        return 0

    # sự kiện cho list chọn film
    def select_Film(self, *args):
        print(self.list_Films.get())
        # self.chosen_movie= self.CONTROL_getInfo.get_movie_info_by_id(self.list_Films.get())
        return 0

    # sự kiện cho button dự đoán.
    def perdict_System(self):
        rs = CF(self.chosen_dataset, k=20, uuCF = self.method, bert=1)
        rs.fit()
        full_rating = rs.full_Y()
        df_result = pd.DataFrame(full_rating)
        # print(df_result)
        # print(result)
        self.set_table(df_result)
        # self.bottom_Display_Perdict.delete(1.0,'end-1c')
        # self.bottom_Display_Perdict.insert("end-1c", "Predict result: "+str(df_result))
        return 0
