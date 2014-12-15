import cv2
import numpy as np
import sys
from scipy import stats
import omr_classes
import pickle

def isTopStaffLine(rho,rhoValues,gap,threshold):
	for i in range(1,5):
		member = False
		for j in range(0,threshold+1):
			if ((rho + i*gap + j) in rhoValues or (rho + i*gap - j) in rhoValues):
				member = True
		if (not(member)):
			return False
	return True

# Read in image from file
imgInput = cv2.imread(sys.argv[1])

width = len(imgInput[0])
height = len(imgInput)

# Convert to grayscale
imgGray = cv2.cvtColor(imgInput,cv2.COLOR_BGR2GRAY)

# Threshold
imgBinary = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,99,2)

# Apply Hough line transform
houghLines = cv2.HoughLines(imgBinary,1,np.pi/180,min(width,height)/2)

# Show lines on copy of input image
imgHoughLines = imgInput.copy()

for rho,theta in houghLines[0]:
	print('rho: ' + str(rho) + ' theta: ' + str(theta))
	cosTheta = np.cos(theta)
	sinTheta = np.sin(theta)
	x0 = cosTheta*rho
	y0 = sinTheta*rho
	length = max(width,height)
	x1 = int(x0 + length * (-sinTheta))
	y1 = int(y0 + length * (cosTheta))
	x2 = int(x0 - length * (-sinTheta))
	y2 = int(y0 - length * (cosTheta))

	cv2.line(imgHoughLines,(x1,y1),(x2,y2),(0,0,255),1)

# Output image with Hough lines
parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('hough_output_' + imageName + '.jpg',imgHoughLines)

# Find staff line spacing

# Find average difference in rho
sortedHoughLines = sorted(houghLines[0],key = lambda x : x[0])

print(sortedHoughLines)

rhoDifferences = np.zeros((len(sortedHoughLines)-1))
for i in range(0,len(sortedHoughLines)-1):
	rhoDifferences[i] = sortedHoughLines[i+1][0] - sortedHoughLines[i][0]

sortedRhoDifferences = sorted(rhoDifferences)
medianRho = int(sortedRhoDifferences[len(sortedRhoDifferences)/2])

print(sortedRhoDifferences)

print("medianRho: " + str(medianRho))

# Now we keep only lines with theta between 1.56 and 1.58. We also only store rho values from now on

sortedRhoValues = []
for rho,theta in sortedHoughLines:
	if (1.56 < theta and theta < 1.58):
		sortedRhoValues.append(int(rho))

print(sortedRhoValues)

# Find rho value of top line of each stave
staffTops = []

for rho in sortedRhoValues:
	if (isTopStaffLine(rho,sortedRhoValues,medianRho,1)):
		staffTops.append(rho)

print(staffTops)

# Show staff lines on copy of input image
imgStaffLines = imgInput.copy()

for rho in staffTops:
	for i in range(0,5):
		y = rho + i*medianRho
		cv2.line(imgStaffLines,(0,y),(width-1,y),(0,0,255),1)

# Output image with staff lines
parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('staff_output_' + imageName + '.jpg',imgStaffLines)

# Find most common black pixel run length (white pixel run length in binary image due to inversion)
# This should correspond to staff line thickness

runLengths = []

for x in range(width*1/4,width*3/4):
	inWhite = False
	currentRun = 0
	for y in range(0,height):
		if (imgBinary[y,x] == 255):
			if (inWhite):
				currentRun = currentRun + 1
			else:
				currentRun = 1
				inWhite = True
		else:
			if (inWhite):
				runLengths.append(currentRun)
				inWhite = False

staffLineThickness = int(stats.mode(runLengths)[0][0])
print(staffLineThickness)

currentStaff = omr_classes.Staff(medianRho,staffLineThickness,staffTops)
currentSheet = omr_classes.Sheet(currentStaff,width,height)

sheetFile = open("sheet","w")

pickle.dump(currentSheet,sheetFile)

sheetFile.close()
