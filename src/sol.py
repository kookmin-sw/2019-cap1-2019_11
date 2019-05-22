from tkinter import *

import sys
import os

import datetime
import time
import face_recognition
import cv2
import camera
import numpy as np

from utils import *
import subprocess as sp

from moviepy.tools import subprocess_call
from moviepy.config import get_setting


#########################################



#######################################################
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




def videoupload(): #??솁??뵬 ??궎?逾? ?뤃?뗭겱?釉?
    filename = askopenfilename(parent=root) 
    f = open(filename) 
    f.read()


def process():
    if optionradio.get==1: #face detection
        if typeradio.get==1: #video
            net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            cap = cv2.VideoCapture("input.mp4")

            video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),cap.get(cv2.CAP_PROP_FPS),
                                           (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                            round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
            #videowriter(outputfile,fourcc,frame,size)
            #fourcc : codec information

            face_recog=FaceRecog_video()
            while True:
                has_frame, frame=cap.read()
                if not has_frame:
                    print('[i] ==> Done processing!!!')
                    print('[i] ==> Output file is stored at', os.path.join(args.output_dir, output_file))
                    cv2.waitKey(1000)
                    break
                frame=face_recog.get_frame(frame)
            # Save the output video to file
                video_writer.write(frame.astype(np.uint8))

                key = cv2.waitKey(1)
                if key == 27 or key == ord('q'):
                    print('[i] ==> Interrupted by user!')
                    break

            cap.release()
            cv2.destroyAllWindows()
            ffmpeg_extract_audio('input.mp4', 'outAudio.mp3', bitrate=3000, fps=44100)
            ffmpeg_merge_video_audio('output.mp4', 'outAudio.mp3', 'output_final.mp4', vcodec='copy', acodec='copy', ffmpeg_output=False, verbose=True)
        elif typeradio.get==2: #webcam
            net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

            face_recog=FaceRecog_Cam()
            while True:
                frame=face_recog.get_frame()
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
    

window=Tk()        
window.title("Auto Blur with Object Dection")
window.geometry("350x400")
window.resizable(False, False)
window['bg']='lavender'


button1 = Button(window, text="file upload", relief='groove', foreground="LightPink4", command=videoupload)
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

button2 = Button(window, text="Convert", relief='groove', foreground="LightPink4", command=process)
button2.pack()
button2["bg"]="peach puff"


window.mainloop()
