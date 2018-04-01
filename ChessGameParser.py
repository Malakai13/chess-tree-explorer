from MoveCount import MoveCount


class ChessGameParser:

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
