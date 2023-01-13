import tkinter as tk 
import glob


'''
class này hiển thị các phần button của trang index của hệ thống

'''

class GUI_index(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
       
        # hiển thị nền cho page.
        path=glob.glob('img/BG.png')
        self.bg = tk.PhotoImage(file = path)

        self.my_Label = tk.Label(self, image= self.bg)
        self.my_Label.place(relwidth= 1, relheight= 1)
       
        # set label hiển thị trên page index.
        label = tk.Label(self, text="Recommendation System Application", font=controller.title_font)
        label.place(x = int(self.winfo_screenwidth())/3,y=10)
       
        # button chuyển qua page định chuẩn dữ liệu.
        self.button_Data = tk.Button(self, text="Data Normalization",font="23",fg='#A50C0C', bg="#C0C0C0",
                            command=lambda: controller.show_frame("Data_Normalization"))
        
        # button chuyển qua page predict movie.
        self.button_Predict = tk.Button(self, text="    Predict Movie   ",font="23",fg='#A50C0C', bg="#C0C0C0",
                            command=lambda: controller.show_frame("Predicit_Movie"))
        # set vị trị cho 2 button
        self.button_Data.place(x = int(self.winfo_screenwidth())/1.3, y = int(self.winfo_screenheight())/8)
        self.button_Predict.place(x = int(self.winfo_screenwidth())/1.3, y = int(self.winfo_screenheight())/5)
        
