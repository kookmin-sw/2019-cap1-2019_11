import cv2, re

mosaic_rate = 30

image = cv2.imread('./input.jpg')

image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# excute face detection
cascade = cv2.CascadeClassifier()
face_list = cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(50, 50))

if len(face_list) == 0:
    print("no face")
    quit()

# do mosaic to identified section
print(face_list)
color = (0, 0, 255)
for ( x, y, w, h) in face_list:
    # extract face 
    face_img = image[x:y+h, x:x+w]
    # resizing
    face_img = cv2.resize(face_img, (w//mosaic_rate, h//mosaic_rate))
    face_img = cv2.resize(face_img, (w, h), interpolation=cv2.INTER_AREA)
    # merging
    image[y:y+h, x:x+h] = face_img

cv2.imwrite('output.jpg', image)
