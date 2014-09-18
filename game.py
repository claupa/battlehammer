from player import Player
from time import sleep

class Game:
	def __init__(self):
		self.player = Player()
		self.enemy_player = Player()
		self.player_board = []
		self.enemy_player_board = []
		self.height = 8
		self.width = 8

	def start_game(self):
		print "Game Starting ..."
		sleep(2)

		player_turn = True
		no_victory = True

		while no_victory:
			player, enemy_player = change_turn()
			print "It's %s turn. Rolling dice ..." % (player.name)
			sleep(1)

			action_points = self.roll_dice()	
			print "%s obtained %s action points." % (player.name , action_points)
			sleep(1)

			attack = current_player.decide_action(action_points)
			print "%s chose to %s." %( player.name, "attack" if attack else "defend")

			if attack: 
				cheat = self.attack(action_points)
				if cheat : pass

			else: self.defend(action_points)		
			player_turn = False
			no_victory = self.no_one_wins(current_enemy_player)
		
			
	def attack(self, action_points):
		for i in range(action_points):
			attack_action = self.player.play_attack_action()
			print "Action %s: Attack position %s." % (self.player, str(attack_action + 1))

			feedback = self.enemy_player.recieve_attack(attack_action)
			print "Action Result: %s hited %s." % (player.name, feedback)
			
			valid = self.check_update_attack(attack_action, attack_result)
			if not valid: 
				print "%s is a cheater and looses immediately."
				return valid
			
			self.player.recieve_info_attack(attack_action, attack_result)
			sleep(2)
		return False

	def check_update_attack(self,attack_action, attack_result):
		x,y = attack_action
		number_id = attack_result.number_id
		if self.enemy_player_board[x][y] != number_id:
			return False
		self.enemy_player_board[x][y] *=  -1
		return True 


	def check_update_defense(self, defend_position, direction):
		x, y = defend_position
		i,j = direction
		if self.player_board[x][y] > 0 and self.player_board[x+i][y+j]==0:
			self.player_board[x+i][y+j] = self.player_board[x][y]
			self.player_board[x][y] = 0
			return True
		return False

	def roll_dice(self):
		dice = random()
		number = int(6*dice)
		return 0 if number ==0 else 1 if number == 2 or number == 3 else 2 if number == 4 or number == 5 else 3 

	def defend(self, action_points):
		print "%s is defending ..." % (self.player)
		self.enemy_player.inform_defense_choice(action_points)
		for i in range(action_points):
			defend_position, direction = self.player.defend()
			valid = self.check_update_defense(defend_position, direction)
			if not valid:
				print "Invalid defense move. Action point wasted."
		return False

	def no_one_wins(self):
		for i in range(self.height):
			for j in range(self.width):
				if self.enemy_player_board[i][j] > 0:
					return True
		return False

	def change_turn(self):
		print "Changing turn."
		aux_player = self.player
		self.player = self.enemy_player
		self.enemy_player = aux_player

		aux_board = self.player_board
		self.player_board = self.enemy_player_board
		self.enemy_player_board = aux_board
		return self.player, self.enemy_player


print 'hello battle hammer'
