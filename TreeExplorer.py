import chess.pgn
import curses
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
		screen = curses.initscr()

		screen.clear()
		screen.addstr(0, 0, "Board:")

		j = 2
		for row in str(board).splitlines():
			screen.addstr(j, 4, row)
			j += 1

		# TODO: have a way to enter your own moves?

		# Build choices here
		fen = board.fen()
		if fen in fen_map:
			top_i_choices = fen_map[fen]
		else:
			top_i_choices = []

		spacer = 2
		screen.addstr(j + spacer, 0, "Choices:")
		spacer += 2

		i = 0
		for move_count in top_i_choices:
			screen.addstr(i + j + spacer, 4, str(i) + "- " + str(move_count))
			i += 1

		spacer += 1
		screen.addstr(i + j + spacer, 4, "b - Back 1 move")
		spacer += 1
		screen.addstr(i + j + spacer, 4, "q - Quit")
		screen.refresh()

		x = chr(screen.getch())

		if x == 'q':
			keep_playing = False
		elif x == 'b':
			if len(board.stack) > 0:
				board.pop()
			else:
				print("Unable to go back, no moves have been made")
		else:
			move_count = top_i_choices[int(x)]
			move = move_count.move
			board.push(move)

	curses.endwin()


if __name__ == '__main__':
	main()
