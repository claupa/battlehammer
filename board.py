from random import random
from time import sleep

class Board:
	def __init__(self, height = 8, width = 8):
		self.height = height
		self.width = width
		self.board = [[0 for i in range(height)] for j in range(width)]
		self.troops = {
		  1 : Army(1, 'Orcs', (1,5)),
		  2 : Army(2, 'Pikemen', (2,3)), 
		  3 : Army(3, 'Knights', (2,2)),
		  4 : Army(4, 'Dragons', (1,3)),
		  5 : Army(5, 'Archers', (1,5)), 
		  0 : Army(0, 'Land', (1,1))}

	def place_troops(self, index = 0):
		last = index == len(self.troops)
		if last:
			failed, position, o = self.generate_start_position(self.troops[index])	
			if not failed:
				self.position_setting(position, army, o)
			return not failed
		else:
			failed, position, o = self.generate_start_position(self.troops[index])
			if failed: return False	
			if not failed:
				new_board = self.position_setting(position, army_type, o)
				succeded = self.place_troops(index + 1, new_board)


		for army in self.mapping.values():
			if not army.number_id: continue			
			x, y, o = self.generate_start_position(army)
			
	def save_state(self):
		current_board = [[elem for elem in row] for row in self.board]
		return current_board

	def generate_start_position(self,army_type, count = 0):
		if count == 100:
			return (False, (0,0), 0)
		orientation = 0 if random() <= 0.5 else 1		
		x,y = self.generate_random_position(army_type,orientation)
		if self.check_position((x,y),army_type):
			return (True, (x,y) , orientation)
		else:
			orientation = 0 if orientation else 1
			x,y = self.generate_random_position(army_type, orientation)
			if self.check_position((x,y),army_type):
				return (True, (x,y) , orientation)

			else:
				count += 1 
				return self.generate_start_position(army_type, count++)

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

	def load_board(self):
		print "Not implemented."
		pass

	def check_board(self):
		print "Not implemented."
		pass

class Army:
	def __init__(self, number_id, name, structure,orientation = 0):
		self.number_id = number_id
		self.name = name
		self.structure = structure
		self.orientation = orientation
		self.soldiers = [] 
		self.position =(0,0)

	def create_soldiers(self,position):
		width, height = self.structure
		x, y = position
		self.soldiers = [ [Soldier(self.number_id) for i in range(height)] for j in range(width)]
		for i in range(height):
			for j in range(width):
				self.soldiers[i][j].set_position((x + i, y+j))

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

	def destroy_soldier(self, position):
		x, y = position
		for row in self.soldiers:
			for soldier in row:
				if soldier.get_position() == position  and not soldier.hitted():
					soldier.got_hit()
					print "attack succeded"
					return True
		print "attack failed"
		return False
		

	def defend_soldier(self, position, direction):
		for row in self.soldiers:
			for soldier in row:
				if soldier.get_position() == position and not soldier.hitted():
					soldier.move(direction)
					print "defense succeded"
					return True
		print "defense failed"
		return False


	def is_army_destroyed(self):
		for row in self.soldiers:
			for soldier in row:
				if not soldier.hitted():
					return False
		return True 


class Soldier:
	def __init__(self, number_id, position = (0,0)):
		self.number_id = number_id
		self.__position = position
		self.directions = {'up':(-1,0), 'down':(1,0) , 'left': (0,-1), 'right':(0,1)}
		self.__discovered = False

	def set_position(self, position):
		self.__position = position

	def get_position(self):
		return self.__position

	def move(self, direction):
		if discovered: 
			print 'Unable to move piece.'
			return

		x, y = self.__position
		i,j = self.directions[direction]
		self.__position = (x+i, y+j)

	def got_hit(self):
		self.__discovered = True

	def hitted(self):
		return self.__discovered

	