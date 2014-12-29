import sys
import cv2
import numpy as np

img = cv2.imread(sys.argv[1],0)

# Invert the image
img = 255 - img

contours,hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

imgContours = np.zeros(img.shape,dtype=np.uint8)

cv2.drawContours(imgContours,contours,-1,255)

boundingBoxes = []

for contour in contours:
	boundingBoxes.append(cv2.boundingRect(contour))

for x,y,w,h in boundingBoxes:
	cv2.rectangle(imgContours,(x,y),(x+w,y+h),127,1)

parsedFilePath = sys.argv[1].split('/')
print('parsedFilePath: ' + str(parsedFilePath))
imageName = parsedFilePath[-1].split('.')[0]
print('imageName: ' + imageName)
cv2.imwrite('contours_' + imageName + '.png',imgContours)

