from tkinter import *
import cv2
import numpy as np

import argparse
import sys
import os
import datetime
import time#######################################################
#ffmpeg


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


######################################################



window=Tk()        
window.title("Bblur")
window.geometry("640x400+100+100")
window.resizable(True, True)

button1 = Button(window, text="file upload")
button1.pack()
entry1 = Entry(window)
entry1.insert(0,"video address")
entry1.pack()##援ы쁽以?

label = Label(window, text="option")
label.pack()

typeradio=IntVar()
tradio1=Radiobutton(window, text="video", value=1, variable=typeradio)
tradio1.pack()
tradio2=Radiobutton(window, text="webcam", value=2, variable=typeradio)
tradio2.pack()

optionradio=IntVar()
oradio1=Radiobutton(window, text="face detection", value=1, variable=optionradio)
oradio1.pack()
oradio2=Radiobutton(window, text="logo detection", value=2, variable=optionradio)
oradio2.pack()


button2 = Button(window, text="Convert")
button2.pack()



window.mainloop()
