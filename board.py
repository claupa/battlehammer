import random
from random import random
from time import sleep

class Board:
	def __init__(self, height = 8, width = 8):
		self.height = height
		self.width = width
		self.board = [[0 for i in range(height)] for j in range(width)]
		self.mapping = {
		  1 : Army(1, 'Orcs', (1,5)),
		  2 : Army(2, 'Pikemen', (2,3)), 
		  3 : Army(3, 'Knights', (2,2)),
		  4 : Army(4, 'Dragons', (1,3)),
		  5 : Army(5, 'Archers', (1,5)), 
		  0 : Army(0, 'Land', (1,1))}

	def place_troops(self):
		for army in self.mapping.values():
			if not army.number_id: continue			
			x, y, o = self.generate_start_position(army)
			self.position_setting((x,y), army, o)

	def generate_start_position(self,army_type):
		orientation = 0 if random() <= 0.5 else 1		
		x,y = self.generate_random_position(army_type,orientation)
		if self.check_position((x,y),army_type):
			return (x,y, orientation)
		else:
			orientation = 0 if orientation else 1
			x,y = self.generate_random_position(army_type, orientation)
			if self.check_position((x,y),army_type):
				return (x,y , orientation)
			else: return self.generate_start_position(army_type)

	def generate_random_position(self, army_type, orientation):
		if orientation: army_type.swap_structure(orientation)
		width, height = army_type.structure
		x = min (int(random() * self.height) , self.height - height)
		y = min (int(random() * self.width), self.width - width)
		return (x,y)

	def check_position(self, start_position, army_type):
		width, height = army_type.structure
		x_start, y_start = start_position
		if x_start + height >= self.height or y_start + width >=self.width:
			return False 
		for i in range(x_start, x_start + height):
			for j in range(y_start, y_start + width):
				if self.board[i][j]:
					return False
		return True

	def position_setting(self, start_position, army_type, orientation):
		width, height = army_type.structure 
		x_start, y_start = start_position
		for i in range(x_start, x_start + height):
			for j in range(y_start,y_start + width):
				self.board[i][j] = army_type.number_id

	def attack_position(self, position_setting):
		x, y = position_setting
		number_id = self.board[x][y]
		if number_id < 0:
			return '%s hited' % (self.mapping[number_id*(-1)].name)  
		self.board[x][y] = -1 * number_id
		return self.mapping[number_id].name

	def defend_position(self, position_setting, direction):
		x, y = position_setting
		i, j = direction 
		if not self.board[x][y] or self.board[x+i][y+j]:
			return "Not a valid move."
		self.board[x+i][y+j] = self.board[x][y]
		self.board[x][y] = 0
		return "Succesful move."

class Army:
	def __init__(self, number_id, name, structure,orientation = 0):
		self.number_id = number_id
		self.name = name
		self.structure = structure
		self.orientation = orientation 

	def get_number(self):
		return self.width * self.height

	def swap_structure(self,orientation):
		if orientation == self.orientation:
			return
		self.orientation = orientation
		width, height = self.structure
		dim    = width
		width  = height
		height = dim
		self.structure = (width,height)


class Player:
	def __init__(self, name = "computer",board = None):
		self.name = name
		if not board:
			self.board = Board()
		else: self.board = board


b = Board()
b.place_troops()
