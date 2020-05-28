# -*- coding: utf-8 -*-
from elements import *
from copy import deepcopy
import torch


class GameState:
	"""
	chessboard是一个棋盘，本质是一个字典
	键为一个表示位置的元组，值为空或者一个棋子对象
	在调用的时候可以通过chessboard[x, y]来调用位于(x, y)的棋子

	另外需注意python的拷贝问题，很多时候python只是传引用
	详见：https://www.cnblogs.com/wilber2013/p/4645353.html
	略见：https://www.runoob.com/w3cnote/python-understanding-dict-copy-shallow-or-deep.html

	坐标原点在左上角，x轴向右，y轴向下
	"""
	def __init__(self, chessboard=None, red_move=True, last_moves=None):
		self.red_move = red_move			# 当前是否红方回合
		if chessboard:
			self.chessboard = chessboard
		else:
			self.chessboard = dict()
			for i in range(9):
				for j in range(10):
					self.chessboard[i, j] = None
			self.chessboard[0, 6] = Bing((0, 6))
			self.chessboard[2, 6] = Bing((2, 6))
			self.chessboard[4, 6] = Bing((4, 6))
			self.chessboard[6, 6] = Bing((6, 6))
			self.chessboard[8, 6] = Bing((8, 6))
			self.chessboard[1, 7] = Pao((1, 7))
			self.chessboard[7, 7] = Pao((7, 7))
			self.chessboard[0, 9] = Che((0, 9))
			self.chessboard[8, 9] = Che((8, 9))
			self.chessboard[1, 9] = Ma((1, 9))
			self.chessboard[7, 9] = Ma((7, 9))
			self.chessboard[2, 9] = Xiang((2, 9))
			self.chessboard[6, 9] = Xiang((6, 9))
			self.chessboard[3, 9] = Shi((3, 9))
			self.chessboard[5, 9] = Shi((5, 9))
			self.chessboard[4, 9] = Shuai((4, 9))
			self.chessboard[0, 3] = Bing((0, 3), red=False)
			self.chessboard[2, 3] = Bing((2, 3), red=False)
			self.chessboard[4, 3] = Bing((4, 3), red=False)
			self.chessboard[6, 3] = Bing((6, 3), red=False)
			self.chessboard[8, 3] = Bing((8, 3), red=False)
			self.chessboard[1, 2] = Pao((1, 2), red=False)
			self.chessboard[7, 2] = Pao((7, 2), red=False)
			self.chessboard[0, 0] = Che((0, 0), red=False)
			self.chessboard[8, 0] = Che((8, 0), red=False)
			self.chessboard[1, 0] = Ma((1, 0), red=False)
			self.chessboard[7, 0] = Ma((7, 0), red=False)
			self.chessboard[2, 0] = Xiang((2, 0), red=False)
			self.chessboard[6, 0] = Xiang((6, 0), red=False)
			self.chessboard[3, 0] = Shi((3, 0), red=False)
			self.chessboard[5, 0] = Shi((5, 0), red=False)
			self.chessboard[4, 0] = Shuai((4, 0), red=False)
		self.index_map = {
			'bing': 0,
			'pao': 1,
			'che': 2,
			'ma': 3,
			'xiang': 4,
			'shi': 5,
			'shuai': 6
		}
		if last_moves:
			self.last_moves = last_moves
		else:
			self.last_moves = [
				((-1, -1), (-1, -1)),
				((-1, -1), (-1, -1)),
				((-1, -1), (-1, -1)),
				((-1, -1), (-1, -1)),
				((-1, -1), (-1, -1))
			]
		self.all_moves = []
		advisor_moves = [
			((3, 0), (4, 1)), ((4, 1), (3, 0)), ((5, 0), (4, 1)), ((4, 1), (5, 0)),
			((3, 2), (4, 1)), ((4, 1), (3, 2)), ((5, 2), (4, 1)), ((4, 1), (5, 2)),
			((3, 9), (4, 8)), ((4, 8), (3, 9)), ((5, 9), (4, 8)), ((4, 8), (5, 9)),
			((3, 7), (4, 8)), ((4, 8), (3, 7)), ((5, 7), (4, 8)), ((4, 8), (5, 7))
		]
		bishop_moves = [
			((2, 0), (0, 2)), ((0, 2), (2, 0)), ((2, 4), (0, 2)), ((0, 2), (2, 4)),
			((2, 0), (4, 2)), ((4, 2), (2, 0)), ((2, 4), (4, 2)), ((4, 2), (2, 4)),
			((6, 0), (4, 2)), ((4, 2), (6, 0)), ((6, 4), (4, 2)), ((4, 2), (6, 4)),
			((6, 0), (8, 2)), ((8, 2), (6, 0)), ((6, 4), (8, 2)), ((8, 2), (6, 4)),
			((2, 9), (0, 7)), ((0, 7), (2, 9)), ((2, 5), (0, 7)), ((0, 7), (2, 5)),
			((2, 9), (4, 7)), ((4, 7), (2, 9)), ((2, 5), (4, 7)), ((4, 7), (2, 5)),
			((6, 9), (4, 7)), ((4, 7), (6, 9)), ((6, 5), (4, 7)), ((4, 7), (6, 5)),
			((6, 9), (8, 7)), ((8, 7), (6, 9)), ((6, 5), (8, 7)), ((8, 7), (6, 5))
		]
		self.all_moves.extend(advisor_moves)
		self.all_moves.extend(bishop_moves)
		for i in range(9):
			for j in range(10):
				destinations = \
					[(k, j) for k in range(9)] + \
					[(i, k) for k in range(10)] + \
					[(i + m, j + n) for (m, n) in
						[(-2, -1), (-1, -2), (-2, 1), (1, -2), (2, -1), (-1, 2), (2, 1), (1, 2)]]
				for (x, y) in destinations:
					if (x, y) != (i, j) and x in range(9) and y in range(10):
						self.all_moves.append(((i, j), (x, y)))

	def copy(self):
		chessboard = deepcopy(self.chessboard)
		last_moves = deepcopy(self.last_moves)
		game = GameState(chessboard, self.red_move, last_moves)
		return game

	def state(self):
		state = torch.zeros(20, 9, 10)
		for piece in self.chessboard.values():
			if piece:
				x, y = piece.position
				index = self.index_map[piece.name]
				state[index, x, y] = 1 if piece.red else state[index + 7, x, y] = 1
		if self.red_move:
			state[14, :, :] = 1
		for i in range(5):
			move = self.last_moves[i]
			if move != ((-1, -1), (-1, -1)):
				(x_from, y_from), (x_to, y_to) = move
				state[15 + i, x_from, y_from] = -1
				state[15 + i, x_to, y_to] = 1
		return state

	@staticmethod
	def check_pos(position):
		"""
		判断坐标是否在棋盘内

		:param position:
		:return:
		"""
		x, y = position
		if x < 0 or y < 0 or x > 8 or y > 9:
			return False
		return True

	def get_legal_moves(self):
		"""
		Returns all possible moves.

		:return: ((x, y), (x_to, y_to))
		"""
		moves = []
		pieces = [piece for piece in self.chessboard.values() if piece and piece.red == self.red_move]
		for piece in pieces:
			for pos in piece.possible_moves(self.chessboard):
				move = (piece.position, pos)
				if self.can_move(move):
					moves.append(move)
		return moves

	def generate_successor(self, move):
		"""
		Returns the successor chessboard after the move.

		:param move:
		:return:
		"""
		# copy current chessboard
		game = self.copy()
		game.move(move)
		return game

	def check(self):
		"""
		判断是否将军

		:return:
		"""
		dangers = []		# 可能会将军的棋子
		king = None			# 己方帅
		for piece in self.chessboard.values():
			if piece:
				if piece.name == 'shuai' and piece.red == self.red_move:		# 找到己方帅
					king = piece
				if piece.red != self.red_move:								# 找到对方可以将军的棋子
					if piece.name in ['pao', 'ma', 'che', 'bing', 'shuai']:
						dangers.append(piece)
		if not king:
			return True
		for danger in dangers:												# 对每个棋子检查能否将军
			if danger.is_legal_move(king.position, self.chessboard):
				return True
		return False

	def can_move(self, move):
		"""
		是否能移动棋子
		可以返回True，否则返回False

		:param move:
		:return:
		"""
		start, end = move
		x, y = start
		x_to, y_to = end
		chessboard = deepcopy(self.chessboard)
		if not self.check_pos(start) or not self.check_pos(end):		# 位置越界
			return False
		if not chessboard[x, y]:										# 出发的位置不存在棋子
			return False
		if self.red_move != chessboard[x, y].red:						# 走棋颜色错误
			print('Not your turn')
			return False
		if not chessboard[x, y].is_legal_move(end, chessboard):			# 该棋子不能动
			print('Illegal move')
			return False
		chessboard[x, y].set_position(end)
		chessboard[x_to, y_to] = chessboard[x, y]
		chessboard[x, y] = None
		game = GameState(chessboard, self.red_move)
		if game.check():												# 检查是否送将
			print('不能送将')												# Todo: 把不能送将显示出来
			return False
		return True

	def move(self, move):
		flag = False
		self.last_moves.pop(0)
		self.last_moves.append(move)
		(x, y), (x_to, y_to) = move
		if self.chessboard[x_to, y_to]:
			flag = True
		self.chessboard[x, y].set_position((x_to, y_to))
		self.chessboard[x_to, y_to] = self.chessboard[x, y]
		self.chessboard[x, y] = None
		self.red_move = not self.red_move
		return flag

	def checkmate(self):
		"""
		判断是否将死

		:return:
		"""
		pieces = []
		for i in self.chessboard.values():							# 找到所有己方棋子
			if i and i.red == self.red_move:
				pieces.append(i)
		for piece in pieces:										# 找到目前能做的所有事
			for pos in piece.possible_moves(self.chessboard):
				chess = deepcopy(piece)
				chessboard = deepcopy(self.chessboard)
				x, y = chess.position
				x_to, y_to = pos
				chess.set_position(pos)
				chessboard[x_to, y_to] = chess
				chessboard[x, y] = None
				game = GameState(chessboard, self.red_move)
				if not game.check():								# 依次检查能否摆脱将军
					return False
		return True
