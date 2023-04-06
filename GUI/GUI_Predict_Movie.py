import glob
import App as APP
from time import strftime
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from tkinter import filedialog, Label, Button, Entry, StringVar
from pandastable import Table
import pandas as pd
from tkinter import font as tkfont  
import tkinter as tk
# Import the required libraries
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

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
        canvas = tk.Canvas(self, width = self.winfo_screenwidth(), height = self.winfo_screenheight())
        canvas.pack()
        # set bg cho page predict
        path = glob.glob('img/BG_predict.png')
        self.bg = tk.PhotoImage(file=path)
        font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")

        background = canvas.create_image(0, 0, image=self.bg,anchor='nw')
        label = canvas.create_text(int(self.winfo_screenwidth())/2, 30, text="Recommendation",font=controller.title_font)
        label_Rating = canvas.create_text(self.winfo_screenwidth()*0.16, self.winfo_screenheight()*0.87, text="Ratings user for item ",font=font,fill="white")
        label_Info = canvas.create_text(self.winfo_screenwidth()*0.65, self.winfo_screenheight()*0.87, text="Information of movie",font=font,fill="white")

        
        # Khởi tạo 2 biến OptionMenu
        self.chosen_dataset = pd.DataFrame()
        self.method = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.initUI()

    def initUI(self):

        self.panel_Left()
        # self.panel_Right()


    def panel_Left(self):
        data = pd.DataFrame()
        
        # Frame Table Rating
        self.bottom_Rating = tk.Frame(self,background='#DCDCDC')
        self.bottom_Rating.place(x=int(self.winfo_screenwidth()/20), y=self.winfo_screenheight()*0.14, width=self.winfo_screenwidth() *
                          0.22, height=self.winfo_screenheight()*0.7)
        
        self.table_rating = Table(self.bottom_Rating, dataframe=data, showstatusbar=True)
        self.table_rating.show()
        self.table_rating.redraw()
        
        # Frame Table Info
        self.bottom_Info = tk.Frame(self,background='#DCDCDC')
        self.bottom_Info.place(x=self.winfo_screenwidth()*0.3, y=self.winfo_screenheight()*0.14, width=self.winfo_screenwidth() *
                          0.646, height=self.winfo_screenheight()*0.7)

        self.table_info = Table(self.bottom_Info, dataframe=data, showstatusbar=True)
        self.table_info.show()
        self.table_info.redraw()
         
        # set list chọn dataset
        self.option_Database = self.CONTROL_getInfo.get_list_Table()
        self.list_Database = tk.StringVar()
        self.list_Database.set("Select database")
        self.list_Database.trace('w', self.select_Database)


        self.option_Menu_Database = tk.OptionMenu(
            self, self.list_Database, *self.option_Database)

        # button go back đã được setup
        self.button_Go_Back = tk.Button(self, text="Go back to menu",
                                        command=lambda: APP.SampleApp.show_frame(self.controller, "GUI_index"))

        # set list chọn method
        self.list_Methods = tk.StringVar()
        self.list_Methods.set("Select method")
        self.option_Methods = ['user_user_BERT','item_item_BERT']
        self.option_Menu_Methods = tk.OptionMenu(
            self, self.list_Methods, *self.option_Methods , command=self.select_Method)

        # set button dự đoán.
        self.button_Predict = tk.Button(
            self, text="Start Predict", command=self.perdict_System)
        
        path = glob.glob('img/Btn_refresh.png')
        # Creating a photoimage object to use image
        icon = tk.PhotoImage(file=path)
        icon = icon.subsample(15, 15)
        

        # set button Refresh DTB.
        self.button_Refresh_DTB = tk.Button(
            self, text="Refresh list Database", image=icon, command=self.refresh_listOption_DTB)
        self.button_Refresh_DTB.image=icon
        # set vị trí của các label, list, button.
        self.option_Menu_Database.place(
            x=int(self.winfo_screenwidth()/4), y=self.winfo_screenheight()*0.09,height=30, width=180)
        self.button_Refresh_DTB.place(
            x=int(self.winfo_screenwidth()/2.5), y=self.winfo_screenheight()*0.09, width=30,height=30)
        self.option_Menu_Methods.place(x=int(self.winfo_screenwidth()/2), y=self.winfo_screenheight()*0.09,height=30)
        self.button_Go_Back.place(
            x=int(self.winfo_screenwidth()/20), y=self.winfo_screenheight()*0.09,height=30)
        self.button_Predict.place(
            x=int(self.winfo_screenwidth()/1.2), y=self.winfo_screenheight()*0.09,height=30)

    def panel_Right(self):
        # set ô text page predict
        self.bottom_Display_Perdict = tk.Text(self, width=int(
            self.winfo_screenwidth()/15), height=int(self.winfo_screenheight()/24))
        self.bottom_Display_Perdict.place(
            x=int(self.winfo_screenwidth()/4), y=int(self.winfo_screenheight()/5))

    # sự kiện cho list chọn database
    def select_Database(self, *args):
        selection = self.list_Database.get()
        print (selection)
        sql = "select * from "+str(selection)
        
        self.chosen_dataset = self.CONTROL_getInfo.query_table(sql)
        self.set_table(self.chosen_dataset.copy())
        return 0

    def refresh_listOption_DTB(self):
        self.option_Database = self.CONTROL_getInfo.get_list_Table()
        # Reset var and delete all old options        
        menu = self.option_Menu_Database["menu"]
        menu.delete(0, "end")

        for choice in self.option_Database:
            menu.add_command(label=choice, 
                             command=lambda value=choice: self.list_Database.set(value))

    def set_table(self, data, predict=0):
        """
        Hiển thị Dataframe lên giao diện
        - Input: Dataframe: data
        - Output: None
        """

        if predict == 0:
            data_rating = data.iloc[:, 0:3].copy()

            data_info = data.iloc[:, [1, 3,4,5]].drop_duplicates().copy()
            
            
            self.table_rating = Table(self.bottom_Rating, dataframe=data_rating, showstatusbar=True,editable=False)
            self.table_info = Table(self.bottom_Info, dataframe=data_info, showstatusbar=True,editable=False)
            self.table_rating.show()
            self.table_info.show()

        self.table_rating.redraw()
        self.table_info.redraw()

    # sự kiện cho list chọn user
    def select_Method(self, *agrs):
        selected = self.list_Methods.get()
        if selected == "user_user_BERT":
            self.method = 1
        else:
            self.method = 0
    def result_predict_table(self):
    	
        if(self.method == 1):
            title_windown = "RESULT PREDICT TABLE WITH USER BERT" 
            option_title = 'Select User'
            list_to_choose = self.chosen_dataset['user_id'].unique().tolist()
            text_option = "Select user to recommend:"
            list_movie = self.chosen_dataset['movie_id'].unique().tolist()
            self.list_movie_with_content = self.chosen_dataset[self.chosen_dataset['movie_id'].isin(list_movie)]
            self.list_movie_with_content = self.list_movie_with_content.drop_duplicates(subset='movie_id')
            self.list_movie_with_content = self.list_movie_with_content.drop(columns=['user_id','rating'])
            self.list_movie_with_content = self.list_movie_with_content.reset_index().drop(columns=['index'])
        else:    
            title_windown = "RESULT PREDICT TABLE WITH ITEM BERT" 
            option_title = 'Select Movie'
            text_option = "Select item to recommend:"
            list_to_choose = self.chosen_dataset['movie_id'].unique().tolist()
            
        result_window = tk.Toplevel()
        result_window.title(title_windown)
        result_window.state('zoomed')
        # Title
        title_result_table = Label(result_window,
            text ="RESULT PREDICT TABLE", font=self.title_font)
        # Frame select
        frame_select_options = tk.Frame(result_window, borderwidth=2, relief="groove")
        
        self.frame_result_table = tk.Frame(result_window,background='#DCDCDC')
        # ----------- Mở cửa sổ chính giữa màn hình-----------
        screen_width = result_window.winfo_screenwidth()
        screen_height = result_window.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
        window_width =result_window.winfo_screenwidth() *0.8
        window_height = result_window.winfo_screenheight()*0.5
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        # ----------- Mở cửa sổ chính giữa màn hình-----------
        frame_select_options.place(x=x_cordinate, y=self.winfo_screenheight()*0.15, width=self.winfo_screenwidth() *
                          0.45, height=self.winfo_screenheight()*0.17)
        title_result_table.place(x=self.winfo_screenwidth()*0.4, y=self.winfo_screenheight()*0.36)
        self.frame_result_table.place(x=x_cordinate, y=self.winfo_screenheight()*0.4, width=window_width, height=window_height)
        
        # -----------------------   
        
        # Label
        label_option_User = tk.Label(frame_select_options, text=text_option, font=("Arial", 15), bd=0)
        label_option_User.place(x=int(self.winfo_screenwidth()*0.02), y=self.winfo_screenheight()*0.06)
        # set list chọn user để recomend
        temp1 = list_to_choose
        self.option_User = temp1
        self.list_User = tk.StringVar()
        self.list_User.set(option_title)
        # self.list_User.trace('w', self.select_Database)
        self.option_Menu_Database = ttk.Combobox(
            frame_select_options, state="readonly",textvariable = self.list_User, values=self.option_User)
        self.option_Menu_Database.bind("<<ComboboxSelected>>", self.select_object)
        self.option_Menu_Database.place(
            x=int(self.winfo_screenwidth()*0.25), y=self.winfo_screenheight()*0.06,height=30, width=180)
        

        
        # Button recommend
        button_recommend = tk.Button(result_window, text='Recommend...', font=("Arial", 12),
                                     command=self.demo)
        button_recommend.configure(bg='#B2EBE0')
        button_recommend.place(x=self.winfo_screenwidth() *0.6, y=self.winfo_screenheight()*0.15, width=self.winfo_screenheight()*0.17,
                                      height=self.winfo_screenheight()*0.17)

        # -----------------------


        data = pd.DataFrame()
        # self.table_result = Table(self.frame_result_table, dataframe=df_result, showstatusbar=True)
        self.table_result = Table(self.frame_result_table, dataframe=data, showstatusbar=True,editable=False)
        self.table_result.show()
        self.table_result.redraw()
        self.table_result.rowselectedcolor = 'none'

        # # ----------- TÔ MÀU cho bảng-----------
        # # Tô cả bảng
        # for i in range(df_result.shape[0]):
        #     self.table_result.setRowColors(rows=i, clr='#F26BAA',  cols="all")
        # self.table_result.setRowColors(rows=range(df_result.shape[0]), clr='#F26BAA', cols='all')
        # index=0
        # for i in mask_color_table:
        #     if len(i) == 0:
        #         pass
        #     else:
        #         self.table_result.setRowColors(rows=index, clr='#B2EBE0',  cols=i)
        #     index = index +1
        # self.table_result.show()

    def select_object(self, event):
        selected = self.list_User.get()
        # print('select user: ',selected)
        self.selected_object = selected 

    def demo(self):
        df_recommend = self.rs.recommend(int(self.selected_object)-1)
        if self.method == 1:
            df_result = pd.merge(df_recommend,self.list_movie_with_content,on='movie_id').sort_values(by=['predict_rate'],ascending=False)
        else:
            df_result = df_recommend.sort_values(by=['predict_rate'], ascending=False)
        self.table_result = Table(self.frame_result_table, dataframe=df_result, showstatusbar=True, editable=False,)

        self.table_result.show()
        self.table_result.expandColumns(factor = 20)
        self.table_result.autoResizeColumns()
        self.table_result.redraw()

    # sự kiện cho button dự đoán.
    def perdict_System(self):
        

        if self.chosen_dataset.empty:
            messagebox.showinfo("Alert", 'Please Select Database')
        elif self.method is None:
            messagebox.showinfo("Alert", 'Please Select Method')
        else:
            data_to_cal =self.chosen_dataset.copy() 
            data_to_cal[['user_id','movie_id']] = data_to_cal[['user_id','movie_id']].apply(lambda x: x-1)
            self.rs = CF(data_to_cal, k=30, uuCF = self.method, bert=1)
            self.rs.fit()
            self.result_predict_table()
            return 0
