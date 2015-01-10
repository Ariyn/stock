# _*_ coding: utf-8 _*_
# map.py

# map tile needs these things
# x,y,z coordinate
# owner
# special
class Tile:
	def __init__(self, x,y,z, seType=None):
		self.x, self.y, self.z = x, y, z
		self.se = None

		if seType:
			self.se = SpecialEffect(seType)


# SpecialEffect needs these things
# type
# total amount
# remain amount
# mine class
class SpecialEffect:
	def __init__(self, type):
		self.type = type
		self.industry = None

class Resource:
	def __init__(self, type):
		self.type = type