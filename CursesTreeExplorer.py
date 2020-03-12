import curses
import sys


class CursesTreeExplorer:

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
			screen.addstr("Board:\n")

			j = 2
			for row in str(board).splitlines():
				screen.addstr(row + "\n")
				j += 1

			# TODO: have a way to enter your own moves?

			# Build choices here
			fen = board.fen()
			if fen in fen_map:
				top_i_choices = fen_map[fen]
			else:
				top_i_choices = []

			screen.addstr("Choices:\n")

			i = 0
			for move_count in top_i_choices:
				screen.addstr(str(i) + " - " + str(move_count) + "\n")
				i += 1

			try:
				board.peek()
				screen.addstr("b - Back 1 move\n")
			except IndexError:
				pass

			screen.addstr("q - Quit\n")
			screen.refresh()

			x = chr(screen.getch())

			if x == 'q':
				keep_playing = False
			elif x == 'b':
				try:
					board.pop()
				except IndexError:
					print("Unable to go back, no moves have been made")
			else:
				try:
					selected = int(x)
					if selected >= len(top_i_choices):
						continue
					move_count = top_i_choices[selected]
					move = move_count.move
					board.push(move)
				except ValueError:
					pass

		curses.endwin()
