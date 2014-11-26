import cv2
import numpy as np
import sys

inputImage = cv2.imread(sys.argv[1])

imageGray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

# Binarize using adaptive thresholding
imageBinarized = cv2.adaptiveThreshold(imageGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 2)

imageWidth = len(imageBinarized[0])
imageHeight = len(imageBinarized)

print('imageWidth: ' + str(imageWidth))
print('imageHeight: ' + str(imageHeight))

# Begin connected-component labeling algorithm

# Stores the smallest equivalence label for label i in smallestLabels[i]
smallestLabels = [0]

nextLabel = 1

# The labels for each pixel on the first pass
labels = np.zeros([imageHeight,imageWidth],dtype=np.int)

# First pass
for row in range(0,imageHeight):
	for column in range(0,imageWidth):
		print(nextLabel)
		# If current cell is not a background pixel
		if (imageBinarized[row][column] != 0):
			# Find values of west and north neighbour pixels to current pixel
			# Neighbours:
			west = 0
			north = 0

			if (column != 0):
				west = imageBinarized[row][column-1]
			if (row != 0):
				north = imageBinarized[row-1][column]

			if ((west == 0) and (north == 0)):
				# Place pixel in new set
				labels[row][column] = nextLabel
				smallestLabels.append(nextLabel)
				nextLabel = nextLabel + 1
			elif (north == 0):
				# Only west is foreground so add pixel to same set as pixel to the west
				labels[row][column] = labels[row][column-1]
			elif (west == 0):
				# Only north is foreground so add pixel to same set as pixel to the north
				labels[row][column] = labels[row-1][column]
			else:
				# Both north and west are foreground. Add pixel to west set and union the two sets if they are not the same
				westLabel = labels[row][column-1]
				northLabel = labels[row-1][column]

				if (westLabel == northLabel):
					labels[row][column] = westLabel
				else:
					minLabel = min(westLabel,northLabel)
					smallestLabels[westLabel] = minLabel
					smallestLabels[northLabel] = minLabel
					labels[row][column] = minLabel

# Second pass
finalLabels = np.zeros([imageHeight,imageWidth],dtype=np.int)
for row in range(0,imageHeight):
	for column in range(0,imageWidth):
		finalLabels[row][column] = smallestLabels[labels[row][column]]

# Determine label frequencies
labelFrequencies = [0]*nextLabel

for row in finalLabels:
	for element in row:
		labelFrequencies[element] = labelFrequencies[element] + 1

# Determine label with greatest frequency
largestFrequencyLabel = 0
largestFrequency = 0

for label in range(0,len(labelFrequencies)):
	if (labelFrequencies[label] > largestFrequency):
		largestFrequency = labelFrequencies[label]
		largestFrequencyLabel = label

print('largestFrequencyLabel: ' + str(largestFrequencyLabel))
print('largestFrequency: ' + str(largestFrequency))

# Construct binary image with all pixels labelled with largestFrequencyLabel set to 255 and 0 otherwise

outputImage = np.zeros([imageHeight,imageWidth],dtype=np.int)

for row in range(0,imageHeight):
	for column in range(0,imageWidth):
		if (finalLabels[row][column] == largestFrequencyLabel):
			outputImage[row][column] = 255			

# Output
parsedFilePath = sys.argv[1].split('/')
print('parsedFilePath: ' + str(parsedFilePath))
imageName = parsedFilePath[-1].split('.')[0]
print('imageName: ' + imageName)
cv2.imwrite('lcc_threshold_output_' + imageName + '.jpg',imageBinarized)
cv2.imwrite('lcc_output_' + imageName + '.jpg', outputImage)
