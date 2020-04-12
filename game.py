# -*- coding: utf-8 -*-
from elements import *
from copy import deepcopy


class Game:
	"""
	chessboard是一个棋盘，本质是一个字典
	键为一个表示位置的元组，值为空或者一个棋子对象
	在调用的时候可以通过chessboard[x, y]来调用位于(x, y)的棋子

	坐标原点在左上角，x轴向右，y轴向下
	"""
	def __init__(self, chessboard=None):
		self.red_move = True		# 当前是否红方回合
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
		pieces = [piece for piece in self.chessboard.values() if piece]
		for piece in pieces:
			for pos in piece.possible_move(self.chessboard):
				move = (piece.position, pos)
				moves.append(move)
		return moves

	def generate_successor(self, move):
		"""
		Returns the successor chessboard after the move.

		:param move:
		:return:
		"""
		# copy current chessboard
		chessboard = deepcopy(self.chessboard)

		start, end = move
		x, y = start
		x_to, y_to = end
		chessboard[x, y].position = (x_to, y_to)
		chessboard[x_to, y_to] = chessboard[x, y]
		chessboard[x, y] = None

		game = Game(chessboard)
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
				if piece.name == '帅' and piece.red == self.red_move:		# 找到己方帅
					king = piece
				if piece.red != self.red_move:								# 找到对方可以将军的棋子
					if piece.name == '炮' or piece.name == '马' or piece.name == '车' or piece.name == '兵':
						dangers.append(piece)
		for danger in dangers:												# 对每个棋子检查能否将军
			if danger.is_legal_move(king.position, self.chessboard):
				return True
		return False

	def move(self, start_position, end_position):
		"""
		移动棋子
		移动成功返回True，否则返回False

		:param start_position:
		:param end_position:
		:return:
		"""
		x, y = start_position
		if not self.check_pos(start_position) or not self.check_pos(end_position):		# 位置越界
			return False
		if not self.chessboard[x, y]:													# 出发的位置不存在棋子
			return False
		if self.red_move != self.chessboard[x, y].red:									# 走棋颜色错误
			print('Not your turn')
			return False
		if not self.chessboard[x, y].is_legal_move(end_position, self.chessboard):		# 该棋子不能动
			print('Illegal move')
			return False
		x_to, y_to = end_position
		temp = self.chessboard[x_to, y_to]
		self.chessboard[x, y].set_position(end_position)
		self.chessboard[x_to, y_to] = self.chessboard[x, y]
		self.chessboard[x, y] = None
		if self.check():																# 检查是否送将，若是则取消移动
			self.chessboard[x_to, y_to].set_position(start_position)
			self.chessboard[x, y] = self.chessboard[x_to, y_to]
			self.chessboard[x_to, y_to] = temp
			print('不能送将')															# Todo: 把不能送将显示出来
			return False
		self.red_move = not self.red_move
		return True

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
			for move in piece.possible_move(self.chessboard):
				x, y = piece.position
				x_to, y_to = move
				temp = self.chessboard[x_to, y_to]
				piece.set_position(move)
				self.chessboard[x_to, y_to] = piece
				self.chessboard[x, y] = None
				if not self.check():								# 依次检查能否摆脱将军
					piece.set_position((x, y))
					self.chessboard[x, y] = piece
					self.chessboard[x_to, y_to] = temp
					return False
				else:
					piece.set_position((x, y))
					self.chessboard[x, y] = piece
					self.chessboard[x_to, y_to] = temp
		return True
