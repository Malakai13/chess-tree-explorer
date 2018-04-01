import chess.pgn
import sys
from chess import Board
from CursesTreeExplorer import CursesTreeExplorer
from ChessGameParser import ChessGameParser


def main():
	explorer = CursesTreeExplorer()

	if len(sys.argv) < 2:
		filename = explorer.no_game_given()
	else:
		filename = sys.argv[1]

	pgn = open(filename)
	parser = ChessGameParser()

	try:
		while True:
			game = chess.pgn.read_game(pgn)
			parser.parse_game(game)
	except:
		pass

	fen_map = parser.transform_to_top_i_map(3)
	explorer.main_loop(Board(), fen_map)


if __name__ == '__main__':
	main()
