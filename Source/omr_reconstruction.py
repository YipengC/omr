

def performReconstruction(musicalObjects,staffData):
	lineariseMusicalObjects(musicalObjects,staffData)

def lineariseMusicalObjects(musicalObjects,staffData):
	staffBoundaries = []
	topOfBassToBoundaryDistance = 7 * (staffData.lineSpacing + staffData.lineThickness)
	for topOfBass in staffData.basses:
		staffBoundaries.append(topOfBass + topOfBassToBoundaryDistance)

	numberOfBoundaries = len(staffBoundaries)

	musicalObjectsLinearised = [[]]*numberOfBoundaries
	for musicalObjectList in musicalObjects.values():
		for musicalObject in musicalObjectList:
			for i in range(0,numberOfBoundaries):
				if (musicalObject.point[1] < staffBoundaries[i]):
					musicalObjectsLinearised[i].append(musicalObject)
					break
	for musicalObjectList in musicalObjectsLinearised:
		musicalObjectList.sort(key=lambda x: x.point[0])

	musicalObjectsLinearised = reduce(lambda x,y: x+y, musicalObjectsLinearised)
