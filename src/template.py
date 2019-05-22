from tkinter import *
from tkinter.filedialog import *


def fileupload():
    filename = askopenfilename(parent=window,title = "Select input File", filetypes = (("jpeg files","*.jpg"), ("video files","*.mp4 *.avi"),("all files","*.*")))
    
    

window=Tk()        
window.title("Auto Blur with Object Dection")
window.geometry("350x400")
window.resizable(False, False)
window['bg']='lavender'


button1 = Button(window, text="file upload", relief='groove', foreground="LightPink4", command=fileupload)
button1.pack() # Displaying the button
button1["bg"]="peach puff"

entry1 = Entry(window)
entry1.insert(0,"video address")
entry1.pack()

typeradio=IntVar()
tradio1=Radiobutton(window, text="video", background="lavender", value=1, variable=typeradio)
tradio1.pack()
tradio2=Radiobutton(window, text="webcam", background="lavender", value=2, variable=typeradio)
tradio2.pack()

optionradio=IntVar()
oradio1=Radiobutton(window, text="face detection", background="lavender", value=1, variable=optionradio)
oradio1.pack()
oradio2=Radiobutton(window, text="logo detection", background="lavender", value=2, variable=optionradio)
oradio2.pack()

button2 = Button(window, text="Convert", relief='groove', foreground="LightPink4")
button2.pack()
button2["bg"]="peach puff"


window.mainloop()
