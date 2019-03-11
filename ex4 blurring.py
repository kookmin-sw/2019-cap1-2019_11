import cv2
import numpy as np
img =cv2.imread('input.jpg') 
rows, cols = img.shape[:2] #slicing
kernel_identity = np.array([[0,0,0],[0,1,0],[0,0,0]])

kernel_3x3 = np.ones((3,3),np.float32) / 9.0 #divide by 9 to normalize the kernel
kernel_5x5 = np.ones((5,5),np.float32) / 25.0 #divide by 25 to normalize the kernel
kernel_10x10 = np.ones((20,20),np.float32) / 400.0


cv2.imshow('original',img)

output = cv2.filter2D(img, -1, kernel_identity) 
cv2.imshow('original filter', output)

output = cv2.filter2D(img, -1, kernel_3x3)
cv2.imshow('3x3 filter', output)

output = cv2.filter2D(img, -1, kernel_5x5)
cv2.imshow('5x5 filter', output)

output = cv2.filter2D(img, -1, kernel_10x10)
cv2.imshow('20x20 filter', output)

cv2.imwrite('10x10 filtered blur.jpg', img)

cv2.waitKey(0)

cv2.destroyAllWindows()
