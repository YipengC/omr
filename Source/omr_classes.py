import bisect

class MusicalObject:
	def __init__(self,name,point=None,dimensions=None,pitch=None):
		self.name = name
		self.point = point
		self.pitch = pitch
		self.dimensions = dimensions

class Staff:
	
	treblePitches = ('C6','B5','A5','G5','F5','E5','D5','C5','B4','A4','G4','F4','E4','D4','C4','B3','A3')
	bassPitches = ('E4','D4','C4','B3','A3','G3','F3','E3','D3','C3','B2','A2','G2','F2','E2','D2','C1')

	def __init__(self,lineSpacing=0,lineThickness=0,tops=[]):
		self.lineSpacing = lineSpacing
		self.lineThickness = lineThickness
		self.tops = tops
		self.trebles = []
		self.basses = []
		self.lines = {}
		self.initLines()

	# Assumes that the first value in top corresponds to a treble staff and the rest alternate between bass and treble

	def initLines(self):
		treble = True
		for top in self.tops:
			if (treble):
				self.trebles.append(top)
				treble = False
			else:
				self.basses.append(top)
				treble = True
		
		treble = True
		pitches = self.treblePitches
		lineDifference = self.lineSpacing + self.lineThickness
		for top in self.tops:
			currentY = top - 2*(lineDifference) + self.lineThickness/2
			for pitch in pitches:
				self.lines[currentY] = pitch
				currentY = currentY + lineDifference
			treble = (not(treble))
			if (treble):
				pitches = self.treblePitches
			else:
				pitches = self.bassPitches
		print(self.trebles)
		print(self.basses)
		print(self.lines)

	def getPitch(self,y):
		yValues = self.lines.keys()
		sorted(yValues)
		key = bisect.bisect_left(yValues,y)
		return self.lines[yValues[key]]

class Sheet:
	def __init__(self,staff=None,width=0,height=0):
		self.staff = staff
		self.width = width
		self.height = height
