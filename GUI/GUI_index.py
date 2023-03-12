import tkinter as tk
import glob
from CanvasButton import CanvasButton


'''
class này hiển thị các phần button của trang index của hệ thống

'''


class GUI_index(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # hiển thị nền cho page.
        canvas = tk.Canvas(self, width = self.winfo_screenwidth(), height = self.winfo_screenheight())
        canvas.pack()
        path = glob.glob('img/BG.png')
        self.bg = tk.PhotoImage(file=path)

        # set label hiển thị trên page index.
        # label = tk.Label(
        #     self, text="Recommendation System Application", font=controller.title_font)
        # label.place(x=int(self.winfo_screenwidth())/3, y=10)

        background = canvas.create_image(0, 0, image=self.bg,anchor='nw')
        label = canvas.create_text(int(self.winfo_screenwidth())/2, 20, text="Recommendation System Application",font=controller.title_font)

        button_Import = CanvasButton(canvas,int(self.winfo_screenwidth())/1.3, int(self.winfo_screenheight())/8, 'img/Btn_1.png',lambda: controller.show_frame("Data_Normalization"))
        label_Import = canvas.create_text(int(self.winfo_screenwidth())-(int(self.winfo_screenwidth())/5), int(self.winfo_screenheight())/5, text="Import",font=controller.title_font)
        
        button_Recommendation = CanvasButton(canvas, int(self.winfo_screenwidth())/1.3, int(self.winfo_screenheight())/3, 'img/Btn_1.png',lambda: controller.show_frame("Predicit_Movie"))
        # label_Recommendation = canvas.create_text(int(self.winfo_screenwidth())/4, 40, text="Recommendation",font=controller.title_font)
