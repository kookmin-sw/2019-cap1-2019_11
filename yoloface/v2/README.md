YOLOFACE + FACE RECOGNITION  Version.2
==================

In Mac
------

가상환경 실행 - source ./yoloface/bin/activate
카메라 실행 및 학습시킬 얼굴 저장 - python cameraAdd.py ( s - 저장 , q - 종료 )
gpu 실시간 웹캠 - python yoloface_gpu.py --video stream
cpu 실시간 웹캠 => python yoloface_cam.py
비디오 업로드 => python yoloface_video.py --video samples/filename
