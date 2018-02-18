class MoveCount:
	def __init__(self, move):
		self.move = move
		self.count = 1

		self.white_wins = 0
		self.black_wins = 0

	def __init__(self, move, game_results):
		self.move = move
		self.count = 1

		self.black_wins = 0
		self.white_wins = 0
		self.increment_by_game_results(game_results)

	def increment_count(self):
		self.count += 1

	def increment_white(self):
		self.white_wins += 1

	def increment_black(self):
		self.black_wins += 1

	def increment_by_game_results(self, game_results):
		if game_results == "1-0":
			self.increment_white()
		elif game_results == "0-1":
			self.increment_black()
			
	def win_str(self):
		total = self.white_wins + self.black_wins

		white_win_percentage = 100.0 * self.white_wins / total
		black_win_percentage = 100.0 * self.black_wins / total
		return "{0:.2f}".format(white_win_percentage) + "|" + "{0:.2f}".format(black_win_percentage)

	def __str__(self):
		return str(self.move) + ":" + str(self.count) + " " + self.win_str()

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.move == other.move
		else:
			return False
