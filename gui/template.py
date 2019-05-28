from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox as msg
from os import path

from client_sending import sendFile
from server_receive import receiveFile

ec2='ec2-52-79-176-116.ap-northeast-2.compute.amazonaws.com'


def fileupload():
    filename = askopenfilename(parent=window,title = "Select input File",
                               filetypes = (("jpeg files","*.jpg"),("video files","*.mp4 *.avi"),("all files","*.*")),
                               initialdir=path.dirname(__file__))
    entry1.config(state="normal")
    entry1.delete(0, END)
    entry1.insert(0, filename)
    entry1.config(state="readonly")

def faceupload():
    filename = askopenfilename(parent=window,title = "Select input File",
                               filetypes = (("jpeg files","*.jpg"),("all files","*.*")),
                               initialdir=path.dirname(__file__))
    print(filename)
    sendFile(ec2,8000, filename)

def quit():
    window.quit()
    window.destroy()
    exit()

def msgbox():
    msg.showinfo('Team Bblur Info', 'Team bblur\n김용욱 : Object detection모델 연구와 사용 및 웹 개발\n김대희 : Object detection 모델 연구와 사용 및 웹 개발\n권보경 : 어플리케이션 및 서버 개발\n이나영 : 어플리케이션 및 서버 개발\n채승훈 : ux/ui')

def convert():
    if typeradio.get()==2:
        if optionradio.get()==1:
            sendFile(ec2,5000, entry1.get())
            receive('outputs/finalvideo.mp4')
        else:
            a=asksaveasfilename(title='save final file', initialfile='final', filetypes=(('image files','*.jpg'),('video files','*.mp4'),('all files', '*.*')))
            if a:
                f=open('outputs/finalvideo.mp4','w')
                g=open(a,'w')
                for i_line in f.readlines():
                    g.write("%s"%i_line)
                f.close

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
filemenu.add_command(label="Save File", command=faceupload)
filemenu.add_separator()
filemenu.add_command(label="Face upload", command=faceupload)
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

button2 = Button(window, text=" Convert ", relief='groove', foreground="LightPink4", command=convert)
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
