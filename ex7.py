from Tkinter import *
import ttk

window=Tk()
window.title("YUN DAE HEE")
window.geometry("640x400+100+100")
window.resizable(False, False)

count=0

def countUP():
    global count
    count +=1
    label.config(text=str(count))

label = Label(window, text="0")
label.pack()

button = Button(window, overrelief="solid", width=15, command=countUP, repeatdelay=1000, repeatinterval=100)
button.pack()

window.mainloop()
