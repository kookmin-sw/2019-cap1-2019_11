import argparse

#from yolo.yolo import YOLO, detect_video, detect_img, letterbox_image
from yolo.yolo import YOLO, detect_video, letterbox_image
import face_recognition
import os
import datetime
import time
#####################################################################
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='model-weights/YOLO_Face.h5',
                        help='path to model weights file')
    parser.add_argument('--anchors', type=str, default='cfg/yolo_anchors.txt',
                        help='path to anchor definitions')
    parser.add_argument('--classes', type=str, default='cfg/face_classes.txt',
                        help='path to class definitions')
    parser.add_argument('--score', type=float, default=0.5,
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
    parser.add_argument('--encodings', required=True,
                        help="path to serialized db of facial encodings")

    
    args = parser.parse_args()
    return args


def _main():
#    print(os.environ['DISPLAY'])
    # Get the arguments
    args = get_args()
    print(args)
    now = datetime.datetime.now()

    if args.image:
        # Image detection mode
        print('[i] ==> Image detection mode\n')
        detect_img(YOLO(args), args.image)
    else:
        print('[i] ==> Video detection mode\n')
        # Call the detect_video method here
        # ******* args.encodings 추가
        detect_video(YOLO(args), args.video, args.output, args.encodings)

    
    print('Well + done!!!')
    end = datetime.datetime.now()
    print(now)
    print(end)

if __name__ == "__main__":
    _main()
