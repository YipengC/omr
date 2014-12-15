import sys
import cv2
import numpy as np
import omr_classes
import pickle

img = cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)

sheetFile = open("sheet","r")
currentSheet = pickle.load(sheetFile)

for y in currentSheet.staff.tops:
	for i in range(0,5):
	#	for x in range(0,currentSheet.width):
		for j in range(0,currentSheet.staff.lineThickness+1):
		#	img[y+currentSheet.staff.lineSpacing*i+j,x] = 255
			currentY = y + currentSheet.staff.lineSpacing*i + j
			cv2.line(img,(0,currentY),(currentSheet.width,currentY),255)
	
# Fix broken objects by erosion followed by dilation
kernel = np.ones((currentSheet.staff.lineThickness*2,currentSheet.staff.lineThickness*2),np.uint8)
img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

# Output image with staff lines removed
parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('staff_removal_' + imageName + '.png',img)
