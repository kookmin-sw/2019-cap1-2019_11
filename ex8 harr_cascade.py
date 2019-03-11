import cv2
import numpy as np

img =cv2.imread('input.jpg') 
image_gs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")


face_list = face_cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(50,50))

if len(face_list) == 0:
    print("no face")
    quit()

color = (0, 0, 255)

for (x,y,w,h) in face_list:
    face_img = img[y:y+h, x:x+w]
    face_img = cv2.resize(face_img, (w//10, h//10))
    face_img = cv2.resize(face_img, (w, h), interpolation=cv2.INTER_AREA)
    img[y:y+h, x:x+w] = face_img
cv2.imwrite('output.jpg', img)
