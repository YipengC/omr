import sys
import cv2
import numpy as np
import omr_classes

# Input: img - a thresholded sheet music image. staff - an omr_classes.staff object corresponding to img
# Output: img with staff lines removed (the method is also destructive - the input is modified)
def removeStaffLines(img,staff):
	width = len(img[0])
	for y in staff.tops:
		for i in range(0,5):
			for j in range(0,staff.lineThickness+1):			
				currentY = y + staff.lineSpacing*i + j
				cv2.line(img,(0,currentY),(width,currentY),255)
	
	# Fix broken objects by erosion followed by dilation
	kernel = np.ones((staff.lineThickness*2,staff.lineThickness*2),np.uint8)
	img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

	return img

	# Output image with staff lines removed
	"""
	parsedFilePath = sys.argv[1].split('/')
	imageName = parsedFilePath[-1].split('.')[0]
	cv2.imwrite('staff_removal_' + imageName + '.png',img)
	"""
