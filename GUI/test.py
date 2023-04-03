# Import the required libraries
from tkinter import *
from PIL import Image, ImageTk

# Create an instance of tkinter frame or window
win=Tk()

# Set the size of the tkinter window
win.geometry("700x350")

frame_img = Frame(win)
frame_img.pack()
frame_img.place(x=10, y=30)
# Load the image
image=Image.open('img/Btn_row.png')

# Resize the image in the given (width, height)
img=image.resize((100, 100))

# Conver the image in TkImage
my_img=ImageTk.PhotoImage(img)

# Display the image with label
label=Label(frame_img, image=my_img)
label.pack()

win.mainloop()