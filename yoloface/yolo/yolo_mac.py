
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

CONF_THRESHOLD = 0.3
NMS_THRESHOLD = 0.2
IMG_WIDTH = 416
IMG_HEIGHT = 416

COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (0, 255, 255)

class YOLO(object):
    def __init__(self, args):
        self.args = args
        self.model_path = args.model
        self.classes_path = args.classes
        self.anchors_path = args.anchors
        
        #추가
#        self.encodings=args.encodings

        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self._generate()
        self.model_image_size = args.img_size

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
    
    
    def detect_image(self, image, encodings):
#        data = pickle.loads(open(encodings, "rb").read(),encoding='latin1')
#        print(data)
        start_time = timer()
        print('success')
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
        #print('image shape', image_data.shape)
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
            
            
            ##########
            text = '{} {:.2f}'.format(predicted_class, score)
            
            draw = ImageDraw.Draw(image)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            
            #top, right, bottom, left
            #print(text, (left, top), (right, bottom))
            print(text, (top, right), (bottom, left))
#            final_boxes.append([left,top,right,bottom])
            final_boxes.append([top,right,bottom,left])
            for thk in range(thickness):
                draw.rectangle(
                    [left + thk, top + thk, right - thk, bottom - thk],
                    outline=(51, 178, 255))
            del draw

        end_time = timer()
        print('*** Processing time: {:.2f}ms'.format((end_time -
                                                          start_time) * 1000))
        return image, out_boxes, final_boxes

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


## encoding
def detect_video(model, video_path=None, output=None, encodings=None):
    print('mo')
    data = pickle.loads(open(encodings, "rb").read(),encoding='latin1')
    now = datetime.datetime.now()
    if video_path == 'stream':
        print('test stream')
        vid = cv2.VideoCapture(0)
    else:
        print('here')
        vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")

    
#    video_fourcc = cv2.VideoWriter_fourcc('M', 'G', 'P', 'G')
    video_fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

#    video_fps = vid.get(cv2.CAP_PROP_FPS)/2
    video_fps = vid.get(cv2.CAP_PROP_FPS)
    print("video_fps : ",video_fps)

    # the size of the frames to write
    video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    isOutput = True if output != "" else False
    if isOutput:
        output_fn = 'output_video.avi'
        out = cv2.VideoWriter(os.path.join(output, output_fn), video_fourcc, video_fps, video_size)
    #out = cv2.VideoWriter(os.path.join(output, output_fn), video_fourcc, 11, video_size)

    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = timer()
    cnt=0
    mosaic_rate = 30


    while True:
        ret, frame = vid.read()
        
        if ret:
            print('Start part')
            image = Image.fromarray(frame)
            image, faces, final_boxes = model.detect_image(image,encodings)
                    
            result = np.asarray(image)
                    
            #top, right, bottom, left
            print('face입니다', faces)
            print('fb=',final_boxes)
            #final_boxes.append([left,top,right,bottom])
            names=[]
           
            to=[]
            ri=[]
            bo=[]
            le=[]
            un_count=0
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb, final_boxes)
                    
            for encoding in encodings:
                matches=face_recognition.compare_faces(data["encodings"],encoding)
                name = "unknown"
                        
                if True in matches:
                    matchedIdxs = [i for (i,b) in enumerate(matches) if b]
                    counts={}
                            
                    for i in matchedIdxs:
                        name=data["names"][i]
                        counts[name]=counts.get(name,0)+1
                            
                    name=max(counts,key=counts.get)
                print('name = ',name)
                if name == 'unknown':
                    un_count += 1
                names.append(name)
            #top, right, bottom, left
            #for ((left, top, right, bottom), name) in zip(final_boxes, names):
            for ((top, right, bottom, left), name) in zip(final_boxes, names):
                # draw the predicted face name on the image
                if name == 'unknown':
                    le.append(left)
                    to.append(top)
                    ri.append(right)
                    bo.append(bottom)
                    
                    mosaic_image=frame[to[0]:bo[0], le[0]:ri[0]]
                    print('top : ',to[0])
                    print('bottom : ',bo[0])
                    print('left : ',le[0])
                    print('right : ',ri[0])
                    print('tmp : ',bo[0]-to[0],' ',ri[0]-le[0])
                    a=(bo[0]-to[0])//13
                    b=(ri[0]-le[0])//13
                    
                    if a < 0 :
                        a=1
                    if b < 0 :
                        b=1
                       
                    mosaic_image=cv2.resize(mosaic_image, (a,b))
                    mosaic_image=cv2.resize(mosaic_image, (ri[0]-le[0],bo[0]-to[0]), interpolation=cv2.INTER_AREA)
                    

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    #y = top - 15 if top - 15 > 15 else top + 15
#                    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
#                        0.75, (0, 255, 0), 2)
                        #frame[to[0]:bo[0], le[0]:ri[0]]=mosaic_image
                    frame[to[0]:bo[0], le[0]:ri[0]]=mosaic_image
                else :
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        #y = top - 15 if top - 15 > 15 else top + 15
#                    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
#                                0.75, (0, 255, 0), 2)

                    
            if isOutput:
                out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    


    end = datetime.datetime.now()
    print(now)
    print(end)
    vid.release()
    out.release()
    cv2.destroyAllWindows()
    # close the session
    model.close_session()
