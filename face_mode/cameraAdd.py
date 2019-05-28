# -*- coding: utf-8 -*-
# 캠 캡쳐한다.

import numpy as np
import cv2
import os

# 캠 캡쳐 핸들 가져온다
cap = cv2.VideoCapture(0)
path = '~/Desktop/face_asia/dFace/yoloface'
count = 0
# 루프문
while(True):
    count = count + 1
    # 캡쳐 Frame
    ret, frame = cap.read()
    # print(count)
    ## 프레임 컬러 설정함
    # gray = cv2.cvtColor(frame)

    ## 윈도우 프레레임에 보임
    cv2.imshow('frame',frame)

    # if count % 20 == 0:
    #     cv2.imwrite('knowns/save{0}.jpg'.format(count/20),frame)
    #
    #
    k=cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite('knowns/save{0}.jpg'.format(count/20),frame)
        print('save success')


# 캠 리소스 해제
cap.release()
# 윈도우즈 해제
cv2.destroyAllWindows()


#~/Desktop/face_asia/dFace/yoloface
