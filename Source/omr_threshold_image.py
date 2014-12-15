import sys
import cv2

img = cv2.imread(sys.argv[1])
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,99,2)

# Output image

parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('binary_' + imageName + '.png',img)
