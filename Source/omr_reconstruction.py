import cv2
import omr_classes

def performReconstruction(musicalObjects,staffData,imageName):
	linearisedMusicalObjects = lineariseMusicalObjects(musicalObjects,staffData)
	print(linearisedMusicalObjects)
	trebleLinearised,bassLinearised = splitTrebleAndBass(linearisedMusicalObjects)
	trebleInMeasures = splitIntoMeasures(trebleLinearised)
	bassInMeasures = splitIntoMeasures(bassLinearised)
	keySignature = resolveKeySignature(musicalObjects)
	print('key signature: ' + str(keySignature))
	timeSignature = resolveTimeSignature(musicalObjects)
	outputLilypond(trebleInMeasures,bassInMeasures,keySignature,imageName)

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

def splitTrebleAndBass(linearisedMusicalObjects):
	trebleLinearised,bassLinearised = [],[]
	for musicalObject in linearisedMusicalObjects:
		if (musicalObject.name == 'bar line'):
			trebleLinearised.append(musicalObject)
			bassLinearised.append(musicalObject)
		elif (musicalObject.pitch in omr_classes.Staff.treblePitches):
			trebleLinearised.append(musicalObject)
		elif (musicalObject.pitch in omr_classes.Staff.bassPitches):
			bassLinearised.append(musicalObject)
		else:
			raise Exception('Error when splitting the treble and bass parts')
	return trebleLinearised,bassLinearised

def resolveKeySignature(musicalObjects):
	# First determine if the key signature is in sharps or flats
	keyType = None
	for accidental in musicalObjects['key signature']:
		if (accidental.accidental == 'sharp'):
			if ((keyType != None) and (keyType != 'sharp')):
				raise Exception('Key signature contains sharps and ' + str(keyType) + 's')
			else:
				keyType = 'sharp'
		elif (accidental.accidental == 'flat'):
			if ((keyType != None) and (keyType != 'flat')):
				raise Exception('Key signature contains flats and ' + str(keyType) + 's')
	
	accidentalPitches = []
	for accidental in musicalObjects['key signature']:
		accidentalPitches.append(accidental.pitch[0])
	# Remove duplicates
	accidentalPitches = list(set(accidentalPitches))
	
	print(accidentalPitches)
	# Determine key
	if (keyType == 'sharp'):
		if not(('F' in accidentalPitches)):
			return 'c'
		elif (not('C' in accidentalPitches)):
			return 'g'
		elif (not('G' in accidentalPitches)):
			return 'd'
		elif (not('D' in accidentalPitches)):
			return 'a'
		elif (not('A' in accidentalPitches)):
			return 'e'
		elif (not('E' in accidentalPitches)):
			return 'b'
		elif (not('B' in accidentalPitches)):
			return 'fis'
		else:
			return 'cis'
	elif (keyType == 'flat'):
		if not(('B' in accidentalPitches)):
			return 'c'
		elif (not('E' in accidentalPitches)):
			return 'f'
		elif (not('A' in accidentalPitches)):
			return 'bes'
		elif (not('D' in accidentalPitches)):
			return 'ees'
		elif (not('G' in accidentalPitches)):
			return 'aes'
		elif (not('C' in accidentalPitches)):
			return 'des'
		elif (not('F' in accidentalPitches)):
			return 'ges'
		else:
			return 'b'
	else:
		return 'c'

def resolveTimeSignature(musicalObjects):
	timeSignatureObjects = musicalObjects['time signature 8'] + musicalObjects['time signature 6'] + musicalObjects['time signature 4'] + musicalObjects['time signature 3']
	timeSignatureObjects.sort(key=lambda x: x.point[1])
	print(timeSignatureObjects[0].name)
	print(timeSignatureObjects[1].name)

def outputLilypond(trebleInMeasures,bassInMeasures,keySignature,imageName):
	outputFile = open(imageName + '.ly','w')
