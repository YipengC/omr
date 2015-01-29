import cv2
import numpy as np
import math
import omr_classes

def dist(a,b):
	return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def average(points):
	sumX = 0
	sumY = 0
	for point in points:
		sumX += point[0]
		sumY += point[1]
	n = len(points)
	return (sumX/n,sumY/n)

def removeDuplicateMatches(threshold,points):
	result = []
	while (points):
		# currentPoints is a list of the current points to be averaged into a single point due to correspondence to the same object
		currentPoints = []
		# nextPoints is a list of the points not removed in the current iteration
		nextPoints = []
		# referencePoint is the point being compared to all of the others in the current iteration
		referencePoint = points[0]
		currentPoints.append(referencePoint)
		if (len(points) > 1):
			for i in range(1,len(points)):
				comparePoint = points[i]
				if (dist(referencePoint,comparePoint) < threshold):
					currentPoints.append(comparePoint)
				else:
					nextPoints.append(comparePoint)
		result.append(average(currentPoints))
		points = nextPoints
	return result

def matchTemplates(img,staffData):
	templatePath = '../Resources/Templates/'

	templates = (
		('treble clef','treble_clef_template.png',20),
		('bass clef','bass_clef_template.png',20),
		('crotchet rest','crotchet_rest_template.png',20),
		('time signature 4','time_signature_4_template.png',20),
		('time signature 3','time_signature_3_template.png',20),
		('quaver rest','quaver_rest_template.png',20),
		('semibreve rest','semibreve_rest_template.png',20),
		('sharp','sharp_template.png',20),
		('natural','natural_template.png',20),
		('flat','flat_template.png',20),
	#	('note head','note_head_template.png',20),
		('note head','note_head_2_template.png',20),
		('minim note head','minim_note_head_template.png',20)
	)

	methods = [cv2.TM_CCOEFF,cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR,cv2.TM_CCORR_NORMED,cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]

	# Each dictionary value is a list of MusicalObjects identified as an object of the type indicated by the key
	objects = {
		'treble clef': [],
		'bass clef': [],
		'crotchet rest': [],
		'time signature 4': [],
		'time signature 3': [],
		'quaver rest': [],
		'semibreve rest': [],
		'sharp': [],
		'natural': [],
		'flat': [],
		'note head': [],
		'minim note head': []
	}

	matchHighlightImage = img.copy()
	threshold = 0.7
	for template in templates:
		templateImg = cv2.imread(templatePath + template[1],0)	
		height = len(templateImg)
		width = len(templateImg[1])
	
		result = cv2.matchTemplate(img,templateImg,methods[1])
		
		musicalObjectPoints = []

		locations = np.where(result >= threshold)
		for point in zip(*locations[::-1]):
			cv2.rectangle(img,point,(point[0]+width,point[1]+height),255,-1)
			musicalObjectPoints.append(point)
		musicalObjectPoints = removeDuplicateMatches(40,musicalObjectPoints)
		for point in musicalObjectPoints:
			cv2.rectangle(matchHighlightImage,point,(point[0]+width,point[1]+height),0,1)
			pitch = staffData.getPitch(point[1]+height/2)
			objects[template[0]].append(omr_classes.MusicalObject(template[0],point,(width,height),pitch))
	cv2.imwrite('template_match_test.png',matchHighlightImage)
	return objects	

# Takes a list of MusicalObjects and removes the ones that cannot possibly be a rest
def filterSemibreveRests(rests):
	result = []
	for musicalObject in rests:
		print(musicalObject.point)
		print(musicalObject.pitch)
		if ((musicalObject.pitch == 'B4') or (musicalObject.pitch == 'C5') or (musicalObject.pitch == 'D5') or (musicalObject.pitch == 'D3') or (musicalObject.pitch == 'E3') or (musicalObject.pitch == 'F3')):
			result.append(musicalObject)
	print('Filtered result:')
	for rest in result:
		print(rest.point)
		print(rest.pitch)
	return result

# Takes a dictionary of musical objects and filters out the erroneous matches
def filterMusicalObjects(musicalObjects):
	musicalObjects['semibreve rest'] = filterSemibreveRests(musicalObjects['semibreve rest'])
	return musicalObjects

# Used in identifyNodes
def maxVerticalBlackCrossings(img,notehead,offsetX):
	xValues = []
	xValues.append(notehead.point[0] + offsetX - 8)
	xValues.append(notehead.point[0] + notehead.dimensions[0] + offsetX + 8)
	currentMaxBlackCrossings = 0
	for x in xValues:
		transitions = 0
		currentColour = 255
		for y in range(0,len(img)):
			if (img[y,x] != currentColour):
				currentColour = img[y,x]
				transitions = transitions + 1
		blackCrossings = transitions/2
		if (blackCrossings > currentMaxBlackCrossings):
			currentMaxBlackCrossings = blackCrossings
	return currentMaxBlackCrossings

# Given a binary image of sheet music with staff lines removed, a list of notehead objects and a Staff object, this function identifies the type of note each of the noteheads belong to
def identifyNotes(img,noteheads,staffData):
	# Invert the image for findContours
	img = 255 - img

	# Find contours
	contours,hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	# Remove contours that have dimensions that are too large to correspond to notes
	heightThreshold = 8*(staffData.lineThickness + staffData.lineSpacing)
	filteredContours = []
	for contour in contours:
		roi = cv2.boundingRect(contour)
		if (roi[3] < heightThreshold):
			filteredContours.append(contour)
	contours = filteredContours

	# contourMap is a list of tuples (contour,noteheads) where contour is a list of points representing a contour and noteheads is a list of noteheads whose centre lies within that contour
	contourMap = []
	
	# Identify, for each contour, which noteheads has a centre that lies within that contour
	for contour in contours:
		noteheadsInContour = []
		for notehead in noteheads:
			if (cv2.pointPolygonTest(contour,tuple(map(lambda (x,y): x+y/2,zip(notehead.point,notehead.dimensions))),False) == 1):
				noteheadsInContour.append(notehead)
		if (noteheadsInContour):
			contourMap.append((contour,noteheadsInContour))
	print(len(contours))
	print(len(contourMap))
	
	imgContours = np.zeros(img.shape,dtype=np.uint8)
	cv2.drawContours(imgContours,contours,-1,255)
	boundingBoxes = []
	for contour,noteheads in contourMap:
		boundingBoxes.append(cv2.boundingRect(contour))
	for x,y,w,h in boundingBoxes:
		cv2.rectangle(imgContours,(x,y),(x+w,y+h),127,1)

	cv2.imwrite('identifyNotesContoursTest.png',imgContours)
	
	# For each contour, identify each note that lies within it by looking at the number of vertical black crossings either side of the note head

	for contour,noteheads in contourMap:
		roi = cv2.boundingRect(contour)
		contourImg = np.empty((roi[3]+32,roi[2]+32),dtype=np.uint8)
		contourImg.fill(255)
		offsetX = - roi[0] + 16
		offsetY = - roi[1] + 16
		for point in contour:
			point[0][0] = point[0][0] + offsetX
			point[0][1] = point[0][1] + offsetY
		cv2.drawContours(contourImg,[contour],-1,0,-1)
		cv2.imshow('contour',contourImg)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		for notehead in noteheads:
			mvbc = maxVerticalBlackCrossings(contourImg,notehead,offsetX)
			if (mvbc == 0):
				notehead.name = 'crotchet'
			elif (mvbc == 1):
				notehead.name = 'quaver'
			elif (mvbc == 2):
				notehead.name = 'semiquaver'
			elif (mvbc == 3):
				notehead.name = 'demisemiquaver'
			else:
				notehead.name = 'unidentified'
			print(notehead.name)
		print	

def performRecognition(img,staffData):
	templateMatchingImage = img.copy()
	musicalObjects = matchTemplates(templateMatchingImage,staffData)
	musicalObjects = filterMusicalObjects(musicalObjects)
	identifyNotes(img,musicalObjects['note head'],staffData)
	return musicalObjects
