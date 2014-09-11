from board import Board

class Player:
	def __init__(self, name):
		self.personal_board = Board()
		self.personal_board.place_troops()
		self.enemy_board = Board()


	def play(self, attack ,dice_roll):
		pass

	def recieve_attack(self):
		pass

