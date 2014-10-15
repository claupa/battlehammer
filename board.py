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
		  0 : Army(5, 'Archers', (1,5)),} 
		  #0 : Army(0, 'Land', (1,1))}
		self.repetitions = 50

	def place_troops(self, index = 0):
		# Place troops, receives an index param. It represents the next army to place.
		# The list can be found in self.troops field.
		## If this is the last army, then check that it can be placed with the current config
		## if not then return False and erase the position.
		last = index == len(self.troops)-1
		## If this is not the last troop, then try to place the next troops.
		## Once they are placed, try to fit my army in. If not repeat procedure until it works.
		not_posible = True
		while not_posible:
			current_board =self.save_state() if last else self.place_troops(index+1)				
			not_posible, new_board = self.try_place_troop(index, current_board)
			if not not_posible: return new_board

			
	def save_state(self, board = []):
		## save  state creates a new copy of the board as it is now.
		copy_board = board if board else self.board
		current_board = [[elem for elem in row] for row in copy_board]
		return current_board

	def place_troop(self,index):
		## Place the first troop on the board
		## Generate a random position and an orientation for the army
		army_type = self.troops[index]		
		orientation = 0 if random() <= 0.5 else 1	
		point = self.generate_random_position(army_type, orientation)
		posible = self.check_position(point,army_type)
		board = self.save_state()
		if posible:
			return self.position_setting(point, army_type, board)
		else: print "-----------------FAILED PLACE TROOP---------------"

	def try_place_troop(self, index, current_board):
		## Try to place the troop number index on the board given the current board setted with 
		## other troops.
		counts = self.repetitions
		army_type = self.troops[index]					
		while counts >=0:
			## Try to place the troops at a random position with a random orientation.
			orientation = 0 if random() <= 0.5 else 1	
			position = self.generate_random_position(army_type, orientation)
			posible = self.check_position(position,army_type, current_board)
			## If it is posible to place the troop at position then place the troop
			## on the board and return the new board
			if posible:
				board = self.save_state(current_board)
				return False, self.position_setting(position, army_type, board)
			counts -= 1
		## Otherwise return the same board with the not_posible setted to true
		return True, current_board

	def generate_random_position(self, army_type, orientation):
		if orientation: army_type.swap_structure()
		width, height = army_type.structure
		x = min (int(random() * self.height) , self.height - height)
		y = min (int(random() * self.width), self.width - width)
		return (x,y)

	def check_position(self, start_position, army_type, check_board = None):
		width, height = army_type.structure
		x_start, y_start = start_position
		board = check_board if check_board else self.board
		if x_start + height >= self.height or y_start + width >=self.width:
			return False 
		for i in range(x_start, x_start + height):
			for j in range(y_start, y_start + width):
				if board[i][j]:
					return False
		return True

	def position_setting(self, start_position, army_type, board= None):
		width, height = army_type.structure 
		x_start, y_start = start_position
		board = board if board else self.board
		for i in range(x_start, x_start + height):
			for j in range(y_start,y_start + width):
				board[i][j] = army_type.number_id
		return board

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

	def load_board(self, board_to_copy = None):
		if board_to_copy:
			self.board = self.save_state(board_to_copy)
		else:
			self.board = self.place_troops(0)

	def check_board(self):
		pass

class Army:
	""" An army has an ID number identifying what type of army it has.
	It also has a formation 2x3 or 1x5 and an orientation which is used
	to determine the swap."""
	def __init__(self, number_id, name, structure):
		self.number_id = number_id
		self.name = name
		self.structure = structure
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

	def swap_structure(self):
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

board = Board()
board.load_board()
for r in board.board:
	print r