from interface import Interface


class TreeExplorer(Interface):

	# What to do when no game is given via the command line arguments
	@staticmethod
	def no_game_given():
		pass

	@staticmethod
	def main_loop(board, fen_map):
		pass