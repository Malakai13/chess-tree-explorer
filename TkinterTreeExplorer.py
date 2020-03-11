from tkinter import Tk
from tkinter.filedialog import askopenfilename

import TreeExplorer
from interface import implements


class TkinterTreeExplorer(implements(TreeExplorer)):

	@staticmethod
	def no_game_given():
		Tk().withdraw()
		filename = askopenfilename()
		return filename

	@staticmethod
	def mainloop(board, fen_map):
		return
