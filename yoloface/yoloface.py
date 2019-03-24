# *******************************************************************
# Face detection using yoloface + face recognition
# Kookmin university sw 2019 capstone design <Bblur> team demo code

# ********************************************************************
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
import cv2
import face_recognition
import pickle
from utils import *

#####################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--model-cfg', type=str, default='drive/Colab/yoloface/cfg/yolov3-face.cfg',  #'drive/Colab/yoloface/cfg/yolov3-face.cfg'
                    help='path to config file')
parser.add_argument('--model-weights', type=str,
                    default='drive/Colab/yoloface/model-weights/yolov3-wider_16000.weights',
                    help='path to weights of model')
parser.add_argument('--image', type=str, default='',
                    help='path to image file')
parser.add_argument('--video', type=str, default='',
                    help='path to video file')
parser.add_argument('--src', type=int, default=0,
                    help='source of the camera')
parser.add_argument('--output-dir', type=str, default='drive/Colab/yoloface/outputs/',
                    help='path to the output directory')
parser.add_argument("--encodings", required=True, help="path to serialized db of facial encodings")
args = parser.parse_args()

#####################################################################
# print the arguments
print('----- info -----')
print("[i] loading encodings...")
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
data = pickle.loads(open(args.encodings, "rb").read())
net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def post_process2(frame, outs, conf_threshold, nms_threshold):
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only
    # the ones with high confidence scores. Assign the box's class label as the
    # class with the highest score.
    confidences = []
    boxes = []
    final_boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                width = int(detection[2] * frame_width)
                height = int(detection[3] * frame_height)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant
    # overlapping boxes with lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold,
                               nms_threshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        right = box[2] + left
        bottom = box[3] + top
        final_boxes.append([top, right, bottom, left])
    return final_boxes


def _main():
    wind_name = 'face detection using YOLOv3'
#    cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)

    output_file = ''

    if args.image:
        if not os.path.isfile(args.image):
            print("[!] ==> Input image file {} doesn't exist".format(args.image))
            sys.exit(1)
        cap = cv2.VideoCapture(args.image)
        image = cv2.imread(args.image)
        output_file = args.image[:-4].rsplit('/')[-1] + '_yoloface.jpg'
    elif args.video:
        if not os.path.isfile(args.video):
            print("[!] ==> Input video file {} doesn't exist".format(args.video))
            sys.exit(1)
        cap = cv2.VideoCapture(args.video)
        output_file = args.video[:-4].rsplit('/')[-1] + '_yoloface.avi'
    else:
        # Get data from the camera
        cap = cv2.VideoCapture(args.src)

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
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
    	    	0.75, (0, 255, 0), 2)
        '''
        print('[i] ==> # detected faces: {}'.format(len(faces)))
        print('#' * 60)
        print('faces : ', faces)

        # initialize the set of information we'll displaying on the frame
        info = [
            ('number of faces detected', '{}'.format(len(faces)))
        ]

        for (i, (txt, val)) in enumerate(info):
            text = '{}: {}'.format(txt, val)
            cv2.putText(frame, text, (10, (i * 20) + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_RED, 2)
        '''
        # Save the output video to file
        if args.image:
            # cv2.imwrite(os.path.join(args.output_dir, output_file), frame.astype(np.uint8))
            cv2.imwrite(os.path.join(args.output_dir, output_file), image)
        else:
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


if __name__ == '__main__':
    _main()
