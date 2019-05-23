from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox as msg
from os import path


def fileupload():
    filename = askopenfilename(parent=window,title = "Select input File",
                               filetypes = (("jpeg files","*.jpg"),("video files","*.mp4 *.avi"),("all files","*.*")),
                               initialdir=path.dirname(__file__))
    entry1.config(state="normal")
    entry1.delete(0, END)
    entry1.insert(0, filename)
    entry1.config(state="readonly")

def quit():
    window.quit()
    window.destroy()
    exit()

def msgbox():
    msg.showinfo('Team Bblur Info', 'Team bblur')

window=Tk()        
window.title("Auto Blur with Object Dection")
window.geometry("190x300")
window.resizable(True, True)
window['bg']='lavender'

#############menu#######
menubar=Menu(window)
window.config(menu=menubar)

filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="File Upload", command=fileupload)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)

helpmenu=Menu(menubar,tearoff=0)
helpmenu.add_command(label="About", command=msgbox)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Help", menu=helpmenu)
############################

label1=Label(window, text="input file", background="lavender")

button1 = Button(window, text=" file upload ", relief='groove', foreground="LightPink4", command=fileupload)
button1["bg"]="peach puff"

entry1 = Entry(window,width=19)
entry1.insert(0,"video address")

radioframe1=LabelFrame(window, text='type',background="lavender")
radioframe2=LabelFrame(window, text='option',background="lavender")

typeradio=IntVar()
tradio1=Radiobutton(radioframe1, padx=18, text="picture", background="lavender", value=1, variable=typeradio)
tradio2=Radiobutton(radioframe1, padx=18, text="video", background="lavender", value=2, variable=typeradio)
tradio3=Radiobutton(radioframe1, padx=18, text="webcam", background="lavender", value=3, variable=typeradio)
optionradio=IntVar()
oradio1=Radiobutton(radioframe2, text="face detection", background="lavender", value=1, variable=optionradio)
oradio2=Radiobutton(radioframe2, text="logo detection", background="lavender", value=2, variable=optionradio)

button2 = Button(window, text=" Convert ", relief='groove', foreground="LightPink4")
button2["bg"]="peach puff"

label1.place(x=20,y=13)
button1.place(x=75, y=10)
entry1.place(x=20, y=40)
radioframe1.place(x=20, y=63)
radioframe2.place(x=20, y=161)
button2.place(x=20, y=240)

tradio1.grid(column=0, row=0, sticky=W)
tradio2.grid(column=0, row=1, sticky=W)
tradio3.grid(column=0, row=2, sticky=W)
oradio1.grid(column=0, row=0)
oradio2.grid(column=0, row=1)



window.mainloop()
