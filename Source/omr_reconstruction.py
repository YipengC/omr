import cv2
import omr_classes

pitchMap = {
	'C6' : "c'''",
	'B5' : "b''",
	'A5' : "a''",
	'G5' : "g''",
	'F5' : "f''",
	'E5' : "e''",
	'D5' : "d''",
	'C5' : "c''",
	'B4' : "b'",
	'A4' : "a'",
	'G4' : "g'",
	'F4' : "f'",
	'E4' : "e'",
	'D4' : "d'",
	'C4' : "c'",
	'B3' : "b",
	'A3' : "a",
	'G3' : "g",
	'F3' : "f",
	'E3' : "e",
	'D3' : "d",
	'C3' : "c",
	'B2' : "b,",
	'A2' : "a,",
	'G2' : "g,",
	'F2' : "f,",
	'E2' : "e,",
	'D2' : "d,",
	'C1' : "c,,"
}

durationMap = {
	'semibreve' : '1',
	'semibreve rest' : '1',
	'minim' : '2',
	'minim rest' : '2',
	'crotchet' : '4',
	'crotchet rest' : '4',
	'quaver' : '8',
	'quaver rest' : '8',
	'semiquaver' : '16',
	'semiquaver rest' : '16',
	'demisemiquaver' : '32',
	'demisemiquaver rest' : '32'
}

xmlDurationMap = {
	'semibreve' : '32',
	'semibreve rest' : '16',
	'minim' : '16',
	'minim rest' : '16',
	'crotchet' : '8',
	'crotchet rest' : '8',
	'quaver' : '4',
	'quaver rest' : '4',
	'semiquaver' : '2',
	'semiquaver rest' : '2',
	'demisemiquaver' : '1',
	'demisemiquaver rest' : '1'
}

typeMap = {
	'semibreve' : 'note',
	'mimim' : 'note',
	'crotchet' : 'note',
	'quaver' : 'note',
	'semiquaver' : 'note',
	'demisemiquaver' : 'note',
	'semibreve rest' : 'rest',
	'minim rest' : 'rest',
	'crotchet rest' : 'rest',
	'quaver rest' : 'rest',
	'semiquaver rest' : 'rest',
	'demisemiquaver rest' : 'rest',
	'bar line' : 'bar line'
}

xmlTypeMap = {
	'semibreve' : 'whole',
	'mimim' : 'half',
	'crotchet' : 'quarter',
	'quaver' : 'eighth',
	'semiquaver' : '16th',
	'demisemiquaver' : '32nd',
	'semibreve rest' : 'whole',
	'minim rest' : 'half',
	'crotchet rest' : 'quarter',
	'quaver rest' : 'eighth',
	'semiquaver rest' : '16th',
	'demisemiquaver rest' : '32nd',
}

def performReconstruction(musicalObjects,staffData,imageName):
	trebleLinearised,bassLinearised = lineariseMusicalObjects(musicalObjects,staffData)
	trebleInMeasures = splitIntoMeasures(trebleLinearised)
	bassInMeasures = splitIntoMeasures(bassLinearised)
	keySignatureLilypond = resolveKeySignatureLilypond(musicalObjects)
	print('key signature Lilypond: ' + str(keySignatureLilypond))
	keySignatureMusicXML = resolveKeySignatureMusicXML(musicalObjects)
	print('key signature MusicXML: ' + str(keySignatureMusicXML))
	timeSignature = resolveTimeSignature(musicalObjects)
	print('trebleInMeasures: ' + str(trebleInMeasures))
	outputLilypond(trebleInMeasures,bassInMeasures,keySignatureLilypond,timeSignature,imageName)
	outputMusicXML(trebleInMeasures,bassInMeasures,keySignatureMusicXML,timeSignature,imageName)

def lineariseMusicalObjects(musicalObjects,staffData):
	trebleBoundaries = staffData.trebles
	for treble in trebleBoundaries:
		treble -= 3 * (staffData.lineSpacing + staffData.lineThickness)
	staffBoundaries = []
	topOfBassToBoundaryDistance = 7 * (staffData.lineSpacing + staffData.lineThickness)
	for topOfBass in staffData.basses:
		staffBoundaries.append(topOfBass + topOfBassToBoundaryDistance)

	numberOfBoundaries = len(staffBoundaries)
	print('staffBoundaries: ' + str(staffBoundaries))
	trebleObjectsLinearised = []
	bassObjectsLinearised = []
	for _ in range(0,numberOfBoundaries):
		trebleObjectsLinearised.append([])
		bassObjectsLinearised.append([])
	for musicalObjectList in musicalObjects.values():
		for musicalObject in musicalObjectList:
			for i in range(0,numberOfBoundaries):
				if (musicalObject.point[1] < staffBoundaries[i]):
					if (musicalObject.name == 'bar line'):
						trebleObjectsLinearised[i].append(musicalObject)
						bassObjectsLinearised[i].append(musicalObject)
					elif (musicalObject.point[1] < (trebleBoundaries[i] + staffBoundaries[i])/2):
						trebleObjectsLinearised[i].append(musicalObject)
					else:
						bassObjectsLinearised[i].append(musicalObject)
					break
	for musicalObjectList in trebleObjectsLinearised:
		musicalObjectList.sort(key=lambda x: x.point[0])
	for musicalObjectList in bassObjectsLinearised:
		musicalObjectList.sort(key=lambda x: x.point[0])
	"""
	for musicalObjectList in musicalObjectsLinearised:
		for musicalObject in musicalObjectList:
			print(musicalObject.name + str(musicalObject.point))
		print
	"""

	trebleObjectsLinearised = [y for x in trebleObjectsLinearised for y in x]
	bassObjectsLinearised = [y for x in bassObjectsLinearised for y in x]
	return (trebleObjectsLinearised,bassObjectsLinearised)

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
	return musicalObjectsInMeasures

def splitTrebleAndBass(linearisedMusicalObjects,staffData):
	trebleTops = staffData.trebles
	bassTops = staffData.basses
	trebleLinearised = []
	bassLinearised = []
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

def resolveKeySignatureLilypond(musicalObjects):
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

def resolveKeySignatureMusicXML(musicalObjects):
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
			return '0'
		elif (not('C' in accidentalPitches)):
			return '1'
		elif (not('G' in accidentalPitches)):
			return '2'
		elif (not('D' in accidentalPitches)):
			return '3'
		elif (not('A' in accidentalPitches)):
			return '4'
		elif (not('E' in accidentalPitches)):
			return '5'
		elif (not('B' in accidentalPitches)):
			return '6'
		else:
			return '7'
	elif (keyType == 'flat'):
		if not(('B' in accidentalPitches)):
			return '0'
		elif (not('E' in accidentalPitches)):
			return '-1'
		elif (not('A' in accidentalPitches)):
			return '-2'
		elif (not('D' in accidentalPitches)):
			return '-3'
		elif (not('G' in accidentalPitches)):
			return '-4'
		elif (not('C' in accidentalPitches)):
			return '-5'
		elif (not('F' in accidentalPitches)):
			return '-6'
		else:
			return '-7'
	else:
		return '0'

def resolveTimeSignature(musicalObjects):
	timeSignatureObjects = musicalObjects['time signature 8'] + musicalObjects['time signature 6'] + musicalObjects['time signature 4'] + musicalObjects['time signature 3']
	timeSignatureObjects.sort(key=lambda x: x.point[1])
	print(timeSignatureObjects[0].name)
	print(timeSignatureObjects[1].name)
	return (timeSignatureObjects[0].name[-1],timeSignatureObjects[1].name[-1])

def outputLilypond(trebleInMeasures,bassInMeasures,keySignature,timeSignature,imageName):
	outputFile = open(imageName + '.ly','w')
	outputFile.write('\\version "2.16.2"\n\n')
	outputFile.write("upper = {\n\\clef treble\n\\key " + keySignature + " \\major\n\\time " + timeSignature[0] + "/" + timeSignature[1] + "\n\n" + outputLilypondPart(trebleInMeasures) + "\n}\n\n")
	outputFile.write("lower = {\n\\clef bass\n\\key " + keySignature + " \\major\n\\time " + timeSignature[0] + "/" + timeSignature[1] + "\n\n" + outputLilypondPart(bassInMeasures) + "\n}\n\n")
	outputFile.write('\\score {\n\\new PianoStaff <<\n\\new Staff = "upper" \\upper\n\\new Staff = "lower" \\lower\n>>\n\\layout { }\n\\midi { }\n}')
	outputFile.close()

# Returns a string corresponding to the LilyPond output for partInMeasures
def outputLilypondPart(partInMeasures):
	outputString = ""
	for measure in partInMeasures:
		measureString = ""
		measureDuration = 0
		for musicalObject in measure:
			musicalObjectType = typeMap.get(musicalObject.name)
			if (musicalObjectType == 'note'):
				word = pitchMap[musicalObject.pitch]
				word += durationMap[musicalObject.name]
				if (musicalObject.accidental == 'sharp'):
					word = word[0] + 'is' + word[1:]
				elif (musicalObject.accidental == 'flat'):
					word = word[0] + 'es' + word[1:]
				outputString += " " + word
			elif (musicalObjectType == 'rest'):
				word = 'r' + durationMap[musicalObject.name]
				outputString += " " + word
	return outputString

def outputMusicXML(trebleInMeasures,bassInMeasures,keySignature,timeSignature,imageName):
	outputFile = open(imageName + '.xml','w')
	templateFile = open('../Resources/MusicXML/MusicXMLTemplate','r')
	output = templateFile.read()
	treblePart = ""
	measureNumber = 1
	for measure in trebleInMeasures:
		if (measure):
			treblePart += outputMeasure(measure,measureNumber,keySignature,timeSignature,'treble')
			measureNumber += 1
	bassPart = ""
	measureNumber = 1
	for measure in bassInMeasures:
		if (measure):
			bassPart += outputMeasure(measure,measureNumber,keySignature,timeSignature,'bass')
			measureNumber += 1
	output = output.replace('TREBLE',treblePart)
	output = output.replace('BASS',bassPart)
	outputFile.write(output)
	print(output)
	outputFile.close()

def outputMeasure(measure,number,keySignature,timeSignature,clef):
	measureXML = '<measure number="' + str(number) + '">'
	if (number == 1):
		if (clef == 'treble'):
			xmlClef = 'G2'
		elif (clef == 'bass'):
			xmlClef = 'F4'
		measureXML += '<attributes><divisions>8</divisions><key><fifths>' + keySignature + '</fifths></key><time><beats>' + timeSignature[0] + '</beats><beat-type>' + timeSignature[1] + '</beat-type></time><clef><sign>' + xmlClef[0] + '</sign><line>' + xmlClef[1] + '</line></clef></attributes>'
	for musicalObject in measure:
		musicalObjectType = typeMap.get(musicalObject.name)
		if (musicalObjectType == 'note'):
			alter = ""
			if (musicalObject.accidental == 'sharp'):
				alter = "1"
			elif (musicalObject.accidental == 'flat'):
				alter = "-1"
			measureXML += '<note><pitch><step>' + musicalObject.pitch[0] + '</step><alter>' + alter + '</alter><octave>' + musicalObject.pitch[1] + '</octave></pitch><duration>' + xmlDurationMap[musicalObject.name]  + '</duration><type>' + xmlTypeMap[musicalObject.name] + '</type></note>'
		elif (musicalObjectType == 'rest'):
			measureXML += '<note><rest/><duration>' + xmlDurationMap[musicalObject.name] + '</duration><type>' + xmlTypeMap[musicalObject.name] + '</type></note>'
	measureXML += '</measure>'
	return measureXML
