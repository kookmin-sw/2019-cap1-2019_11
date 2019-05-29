from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox as msg
from os import path

from yolo.yoloTracingRe import YOLO, detect_video, letterbox_image
from PIL import Image 

import face_recognition
import os
import datetime
import time
import sys
import subprocess as sp
import yoloface_img 
import cv2

from yolologo import YOLO2, blur_video, blur_webcam

from moviepy.tools import subprocess_call
from moviepy.config import get_setting

import pdb
import argparse

import client_sending
import server_receive

class f_setting:
    model = 'model-weights/face.h5'
    classes = 'cfg/face_classes.txt'
    anchors = 'cfg/yolo_anchors(face).txt'
    model_cfg='/cfg/face.cfg'
    score=0.5
    iou=0.45
    img_size=(416,416)
    image=False
    video=False
    output='outputs/'
    
    def __init__(self):
        pass;


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


def detect_img(yolo2):
    cap = cv2.VideoCapture(entry1.get())
    output_file='final.jpg'

    cv2.imwrite(entry1.get()+output_file, frame.astype(np.uint8))
##########################################


def ffmpeg_movie_from_frames(filename, folder, fps, digits=6):
    """
    Writes a movie out of the frames (picture files) in a folder.
    Almost deprecated.
    """
    s = "%" + "%02d" % digits + "d.png"
    cmd = [get_setting("FFMPEG_BINARY"), "-y", "-f","image2",
             "-r", "%d"%fps,
             "-i", os.path.join(folder,folder) + '/' + s,
             "-b", "%dk"%bitrate,
             "-r", "%d"%self.fps,
             filename]

    subprocess_call(cmd)



def ffmpeg_extract_subclip(filename, t1, t2, targetname=None):
    """ makes a new video file playing video file ``filename`` between
        the times ``t1`` and ``t2``. """
    name,ext = os.path.splitext(filename)
    if not targetname:
        T1, T2 = [int(1000*t) for t in [t1, t2]]
        targetname = name+ "%sSUB%d_%d.%s"(name, T1, T2, ext)

    cmd = [get_setting("FFMPEG_BINARY"),"-y",
      "-i", filename,
      "-ss", "%0.2f"%t1,
      "-t", "%0.2f"%(t2-t1),
      "-vcodec", "copy", "-acodec", "copy", targetname]

    subprocess_call(cmd)



def ffmpeg_merge_video_audio(video,audio,output, vcodec='copy',acodec='copy', ffmpeg_output=False,verbose = True):
    """ merges video file ``video`` and audio file ``audio`` into one
        movie file ``output``. """
    cmd = [get_setting("FFMPEG_BINARY"), "-y", "-i", audio,"-i", video,
             "-vcodec", vcodec, "-acodec", acodec, output]

    subprocess_call(cmd)



def ffmpeg_extract_audio(inputfile,output,bitrate=3000,fps=44100):
    """ extract the sound from a video file and save it in ``output`` """
    cmd = [get_setting("FFMPEG_BINARY"), "-y", "-i", inputfile, "-ab", "%dk"%bitrate,
         "-ar", "%d"%fps, output]
    subprocess_call(cmd)



def ffmpeg_resize(video,output,size):
    """ resizes ``video`` to new size ``size`` and write the result
        in file ``output``. """
    cmd= [get_setting("FFMPEG_BINARY"), "-i", video, "-vf", "scale=%d:%d"%(res[0], res[1]),
             output]

    subprocess_call(cmd)


####################################################################################

def convert():
    now = datetime.datetime.now()
    if typeradio.get()==1:
        if optionradio.get()==1:
            yoloface_img._main(entry1.get())
        else:
            FLAGS.input=entry1.get()
            detect_img(YOLO2(**vars(FLAGS)))
    elif typeradio.get()==2:
        if optionradio.get()==1:
            os.system(upload.php)
        else:
            os.system(upload2.php)           

            
    elif typeradio.get()==3:
        if optionradio.get()==1:
            fset=f_setting()
            fset.model='model-weights/face.h5'
            fset.classes = 'cfg/face_classes.txt'
            fset.anchors = 'cfg/yolo_anchors(face).txt'
            fset.video='stream'
            detect_video(YOLO(fset), fset.video, fset.output)

            # 음성 추출 extract the sound from a video file and save it in output

            inputfile=fset.video
            output='outputs/outAudio.mp3'
            ffmpeg_extract_audio(inputfile, output, bitrate=3000, fps=44100)

            audio='outputs/outAudio.mp3'
            video='outputs/output_video.avi'
            outputfinal='outputs/finalvideo.mp4'
            # merges video file video and audio file audio into one movie file output.

            ffmpeg_merge_video_audio(video, audio, outputfinal, vcodec='copy', acodec='copy', ffmpeg_output=False, verbose=True)
        else:
            blur_webcam(YOLO2(**vars(FLAGS)))
                    
####################################################################################
def getFileFromServer(filename):
    data_transferred = 0 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        sock.sendall(filename.encode()) 

        data = sock.recv(1024)
        if not data:
            print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' %filename)
            return 

        with open(filename, 'wb') as f:
            try:
                while  data:
                    f.write(data)
                    data_transferred += len(data)
                    data = sock.recv(1024)
            except Exception as e:
                print(e) 

    print('파일[%s] 전송종료. 전송량 [%d]' %(filename, data_transferred)) 

####################################################################################
parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
'''
Command line options
'''
parser.add_argument(
    '--model', type=str,
    help='path to model weight file, default ' + YOLO2.get_defaults("model_path")
)

parser.add_argument(
    '--anchors', type=str,
    help='path to anchor definitions, default ' + YOLO2.get_defaults("anchors_path")
)

parser.add_argument(
    '--classes', type=str,
    help='path to class definitions, default ' + YOLO2.get_defaults("classes_path")
)

parser.add_argument(
    '--gpu_num', type=int,
    help='Number of GPU to use, default ' + str(YOLO2.get_defaults("gpu_num"))
)

parser.add_argument(
    '--image', default=False, action="store_true",
    help='Image detection mode, will ignore all positional arguments'
)
'''
Command line positional arguments -- for video detection mode
'''
parser.add_argument(
    '--webcam', default=False, action="store_true",
    help='Webcam mode'
)
parser.add_argument(
    "--input", nargs='?', type=str,required=False,default='./path2your_video',
    help = "Video input path"
)

parser.add_argument(
    "--output", nargs='?', type=str, default="",
    help = "[Optional] Video output path"
)

FLAGS = parser.parse_args()
##########################################

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
