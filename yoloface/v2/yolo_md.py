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

from yolo.model import eval

from keras import backend as K
from keras.models import load_model
from timeit import default_timer as timer
from PIL import ImageDraw, Image


class YOLO(object):
    def __init__(self, args):
        self.args = args
        self.model_path = args.model
        self.classes_path = args.classes
        self.anchors_path = args.anchors
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self._generate()
        self.model_image_size = args.img_size
        self.known_face_encodings = []
        self.known_face_names = []
        
        dirname='knowns'
        files=os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)
        
        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def _generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith(
            '.h5'), 'Keras model or weights must be a .h5 file'

        # load model, or construct model and load weights
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            # make sure model, anchors and classes match
            self.yolo_model.load_weights(self.model_path)
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                   num_anchors / len(self.yolo_model.output) * (
                           num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'
        print(
            '*** {} model, anchors, and classes loaded.'.format(model_path))

        # generate colors for drawing bounding boxes
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))

        # shuffle colors to decorrelate adjacent classes.
        np.random.seed(102)
        np.random.shuffle(self.colors)
        np.random.seed(None)

        # generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2,))
        boxes, scores, classes = eval(self.yolo_model.output, self.anchors,
                                           len(self.class_names),
                                           self.input_image_shape,
                                           score_threshold=self.args.score,
                                           iou_threshold=self.args.iou)
        return boxes, scores, classes

    def detect_image(self, image):
        start_time = timer()
        if self.model_image_size != (None, None):
            assert self.model_image_size[
                       0] % 32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[
                       1] % 32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(
                reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')
        print(image_data.shape)
        image_data /= 255.
        # add batch dimension
        image_data = np.expand_dims(image_data, 0)
        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        print('*** Found {} face(s) for this image'.format(len(out_boxes)))
        thickness = (image.size[0] + image.size[1]) // 400
        
        final_boxes=[]

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]
            text = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

            
            final_boxes.append([top,right,bottom,left])
            print('top : ', top,' right : ', right,' bottom : ', bottom, ' left : ',left)
            for thk in range(thickness):
                draw.rectangle(
                    [left + thk, top + thk, right - thk, bottom - thk],
                    outline=(51, 178, 255))
            del draw

        return image, out_boxes,final_boxes

    def close_session(self):
        self.sess.close()


def letterbox_image(image, size):
    '''Resize image with unchanged aspect ratio using padding'''

    img_width, img_height = image.size
    w, h = size
    scale = min(w / img_width, h / img_height)
    nw = int(img_width * scale)
    nh = int(img_height * scale)

    image = image.resize((nw, nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128, 128, 128))
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
    return new_image


def detect_video(model, video_path=None, output=None):
    if video_path == 'stream':
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")

    video_fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video_fps = vid.get(cv2.CAP_PROP_FPS)
    print(video_fps)

    # the size of the frames to write
    video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    isOutput = True if output != "" else False
    if isOutput:
        output_fn = 'output_video.avi'
        out = cv2.VideoWriter(os.path.join(output, output_fn), video_fourcc, video_fps, video_size)

    while True:
        ret, frame = vid.read()
        if ret:
            
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            image = Image.fromarray(rgb_small_frame)
            image, faces, final_boxes= model.detect_image(image)
            
            if model.process_this_frame:
                print('process_this_frame')
                model.face_encodings = face_recognition.face_encodings(rgb_small_frame, final_boxes)
            
                model.face_names=[]
            
                for face_encoding in model.face_encodings :
                    distances = face_recognition.face_distance(model.known_face_encodings, face_encoding)
                    min_value = min(distances)


                    name = "Unknown"
                    if min_value < 0.42 :
                        index=np.argmin(distances)
                        name=model.known_face_names[index]
                    model.face_names.append(name)
                    
            model.process_this_frame=not model.process_this_frame
            

            for (top,right,bottom,left), name in zip(final_boxes, model.face_names):
            
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                #### GaussianBlur 방식
                #
#                if name == 'Unknown':
#                    # Extract the region of the image that contains the face
#                    face_image = frame[top:bottom, left:right]
#
#                    # Blur the face image
#                    face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
#
#                    # Put the blurred face region back into the frame image
#                    frame[top:bottom, left:right] = face_image

                ### resize 사용하여 모자이크
                if name == 'Unknown':
                    face_img = frame[top:bottom, left:right]
                    a=(right-left)//30
                    b=(bottom-top)//30
                    if a <= 0 :
                        a=1
                    if b <= 0 :
                        b=1
                    face_img = cv2.resize(face_img, (a, b))
                    face_img = cv2.resize(face_img, (right-left, bottom-top), interpolation=cv2.INTER_AREA)

                    frame[top:bottom, left:right]=face_img

                cv2.rectangle(frame, (left, top), (right, bottom+10), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
                if video_path == 'stream':
                    cv2.imshow("face", frame)
                        
            if isOutput:
                out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    vid.release()
    out.release()
    cv2.destroyAllWindows()
    # close the session
    model.close_session()
