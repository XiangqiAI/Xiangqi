# -*- coding: utf-8 -*-
from abc import abstractmethod


class Chess:
	def __init__(self, position, red=True):
		self.position = position
		self.red = red
		self.name = ''
		self.pos_list = []		# 将来的可能目标位置，由各派生类确定

	def __str__(self):
		if self.red:
			color = 'R'
		else:
			color = 'B'
		return '{}{} at {}'.format(color, self.name, self.position)

	@abstractmethod
	def get_pos_list(self):
		"""
		返回所有可能的后续坐标
		:return:
		"""
		pass

	@abstractmethod
	def picture(self):
		"""
		返回该棋子的图片

		:return:
		"""
		pass

	@abstractmethod
	def is_legal_action(self, dx, dy, end_position=None):
		"""
		判断此行为是否合法

		:param dx: x方向的移动距离
		:param dy: y方向的移动距离
		:param end_position:
		:return: 合法与否
		"""
		pass

	@abstractmethod
	def is_legal_move(self, end_position, chessboard):
		"""
		判断移动到某一位置是否合法

		:param end_position: 将要移动到的位置
		:param chessboard: 当前棋盘对象
		:return: 合法与否
		"""
		pass

	def set_position(self, pos):
		"""
		Set the position of chess piece.

		:param pos: (x, y)
		:return:
		"""
		self.position = pos

	def is_inplace(self):
		"""
		判断棋子是否位于己侧

		:return: True: 在己侧；False: 不在己侧
		"""
		y = self.position[1]
		if self.red and y < 5:
			return False
		elif not self.red and y > 4:
			return False
		return True

	def d_position(self, end_position):
		"""
		计算移动到目标位置需要执行的动作

		:param end_position: 目标位置
		:return: (x轴移动动作, y轴移动动作)
		"""
		dx = end_position[0] - self.position[0]
		dy = end_position[1] - self.position[1]
		return dx, dy

	@staticmethod
	def is_out(pos):
		"""
		检查此坐标是否出棋盘

		:param pos:
		:return: True: 已出棋盘
		"""
		x, y = pos
		if x < 0 or y < 0 or x > 8 or y > 9:
			return True
		return False

	@staticmethod
	def position_has_chess(position, chessboard):
		"""
		判断某个位置是否有棋子

		:param position:
		:param chessboard:
		:return:
		"""
		x, y = position
		if chessboard[x, y]:
			return True
		return False

	def is_own(self, chess):
		"""
		判断是否为己方棋子

		:param chess:
		:return:
		"""
		if self.red == chess.red:
			return True
		return False

	def count_chess(self, end_position, chessboard):
		"""
		计算到目标位置的直线上的棋子数

		:param end_position:
		:param chessboard:
		:return:
		"""
		x, y = self.position
		x_to, y_to = end_position
		dx, dy = self.d_position(end_position)
		dx = dx/abs(dx) if x != x_to else 0
		dy = dy/abs(dy) if y != y_to else 0
		num = 0
		while x != x_to or y != y_to:
			x += dx
			y += dy
			if chessboard[int(x), int(y)]:
				num += 1
		return num

	def possible_moves(self, chessboard):
		"""
		寻找所有可能移动到的合法位置

		:param chessboard: 当前棋盘对象
		:return: 一个合法移动位置的列表: [(0, 1), (2, 3), ...]
		"""
		legal_pos = []
		for pos in self.get_pos_list():
			if not self.is_out(pos):
				if self.is_legal_move(pos, chessboard):
					legal_pos.append(pos)
		return legal_pos


class Bing(Chess):
	def __init__(self, position, red=True):
		super().__init__(position, red)
		self.name = 'bing'
		x, y = self.position
		self.pos_list = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

	def get_pos_list(self):
		x, y = self.position
		return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

	def picture(self):
		if self.red:
			return 'red_pawn.gif'
		else:
			return 'black_pawn.gif'

	def is_legal_action(self, dx, dy, end_position=None):
		if abs(dx) + abs(dy) != 1:
			return False
		if self.is_inplace():  	# 兵未过河
			if (self.red and dy == -1 and dx == 0) or (not self.red and dy == 1 and dx == 0):
				return True
			else:
				return False
		else:  					# 兵已过河
			if (self.red and dy == 1) or (not self.red and dy == -1):
				return False
			else:
				return True

	def is_legal_move(self, end_position, chessboard):
		x, y = end_position
		dx, dy = self.d_position(end_position)
		if self.is_legal_action(dx, dy):  			# 走棋合法
			if not self.position_has_chess(end_position, chessboard):  # 移动到的位置没棋子
				return True
			else:
				if self.is_own(chessboard[x, y]):  	# 本方棋子，不能吃
					return False
				else:  								# 对方棋子，可以吃
					return True
		else:
			return False


class Che(Chess):
	def __init__(self, position, red=True):
		super().__init__(position, red)
		self.name = 'che'
		x, y = self.position
		self.pos_list = [
			(x + 1, y), (x + 2, y), (x + 3, y), (x + 4, y), (x + 5, y), (x + 6, y), (x + 7, y), (x + 8, y),
			(x - 1, y), (x - 2, y), (x - 3, y), (x - 4, y), (x - 5, y), (x - 6, y), (x - 7, y), (x - 8, y),
			(x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4), (x, y + 5), (x, y + 6), (x, y + 7), (x, y + 8),
			(x, y + 9), (x, y - 1), (x, y - 2), (x, y - 3), (x, y - 4), (x, y - 5), (x, y - 6), (x, y - 7),
			(x, y - 8), (x, y - 9)
		]

	def get_pos_list(self):
		x, y = self.position
		return [
			(x + 1, y), (x + 2, y), (x + 3, y), (x + 4, y), (x + 5, y), (x + 6, y), (x + 7, y), (x + 8, y),
			(x - 1, y), (x - 2, y), (x - 3, y), (x - 4, y), (x - 5, y), (x - 6, y), (x - 7, y), (x - 8, y),
			(x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4), (x, y + 5), (x, y + 6), (x, y + 7), (x, y + 8),
			(x, y + 9), (x, y - 1), (x, y - 2), (x, y - 3), (x, y - 4), (x, y - 5), (x, y - 6), (x, y - 7),
			(x, y - 8), (x, y - 9)
		]

	def picture(self):
		if self.red:
			return 'red_rook.gif'
		else:
			return 'black_rook.gif'

	def is_legal_action(self, dx, dy, end_position=None):
		if not (dx == 0 and dy == 0):
			if dx == 0 or dy == 0:
				return True
		return False

	def is_legal_move(self, end_position, chessboard):
		x, y = end_position
		dx, dy = self.d_position(end_position)
		if self.is_legal_action(dx, dy):
			num = self.count_chess(end_position, chessboard)  # 路线上是否有子阻挡
			if not num:  # 没有子
				return True
			if num == 1 and self.position_has_chess(end_position, chessboard):  # 终点位置有子
				if not self.is_own(chessboard[x, y]):  # 不是本方子
					return True
			return False
		else:
			return False


class Ma(Chess):
	def __init__(self, position, red=True):
		super().__init__(position, red)
		self.name = 'ma'
		x, y = self.position
		self.pos_list = [
			(x + 1, y + 2), (x + 2, y + 1), (x - 1, y + 2), (x - 2, y + 1),
			(x - 1, y - 2), (x - 2, y - 1), (x + 1, y - 2), (x + 2, y - 1)
		]

	def get_pos_list(self):
		x, y = self.position
		return [
			(x + 1, y + 2), (x + 2, y + 1), (x - 1, y + 2), (x - 2, y + 1),
			(x - 1, y - 2), (x - 2, y - 1), (x + 1, y - 2), (x + 2, y - 1)
		]

	def picture(self):
		if self.red:
			return 'red_knight.gif'
		else:
			return 'black_knight.gif'

	def is_legal_action(self, dx, dy, end_position=None):
		if dx == 0 or dy == 0:
			return False
		if abs(dx) + abs(dy) == 3:  # 马走日
			return True

	def block(self, dx, dy, chessboard):
		"""
		是否蹩马腿

		:param dx:
		:param dy:
		:param chessboard:
		:return: True: 蹩马腿
		"""
		x, y = self.position
		if abs(dx) == 1:
			y = int(y + dy / 2)
			if not chessboard[x, y]:
				return False
		else:
			x = int(x + dx / 2)
			if not chessboard[x, y]:
				return False
		return True

	def is_legal_move(self, end_position, chessboard):
		x, y = end_position
		dx, dy = self.d_position(end_position)
		if self.is_legal_action(dx, dy) and not self.block(dx, dy, chessboard):
			if not self.position_has_chess(end_position, chessboard):  	# 不吃子
				return True
			else:  														# 吃子
				if not self.is_own(chessboard[x, y]):  # 不是本方棋子
					return True
		return False


class Pao(Chess):
	def __init__(self, position, red=True):
		super().__init__(position, red)
		self.name = 'pao'
		x, y = self.position
		self.pos_list = [
			(x + 1, y), (x + 2, y), (x + 3, y), (x + 4, y), (x + 5, y), (x + 6, y), (x + 7, y), (x + 8, y),
			(x - 1, y), (x - 2, y), (x - 3, y), (x - 4, y), (x - 5, y), (x - 6, y), (x - 7, y), (x - 8, y),
			(x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4), (x, y + 5), (x, y + 6), (x, y + 7), (x, y + 8),
			(x, y + 9), (x, y - 1), (x, y - 2), (x, y - 3), (x, y - 4), (x, y - 5), (x, y - 6), (x, y - 7),
			(x, y - 8), (x, y - 9)]

	def get_pos_list(self):
		x, y = self.position
		return [
			(x + 1, y), (x + 2, y), (x + 3, y), (x + 4, y), (x + 5, y), (x + 6, y), (x + 7, y), (x + 8, y),
			(x - 1, y), (x - 2, y), (x - 3, y), (x - 4, y), (x - 5, y), (x - 6, y), (x - 7, y), (x - 8, y),
			(x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4), (x, y + 5), (x, y + 6), (x, y + 7), (x, y + 8),
			(x, y + 9), (x, y - 1), (x, y - 2), (x, y - 3), (x, y - 4), (x, y - 5), (x, y - 6), (x, y - 7),
			(x, y - 8), (x, y - 9)]

	def picture(self):
		if self.red:
			return 'red_cannon.gif'
		else:
			return 'black_cannon.gif'

	def is_legal_action(self, dx, dy, end_position=None):
		if not (dx == 0 and dy == 0):
			if dx == 0 or dy == 0:
				return True
		return False

	def is_legal_move(self, end_position, chessboard):
		x, y = end_position
		dx, dy = self.d_position(end_position)
		if self.is_legal_action(dx, dy):
			num = self.count_chess(end_position, chessboard)
			if not num:  		# 移动的路线上没子
				return True
			if num == 2 and self.position_has_chess(end_position, chessboard):  # 有两个子且一个在终点处
				if not self.is_own(chessboard[x, y]):
					return True
		return False


class Shi(Chess):
	def __init__(self, position, red=True):
		super().__init__(position, red)
		self.name = 'shi'
		x, y = self.position
		self.pos_list = [(x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1), (x + 1, y - 1)]

	def get_pos_list(self):
		x, y = self.position
		return [(x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1), (x + 1, y - 1)]

	def picture(self):
		if self.red:
			return 'red_mandarin.gif'
		else:
			return 'black_mandarin.gif'

	def is_legal_action(self, dx, dy, end_position=None):
		x, y = end_position
		if abs(dx) == 1 and abs(dy) == 1:
			if self.red and 2 < x < 6 < y < 10:  # 判断是否出九宫格
				return True
			if not self.red and 2 < x < 6 and -1 < y < 3:
				return True
		return False

	def is_legal_move(self, end_position, chessboard):
		x, y = end_position
		dx, dy = self.d_position(end_position)
		if self.is_legal_action(dx, dy, end_position):
			if not self.position_has_chess(end_position, chessboard):  # 终点处无棋子
				return True
			elif not self.is_own(chessboard[x, y]):  # 终点处是对方棋子
				return True
		return False


class Shuai(Chess):
	def __init__(self, position, red=True):
		super().__init__(position, red)
		self.name = 'shuai'
		x, y = self.position
		self.pos_list = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

	def get_pos_list(self):
		x, y = self.position
		return [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

	def picture(self):
		if self.red:
			return 'red_king.gif'
		else:
			return 'black_king.gif'

	def is_legal_action(self, dx, dy, end_position=None):
		x, y = end_position
		if abs(dx) + abs(dy) == 1:
			if self.red and 2 < x < 6 < y < 10:
				return True
			if not self.red and 2 < x < 6 and -1 < y < 3:
				return True
		return False

	def is_legal_move(self, end_position, chessboard):
		x, y = end_position
		dx, dy = self.d_position(end_position)
		for i in chessboard.values():  # 判断是否有白脸将
			if i and i.name == 'shuai' and (i.red != self.red):
				x_enemy, y_enemy = i.position
				if x_enemy == x:
					if y_enemy == y:
						for y_pos in range(min(self.position[1], y) + 1, max(self.position[1], y)):
							if chessboard[x, y_pos]:
								break
						else:
							return True
					else:
						for y_pos in range(min(y_enemy, y) + 1, max(y_enemy, y)):
							if chessboard[x, y_pos]:
								break
						else:
							# print('白脸将')
							return False
				break
		if self.is_legal_action(dx, dy, end_position):
			if not self.position_has_chess(end_position, chessboard):  # 终点处无棋子
				return True
			elif not self.is_own(chessboard[x, y]):  # 终点处是对方棋子
				return True
		return False


class Xiang(Chess):
	def __init__(self, position, red=True):
		super().__init__(position, red)
		self.name = 'xiang'
		x, y = self.position
		self.pos_list = [(x + 2, y + 2), (x - 2, y + 2), (x - 2, y - 2), (x + 2, y - 2)]

	def get_pos_list(self):
		x, y = self.position
		return [(x + 2, y + 2), (x - 2, y + 2), (x - 2, y - 2), (x + 2, y - 2)]

	def picture(self):
		if self.red:
			return 'red_elephant.gif'
		else:
			return 'black_elephant.gif'

	def is_legal_action(self, dx, dy, end_position=None):
		x, y = end_position
		if abs(dx) == 2 and abs(dy) == 2:
			if (self.red and y > 4) or (not self.red and y < 5):
				return True
		return False

	def block(self, dx, dy, chessboard):
		"""
		判断是否别象眼

		:param dx:
		:param dy:
		:param chessboard:
		:return:
		"""
		x, y = self.position
		x = int(x + dx / 2)
		y = int(y + dy / 2)
		if chessboard[x, y]:
			return True
		else:
			return False

	def is_legal_move(self, end_position, chessboard):
		x, y = end_position
		dx, dy = self.d_position(end_position)
		if self.is_legal_action(dx, dy, end_position) and not self.block(dx, dy, chessboard):
			if not self.position_has_chess(end_position, chessboard):  # 终点处无棋子
				return True
			elif not self.is_own(chessboard[x, y]):  # 终点处是对方棋子
				return True
		return False
