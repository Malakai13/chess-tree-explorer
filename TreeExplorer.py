import chess.pgn
import sys
from chess import Board

from MoveCount import MoveCount


class TreeExplorer:

	def __init__(self):
		self.fen_to_move_counts = {}

	def parse_game(self, game):
		board = game.board()

		for move in game.main_line():
			fen = board.fen()
			game_result = game.headers["Result"]

			if fen in self.fen_to_move_counts:
				move_count_map = self.fen_to_move_counts[fen]
				if move in move_count_map:
					move_count = move_count_map[move]
					move_count.increment_count()
					move_count.increment_by_game_results(game_result)
				else:
					move_count = MoveCount(move, game_result)
					move_count_map[move] = move_count
			else:
				move_count = MoveCount(move, game_result)
				move_count_map = {move: move_count}
				self.fen_to_move_counts[fen] = move_count_map

			board.push(move)

	def transform_to_top_i_map(self, i):
		results = {}

		for fen in self.fen_to_move_counts:
			move_counts = self.fen_to_move_counts[fen]
			all_move_counts = []

			for move in move_counts:
				move_count = move_counts[move]
				all_move_counts.append(move_count)

			# Sort & limit to top i
			sorted_move_counts = sorted(all_move_counts, key=lambda mc: mc.count, reverse=True)
			top_i = sorted_move_counts[:i]
			results[fen] = top_i

		return results


def main():
	if len(sys.argv) < 2:
		print('Must pass a .pgn file to parse')
		quit()

	filename = sys.argv[1]
	pgn = open(filename)

	explorer = TreeExplorer()

	try:
		while True:
			game = chess.pgn.read_game(pgn)
			explorer.parse_game(game)
	except:
		print('Done parsing file')

	fen_map = explorer.transform_to_top_i_map(3)

	# New game
	board = Board()

	keep_playing = True

	while keep_playing:
		print(board)

		fen = board.fen()
		if fen in fen_map:
			top_i_choices = fen_map[fen]
		else:
			top_i_choices = []

		choices = "back: back 1 move\nq: quit\n"

		i = 0
		for move_count in top_i_choices:
			choices += str(i) + ": " + str(move_count) + "\n"
			i += 1

		print("\n" + choices + "\n")

		choice = None
		while choice is None:
			x = raw_input("What is your choice?")
			if x == "back" or x == "q":
				choice = x
				continue
			else:
				try:
					choice = int(x)
					if choice >= len(top_i_choices) or choice < 0:
						choice = None
						print("That is not a valid choice")
				except:
					print("That is not a valid choice")

		if choice == "back":
			if len(board.stack) > 0:
				board.pop()
			else:
				print("Unable to go back, no moves have been made")
			continue

		if choice == "q":
			sys.exit()

		# TODO: have a way to enter your own moves?

		move_count = top_i_choices[choice]
		move = move_count.move
		board.push(move)


if __name__ == '__main__':
	main()

