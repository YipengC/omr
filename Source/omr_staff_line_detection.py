import cv2
import numpy as np
import sys

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

	cv2.line(imgHoughLines,(x1,y1),(x2,y2),(0,0,255),2)

# Output image with Hough lines
parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('hough_output_' + imageName + '.jpg',imgHoughLines)

# Find staff line spacing

# Find average difference in rho
sortedHoughLines = sorted(houghLines[0],key = lambda x : x[0])

rhoDifferences = np.zeros((len(sortedHoughLines)-1))
for i in range(0,len(sortedHoughLines)-1):
	rhoDifferences[i] = sortedHoughLines[i+1][0] - sortedHoughLines[i][0]

sortedRhoDifferences = sorted(rhoDifferences)
medianRho = sortedRhoDifferences[len(sortedRhoDifferences)/2]

print(sortedRhoDifferences)

print("medianRho: " + str(medianRho))
