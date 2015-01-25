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
		currentPoints = []
		nextPoints = []
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
		('treble clef','treble_clef_template.png'),
		('bass clef','bass_clef_template.png'),
		('crotchet rest','crotchet_rest_template.png'),
		('time signature 4','time_signature_4_template.png'),
		('time signature 3','time_signature_3_template.png'),
		('quaver rest','quaver_rest_template.png'),
		('semibreve rest','semibreve_rest_template.png'),
		('sharp','sharp_template.png'),
		('natural','natural_template.png'),
		('flat','flat_template.png'),
	#	('note head','note_head_template.png'),
		('note head','note_head_2_template.png'),
		('minim note head','minim_note_head_template.png')
	)

	methods = [cv2.TM_CCOEFF,cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR,cv2.TM_CCORR_NORMED,cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]

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

def performRecognition(img,staffData):
	musicalObjects = matchTemplates(img,staffData)
	musicalObjects = filterMusicalObjects(musicalObjects)
