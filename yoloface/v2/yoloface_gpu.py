# -*- coding: utf-8 -*-
import argparse

# from yolo.yolo_md import YOLO, detect_video, letterbox_image
from yolo.yoloTracingRe import YOLO, detect_video, letterbox_image
# from yolo.yoloTracing import YOLO, detect_video, letterbox_image
# from yolo.yolo_md_half import YOLO, detect_video, letterbox_image

import face_recognition
import os
import datetime
import time
import sys
# import subprocess as sp

from moviepy.tools import subprocess_call
from moviepy.config import get_setting

#####################################################################




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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='model-weights/YOLO_Face.h5',
                        help='path to model weights file')
    parser.add_argument('--anchors', type=str, default='cfg/yolo_anchors.txt',
                        help='path to anchor definitions')
    parser.add_argument('--classes', type=str, default='cfg/face_classes.txt',
                        help='path to class definitions')
    parser.add_argument('--score', type=float, default=0.7,
                        help='the score threshold')
    parser.add_argument('--iou', type=float, default=0.45,
                        help='the iou threshold')
    parser.add_argument('--img-size', type=list, action='store',
                        default=(416, 416), help='input image size')
    parser.add_argument('--image', default=False, action="store_true",
                        help='image detection mode')
    parser.add_argument('--video', type=str, default='samples/subway.mp4',
                        help='path to the video')
    parser.add_argument('--output', type=str, default='outputs/',
                        help='image/video output path')
    args = parser.parse_args()
    return args


def _main():
    # Get the arguments
    args = get_args()
    now = datetime.datetime.now()

    if args.image:
        # Image detection mode
        print('[i] ==> Image detection mode\n')
        detect_img(YOLO(args))
    else:
        print('[i] ==> Video detection mode\n')
        # Call the detect_video method here
        detect_video(YOLO(args), args.video, args.output)

    print('Well done!!!')
    end = datetime.datetime.now()
    print(now)
    print(end)


    # 음성 추출 extract the sound from a video file and save it in output

    inputfile=args.video
    output='outputs/outAudio.mp3'
    ffmpeg_extract_audio(inputfile, output, bitrate=3000, fps=44100)

    audio='outputs/outAudio.mp3'
    video='outputs/output_video.avi'
    outputfinal='outputs/finalvideo.mp4'
    # merges video file video and audio file audio into one movie file output.

    ffmpeg_merge_video_audio(video, audio, outputfinal, vcodec='copy', acodec='copy', ffmpeg_output=False, verbose=True)

if __name__ == "__main__":
    _main()
