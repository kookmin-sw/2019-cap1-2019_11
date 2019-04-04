!python yoloface.py --image examples/example_02.png --encodings encodings.pickle




==============================================
In Mac - Colab

from google.colab import auth
auth.authenticate_user()
from google.colab import drive
drive.mount('/content/gdrive')

%cd gdrive/'My Drive'/colab/yoloface/yoloface
!pip install virtualenv
!pip install face_recognition


학습명령어 - !python encode_faces.py --dataset dataset --encodings encodings.pickle
이미지 명령어 - !python yoloface --image samples/example_05.png --encodings encodings.pickle
동영상 명령어 - !python yoloface_video.py --video samples/test.mp4 --encodings encodings.pickle
GPU 명령어 - !python yoloface_gpu.py --video samples/test2.mp4 --encodings encodings.pickle
