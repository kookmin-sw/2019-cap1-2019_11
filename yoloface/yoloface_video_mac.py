# -*- coding: utf-8 -*-

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

# python yoloface.py --video samples/lunch1.mp4 --encodings encodings.pickle
# python yoloface.py --image samples/outside_000001.jpg --output-dir outputs/
# python yoloface.py --image samples/example_04.png  --encodings encodings.pickle
from datetime import datetime
import argparse
import sys
import os
import cv2
import face_recognition
import time
import pickle
from utils import *
#####################################################################
print('hi')

parser = argparse.ArgumentParser()
parser.add_argument('--model-cfg', type=str, default='./cfg/yolov3-face.cfg',
                    help='path to config file')
parser.add_argument('--model-weights', type=str,
                    default='./model-weights/yolov3-wider_16000.weights',
                    help='path to weights of model')
parser.add_argument('--image', type=str, default='',
                    help='path to image file')
parser.add_argument('--video', type=str, default='',
                    help='path to video file')
parser.add_argument('--src', type=int, default=0,
                    help='source of the camera')
parser.add_argument('--output-dir', type=str, default='outputs/',
                    help='path to the output directory')
parser.add_argument('--encodings', required=True, help="path to serialized db of facial encodings")
args = parser.parse_args()

#####################################################################
# print the arguments
now = datetime.datetime.now()

print('----- info -----')
print('[i] The config file: ', args.model_cfg)
print('[i] The weights of model file: ', args.model_weights)
print('[i] Path to image file: ', args.image)
print('[i] Path to video file: ', args.video)
print('[i] test ', args.encodings)
print('###########################################################\n')

# check outputs directory
if not os.path.exists(args.output_dir):
    print('==> Creating the {} directory...'.format(args.output_dir))
    os.makedirs(args.output_dir)
else:
    print('==> Skipping create the {} directory...'.format(args.output_dir))

# Give the configuration and weight files for the model and load the network
# using them.
data = pickle.loads(open(args.encodings, "rb").read(),encoding='latin1')
# data = pickle.loads(open(args["encodings"], "rb").read())
net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

print("[INFO] processing video...")
writer = None

def _main():
    wind_name = 'face detection using YOLOv3'
#    cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)

    output_file = ''

    if args.video:
        if not os.path.isfile(args.video):
            print("[!] ==> Input video file {} doesn't exist".format(args.video))
            sys.exit(1)
        cap = cv2.VideoCapture(args.video)
        output_file = args.video[:-4].rsplit('/')[-1] + '_yoloface.avi'


    # Get the video writer initialized to save the output video
    if not args.image:
        video_writer = cv2.VideoWriter(os.path.join(args.output_dir, output_file),
                                       cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                       cap.get(cv2.CAP_PROP_FPS), (
                                           round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                           round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

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
        faces = post_process2(frame, outs, CONF_THRESHOLD, NMS_THRESHOLD)
        print(faces)
        #### image = cv2.imread(args["image"])
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb, faces)

        # initialize the list of names for each face detected
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
	        # encodings
            matches = face_recognition.compare_faces(data["encodings"],
	        	encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
        		# find the indexes of all matched faces then initialize a
	         	# dictionary to count the total number of times each face
	         	# was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

	          	# loop over the matched indexes and maintain a count for
	    	    # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

    	    	# determine the recognized face with the largest number of
        		# votes (note: in the event of an unlikely tie Python will
        		# select first entry in the dictionary)
                name = max(counts, key=counts.get)

        	# update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(faces, names):
        	# draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
    	    	0.75, (0, 255, 0), 2)

        # Save the output video to file
        if args.video:
            # cv2.imwrite(os.path.join(args.output_dir, output_file), frame.astype(np.uint8))
            video_writer.write(frame.astype(np.uint8))

#        cv2.imshow(wind_name, frame)

        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            print('[i] ==> Interrupted by user!')
            break

    cap.release()
    cv2.destroyAllWindows()

    print('==> All done!')
    print('***********************************************************')
    end = datetime.datetime.now()
    print('start time : ', now)
    print('end time : ', end)


if __name__ == '__main__':
    _main()
