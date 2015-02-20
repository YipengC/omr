import cv2
import numpy as np

def getStaffPositions(img,staffData):
	staffPositions = []
	trebles = staffData.trebles
	basses = staffData.basses
	for i in range(0,len(trebles)):
		staffPositions.append((trebles[i],basses[i]+4*(staffData.lineSpacing + staffData.lineThickness)))
	return staffPositions

def getLinePositions(img,top,bottom):
	width = len(img[0])
	roi = img[top:bottom,:]
	height = len(roi)
	# Invert the image
	roi = 255 - roi
	# Perform hough line transform
	lines = cv2.HoughLines(roi,1,np.pi/180,height*3/4)
	for rho,theta in lines[0]:
		if (rho < 0):
			rho = -rho
			theta = theta - np.pi

	linePositions = []
	y = (top + bottom) / 2
	for rho,theta in lines[0]:
		if (abs(theta) < 0.157):
			linePositions.append((int(rho),y))
	return linePositions
# Given img, an image with staff lines removed, locate all of the bar lines on the page
def detectBarLines(img,staffData):
	# Detect positions of the staffs
	staffPositions = getStaffPositions(img,staffData)

	# For each staff, detect bar lines
	barLines = []
	for top,bottom in staffPositions:
		barLines.append(getLinePositions(img,top,bottom))

	return barLines
