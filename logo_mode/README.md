# Brand Logo Blurring System

This system could detect 16 brand logos.

Adidas  Apple  BMW  Cocacola  Ferrari  Google
Heineken  McDonalds  Mini  Nike  Pepsi  Porsche
Puma  RedBull  Sprite  Starbucks

---

Weights file link : https://nas.gclab.cs.kookmin.ac.kr:5001/sharing/tizrp8gfx

Weights file path : model_data/yolo_logos.h5

---
## Quick start

Webcam mode :  python blur_logo.py --webcam         
Input video or image mode : python blur_logo.py --input "File path" --output "File path"        

---
### Usage
Use --help to see usage of yolo_video.py:
```
usage: blur_logo.py [-h] [--model MODEL] [--anchors ANCHORS]
                     [--classes CLASSES] [--gpu_num GPU_NUM]
                     [--input] [--output][--webcam]

positional arguments:
  --input        Video input path
  --output       Video output path

optional arguments:
  -h, --help         show this help message and exit
  --model MODEL      path to model weight file, default model_data/yolo.h5
  --anchors ANCHORS  path to anchor definitions, default
                     model_data/yolo_anchors.txt
  --classes CLASSES  path to class definitions, default
                     model_data/coco_classes.txt
  --gpu_num GPU_NUM  Number of GPU to use, default 1
```
---

4. MultiGPU usage: use `--gpu_num N` to use N GPUs. It is passed to the [Keras multi_gpu_model()](https://keras.io/utils/#multi_gpu_model).

---

The original code address : https://github.com/qqwweee/keras-yolo3