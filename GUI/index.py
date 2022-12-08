import tkinter as tk


class index(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background = "white")
        self.parent = parent

        self.initUI()

    
    def initUI(self):
        #set title application
        self.parent.title("Recommendation System Application")

        #setup listbox 1 
        self.listOption = ('Java', 'C#', 'C', 'C++', 'Python')
        self.var = tk.Variable(value=self.listOption)
        self.listbox = tk.Listbox(root, listvariable=self.var, height=6, selectmode=tk.EXTENDED, background="#cc99ff",font=("",13),)
        self.listbox.bind('<<ListboxSelect>>', self.items_selected_1)
        self.listbox.place(x=width_value/1.5,y=height_value/6, anchor=tk.SE)

        #setup Listbox 2
        self.listOption_2 = ['baka', 'taki', 'Ren', 'baga', 'te liet']
        self.var_2 = tk.Variable(value=self.listOption_2)
        self.listbox_2 = tk.Listbox(root, listvariable=self.var_2, height=6, selectmode=tk.EXTENDED, background="#ffcc99",font=("",13))
        self.listbox_2.bind('<<ListboxSelect>>', self.items_selected_2) 
        self.listbox_2.place(x=width_value/3,y=height_value/6,anchor=tk.SW)
         #setup checkbox
        self.mvar = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(root,text="Choose option",variable = self.mvar,background="#ff0000",
                                                onvalue = True, offvalue = False,font=("",13),command=self.chooseCheckbox)
        self.checkbox.place(x=width_value/2,y=height_value/2.7,anchor=tk.CENTER)
        #setup label
        self.label = tk.Label(root,text= self.mvar.get(),font=("",30),background="#34A2FE")
        self.label.place(x=width_value/2,y=height_value/2.5,height=height_value/2, width=width_value/2,anchor=tk.N)
        #
        
    
    def chooseCheckbox(self):
        if (self.mvar.get() == True) :
            self.label.config(text=self.mvar.get())
        else :
            self.label.config(text=self.mvar.get())

    
    def items_selected_1(self,event):
        # get selected indices
        self.selected_indices = self.listbox.curselection()
        # get selected items
        self.selected_langs = ",".join([self.listbox.get(i) for i in self.selected_indices])
        self.msg = f'You selected: {self.selected_langs}'
        # self.showinfo(title='Information', message=msg)
    
    
    def items_selected_2(self):
        # get selected indices
        self.selected_indices = self.listbox_2.curselection()
        # get selected items
        self.selected_langs = ",".join([self.listbox_2.get(i) for i in self.selected_indices])
        self.msg = f'You selected: {self.selected_langs}'
        # self.showinfo(title='Information', message=msg)
        
        
        


        

            
        
if __name__ == "__main__":
    root = tk.Tk()
    width_value = root.winfo_screenwidth()
    height_value = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (width_value,height_value))
    app = index(root)
    root.mainloop()