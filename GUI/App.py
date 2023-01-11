try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
import Predict_Movie as PM
import Data_Normalization as DN
import Index as IN
'''
chạy class này đầu tiên!!
nó như controller điều khiển và chuyển đổi các page của app.
'''
class SampleApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (IN.Index, DN.Data_Normalization, PM.Predicit_Movie):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Index")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = SampleApp()
    app.title("Recommendation System Application")
    width_value = app.winfo_screenwidth()
    height_value = app.winfo_screenheight()
    app.geometry("%dx%d+0+0" % (width_value,height_value))
    app.mainloop()