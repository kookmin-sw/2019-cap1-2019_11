# *******************************************************************
#
# Author : Thanh Nguyen, 2018
# Email  : sthanhng@gmail.com
# Github : https://github.com/sthanhng
#
# BAP, AI Team
# Face detection using the YOLOv3 algorithm
#
# Description : yoloface.py
# The main code of the Face detection using the YOLOv3 algorithm
#
# *******************************************************************

# Usage example:  python yoloface.py --image samples/outside_000001.jpg \
#                                    --output-dir outputs/
#                 python yoloface.py --video samples/subway.mp4 \
#                                    --output-dir outputs/
#                 python yoloface.py --src 1 --output-dir outputs/


import argparse
import sys
import os
# -*- coding: utf-8 -*-
import camera
import datetime
import time
import sys
import os
import colorsys
import numpy as np
import cv2
import face_recognition
import pickle

from utils import *

#####################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--model-cfg', type=str, default='./cfg/face.cfg',
                    help='path to config file')
parser.add_argument('--model-weights', type=str,
                    default='./model-weights/face16000.weights',
                    help='path to weights of model')
parser.add_argument('--image', type=str, default='',
                    help='path to image file')
parser.add_argument('--video', type=str, default='',
                    help='path to video file')
parser.add_argument('--src', type=int, default=0,
                    help='source of the camera')
parser.add_argument('--output-dir', type=str, default='outputs/',
                    help='path to the output directory')
args = parser.parse_args()

#####################################################################
# print the arguments
print('----- info -----')
print('[i] The config file: ', args.model_cfg)
print('[i] The weights of model file: ', args.model_weights)
print('[i] Path to image file: ', args.image)
print('[i] Path to video file: ', args.video)
print('###########################################################\n')

# check outputs directory
if not os.path.exists(args.output_dir):
    print('==> Creating the {} directory...'.format(args.output_dir))
    os.makedirs(args.output_dir)
else:
    print('==> Skipping create the {} directory...'.format(args.output_dir))

# Give the configuration and weight files for the model and load the network
# using them.
net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def _main(fileinput):
    # wind_name = 'face detection using YOLOv3'
    # cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)

    output_file = ''
    known_face_encodings=[]
    known_face_names=[]
    args.image=fileinput
    if args.image:
        if not os.path.isfile(args.image):
            print("[!] ==> Input image file {} doesn't exist".format(args.image))
            sys.exit(1)
        cap = cv2.VideoCapture(args.image)
        # output_file = args.image[:-4].rsplit('/')[-1] + '_yoloface.jpg'
        output_file='final.jpg'
    elif args.video:
        if not os.path.isfile(args.video):
            print("[!] ==> Input video file {} doesn't exist".format(args.video))
            sys.exit(1)
        cap = cv2.VideoCapture(args.video)
        output_file = args.video[:-4].rsplit('/')[-1] + '_yoloface.avi'
    else:
        # Get data from the camera
        cap = cv2.VideoCapture(args.src)

    dirname='face_except'
    files=os.listdir(dirname)
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext == '.jpg':
            known_face_names.append(name)
            pathname = os.path.join(dirname, filename)
            img = face_recognition.load_image_file(pathname)

            try :
                face_encoding = face_recognition.face_encodings(img)[0]
                known_face_encodings.append(face_encoding)
                print('{}는 인식이 되었습니다. '.format(name))

            except IndexError :  # 에러 종류
                print('{}는 인식이 되지 않습니다.'.format(name))  #에러가 발생 했을 경우 처리할 코드


    while True:

        has_frame, frame = cap.read()

        # Stop the program if reached end of video
        if not has_frame:
            print('[i] ==> Done processing!!!')
            print('[i] ==> Output file is stored at', os.path.join(args.output_dir, output_file))
            cv2.waitKey(1000)
            break

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                     [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(get_outputs_names(net))

        # Remove the bounding boxes with low confidence
        final_boxes = post_process2(frame, outs, CONF_THRESHOLD, NMS_THRESHOLD)

        # left, top, width, height

        # [[139, 106, 205, 248]]
        face_encodings = face_recognition.face_encodings(frame, final_boxes)
        face_names=[]

        for face_encoding in face_encodings:
            distances=face_recognition.face_distance(known_face_encodings, face_encoding)

            if not len(distances)==0:

                min_value=min(distances)
                print(min_value)
                name="Unknown"
                if min_value < 0.37:
                    index=np.argmin(distances)
                    name = known_face_names[index]
                    print('name = ', name)
                    print('min_v : ',min_value)

                face_names.append(name)
            else:
                name="Unknown"
                face_names.append(name)
                print('name = ', name)


        for (top,right,bottom,left), name in zip(final_boxes, face_names):

            

            if name == 'Unknown':
                face_image = frame[top:bottom, left:right]
                face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
                frame[top:bottom, left:right] = face_image


        # Save the output video to file
        if args.image:
            cv2.imwrite(os.path.join(args.output_dir, output_file), frame.astype(np.uint8))
        else:
            video_writer.write(frame.astype(np.uint8))

        # cv2.imshow(wind_name, frame)

        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            print('[i] ==> Interrupted by user!')
            break

    cap.release()
    cv2.destroyAllWindows()

    print('==> All done!')
    print('***********************************************************')


if __name__ == '__main__':
    _main()
