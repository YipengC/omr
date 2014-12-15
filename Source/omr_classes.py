class Staff:
	def __init__(self,lineSpacing=0,lineThickness=0,tops=[]):
		self.lineSpacing = lineSpacing
		self.lineThickness = lineThickness
		self.tops = tops

class Sheet:
	def __init__(self,staff=None,width=0,height=0):
		self.staff = staff
		self.width = width
		self.height = height
