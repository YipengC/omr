import cv2

def performReconstruction(musicalObjects,staffData,imageName):
	linearisedMusicalObjects = lineariseMusicalObjects(musicalObjects,staffData)
	musicalObjectsInMeasures = splitIntoMeasures(linearisedMusicalObjects)
	outputLilypond(musicalObjectsInMeasures,imageName)

def lineariseMusicalObjects(musicalObjects,staffData):
	staffBoundaries = []
	topOfBassToBoundaryDistance = 7 * (staffData.lineSpacing + staffData.lineThickness)
	for topOfBass in staffData.basses:
		staffBoundaries.append(topOfBass + topOfBassToBoundaryDistance)

	numberOfBoundaries = len(staffBoundaries)
	print('staffBoundaries: ' + str(staffBoundaries))
	musicalObjectsLinearised = []
	for _ in range(0,numberOfBoundaries):
		musicalObjectsLinearised.append([])
	print(musicalObjectsLinearised)
	for musicalObjectList in musicalObjects.values():
		for musicalObject in musicalObjectList:
			for i in range(0,numberOfBoundaries):
				if (musicalObject.point[1] < staffBoundaries[i]):
					musicalObjectsLinearised[i].append(musicalObject)
					break
	for musicalObjectList in musicalObjectsLinearised:
		musicalObjectList.sort(key=lambda x: x.point[0])
	"""
	for musicalObjectList in musicalObjectsLinearised:
		for musicalObject in musicalObjectList:
			print(musicalObject.name + str(musicalObject.point))
		print
	"""

	musicalObjectsLinearised = [y for x in musicalObjectsLinearised for y in x]
	return musicalObjectsLinearised

def splitIntoMeasures(linearisedMusicalObjects):
	musicalObjectsInMeasures = []
	currentMeasureObjects = []
	for musicalObject in linearisedMusicalObjects:
		if (musicalObject.name == 'bar line'):
			musicalObjectsInMeasures.append(currentMeasureObjects)
			currentMeasureObjects = []
		else:
			currentMeasureObjects.append(musicalObject)
	
	for measure in musicalObjectsInMeasures:
		for musicalObject in measure:
			print(musicalObject.name + str(musicalObject.point))
		print

def outputLilypond(musicalObjectsInMeasures,imageName):
	outputFile = open(imageName + '.ly','w')
