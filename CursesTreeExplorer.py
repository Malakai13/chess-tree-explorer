from TreeExplorer import TreeExplorer
from interface import implements
import curses
import sys


class CursesTreeExplorer(implements(TreeExplorer)):

	@staticmethod
	def no_game_given():
		print("Must give a pgn game file as a command line argument")
		sys.exit()

	@staticmethod
	def main_loop(board, fen_map):
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
