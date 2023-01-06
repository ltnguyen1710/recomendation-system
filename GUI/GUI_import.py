from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
from tkinter import filedialog as fd

# ------------------------Import Package CONTROL------------------------
import sys
sys.path.insert(0, 'CONTROL')
from CONTROL_import import CONTROL_import

class GUI_import:
    def __init__(self,root):
        self.single_import = None
        self.CONTROL_import = CONTROL_import()
        self.root=root
        
    def run_report(self, *args):
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
        path=''.join(filenames) #Convert Filenames to Str
        
        self.CONTROL_import.import_file(path,filenames)
        self.root.event_generate("<<PhishDoneEvent>>") # This is using tkinter in a thread, but some tkinter methods are ok to use in threads

    def close_import(self):
        self.single_import
        self.single_import.destroy()
        self.single_import = None

     
    def open_import(self):
        self.single_import
        if self.single_import is None:
            self.single_import = Toplevel(self.root)
            self.window_height = 250
            self.window_width = 250
            self.single_import.title("Import files")

            #----------- Mở cửa sổ chính giữa màn hình-----------

            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()
            # Coordinates of the upper left corner of the window to make the window appear in the center
            x_cordinate = int((self.screen_width/2) - (self.window_width/2))
            y_cordinate = int((self.screen_height/2) - (self.window_height/2))
            # Open root windown center
            self.single_import.geometry("{}x{}+{}+{}".format(self.window_width,
                        self.window_height, x_cordinate, y_cordinate))


            # open file button
            open_button = ttk.Button(
                self.single_import,
                text='Choose File',
                command=self.do_reports
            )
            
            open_button.grid(column=0, row=1, sticky='w', padx=85, pady=10)    
            self.root.bind("<<PhishDoneEvent>>", self.report_done)
            # assign to closing button [X]
            self.single_import.protocol("WM_DELETE_WINDOW", self.close_import)
        else:
            print("Add new already exists")
    
    # Show process bar when import bigdata in SQL
    def do_reports(self, *args):
        self.pbar = ttk.Progressbar(self.single_import, orient = HORIZONTAL, mode = 'indeterminate')
        self.pbar.grid(row = 4, column = 3, sticky = (W, E))
        start, end = 4,5
        t1 = threading.Thread(target = self.run_report, args = [self.root, start, end])
        t1.start()
        self.pbar.start()

    # Show alert when Import is done
    def report_done(self, event=None):
        self.pbar.stop()
        messagebox.showinfo("Alert", self.CONTROL_import.show_alert())
        self.close_import()