import sys
import cv2
import numpy as np
import omr_classes

# Input: img - a thresholded sheet music image. staff - an omr_classes.staff object corresponding to img
# Output: img with staff lines removed (the method is also destructive - the input is modified)
def removeStaffLines(img,staff):
	width = len(img[0])
	
	# Kernel for dilation and erosion operations
	kernel = np.ones((2,2),np.uint8)
	# Dilate
	img = cv2.dilate(img,kernel,iterations=1)

	# Remove staff lines
	for y in staff.tops:
		for i in range(-2,7):
			for j in range(0,staff.lineThickness+1):			
				currentY = y + staff.lineSpacing*i + j
				cv2.line(img,(0,currentY),(width,currentY),255)
	
	# Erode
	img = cv2.erode(img,kernel,iterations=1)

	# Fix broken objects by erosion followed by dilation
	kernel = np.ones((staff.lineThickness*2,staff.lineThickness*2),np.uint8)
	img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

	# Output image with staff lines removed
	parsedFilePath = sys.argv[1].split('/')
	imageName = parsedFilePath[-1].split('.')[0]
	cv2.imwrite('staff_removal_' + imageName + '.png',img)

	return img

def removeStaffLinesSP(img,staff):
	staffLineSpacing = staff.lineSpacing
	staffLineThickness = staff.lineThickness
	# Threshold for black pixel height
	threshold = staffLineSpacing/2
	width = len(img[1])
	
	for i in staff.tops:
		for y in range(0,4*staffLineSpacing+1,staffLineSpacing):
			# For each staff line, 
			print("i + y: " + str(i + y))
			startX = 0
			for x in range(width-1,0,-1):
				if (img[i+y,x] == 0):
					startX = x
					#cv2.rectangle(img,(0,0),(x,i+y),127)
					break
			yRef = i+y
			for x in range(x,0,-1):
				if (not(img[yRef,x] == 0)):
					# Find closest black pixel vertically
					for j in range(1,threshold/2):
						if (img[yRef+j,x] == 0):
							yRef = yRef + j
							break
						if (img[yRef-j,x] == 0):
							yRef = yRef - j
							break
				verticalThresholdResult = testVerticalThreshold(img,x,yRef,staffLineThickness*5/4)
				#if (verticalThresholdResult[0]):
				#	yRef = (verticalThresholdResult[1] + verticalThresholdResult[2]) / 2
				if (verticalThresholdResult[0]):
					cv2.line(img,(x,verticalThresholdResult[1]),(x,verticalThresholdResult[2]),255)

	# Fix broken objects by erosion followed by dilation
	kernel = np.ones((staff.lineThickness,staff.lineThickness),np.uint8)
	img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

	# Output image with staff lines removed
	parsedFilePath = sys.argv[1].split('/')
	imageName = parsedFilePath[-1].split('.')[0]
	cv2.imwrite('staff_removal_' + imageName + '.png',img)

	return img

def testVerticalThreshold(img,x,y,threshold):
	upperY = y
	lowerY = y
	while (upperY >= 0):
		if (img[upperY-1,x] == 0):
			upperY -= 1
		else:
			break
	while (lowerY <= len(img)):
		if (img[lowerY+1,x] == 0):
			lowerY += 1
		else:
			break
	return (lowerY - upperY <= threshold),upperY,lowerY
