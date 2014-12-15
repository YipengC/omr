import sys
import cv2
import numpy as np

img = cv2.imread(sys.argv[1],0)

# Invert the image
img = 255 - img

contours,hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

imgContours = img.copy()

cv2.drawContours(imgContours,contours,-1,127)
cv2.imshow('contours',imgContours)
cv2.waitKey(0)
cv2.destroyAllWindows()
