# -*- coding: utf-8 -*-
import pygame
import os

data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'src')


def load_image(name):
	filename = os.path.join(data_dir, name)
	surface = pygame.image.load(filename)
	return surface.convert(), surface.get_rect()


class StartGame(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('background.jpg')


class AddButton(pygame.sprite.Sprite):
	def __init__(self, name, position):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(name)
		x, y = position
		self.rect.center = (x * 80 + 40, y * 80 + 40)   	# 使得棋子位于棋盘图像中合适位置（小格内居中）
		self.position = position


class Background(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('chessboard.gif')


class AddChess(pygame.sprite.Sprite):
	def __init__(self, name, position):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(name)
		x, y = position
		self.rect.center = (x * 80 + 40, y * 80 + 40)   	# 使得棋子位于棋盘图像中合适位置（小格内居中）
		self.position = position

	def move(self, position):
		x, y = position
		self.rect.center = (x * 80 + 40, y * 80 + 40)   	# 使得棋子位于棋盘图像中合适位置（小格内居中）
		self.position = position


class Display:
	def __init__(self, is_muted=False):
		self.screen = pygame.display.set_mode((720, 800))  	# 设置屏幕大小为（720，800），方便对应棋子位置
		self.pieces = None
		self.board = pygame.sprite.Group()  				# 棋盘
		self.board.add((Background()))
		pygame.mixer.init()
		if not is_muted:
			pygame.mixer.music.load(os.path.join(data_dir, 'easy_mode.wav'))
			pygame.mixer.music.play(-1)

	@staticmethod
	def convert_pos(position):  # 将鼠标点击位置转化为棋盘编号位置（0，0）-（9，10）
		x, y = position
		return x // 80, y // 80

	def get_pos(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:    			# 点击某处
					pos = self.convert_pos(pygame.mouse.get_pos())		# 将点击位置转化为棋盘上坐标
					if pos:
						return pos
				elif event.type == pygame.QUIT:							# 退出游戏
					quit()

	def begin(self):
		start_page = pygame.sprite.Group()
		start_page.add(StartGame())
		buttons = pygame.sprite.Group()
		buttons.add(AddButton('pvp.jpg', (3, 4)))
		buttons.add(AddButton('pvc.jpg', (3, 7)))
		start_page.draw(self.screen)
		buttons.draw(self.screen)
		pygame.display.flip()
		while True:
			pos = self.get_pos()
			if pos == (3, 4) or pos == (2, 4) or pos == (4, 4):  	# 点击双人对战按钮
				return 'pvp'
			elif pos == (3, 7) or pos == (2, 7) or pos == (4, 7):  	# 点击人机对战按钮
				return 'pvc'

	def init(self, game):
		self.pieces = pygame.sprite.Group()  	# 所有棋子
		for piece in game.chessboard.values():  # 找到所有棋子
			if piece:
				self.pieces.add((AddChess(piece.picture(), piece.position)))
		self.board.draw(self.screen)  			# 显示棋盘背景
		self.pieces.draw(self.screen)  			# 显示所有棋子
		pygame.display.flip()

	def get_move(self, game):
		start = (-1, -1)  						# 棋子出发位置
		while True:
			end = self.get_pos()				# 将点击位置转化为棋盘上坐标
			if game.can_move((start, end)):		# 棋子从出发位置到鼠标点击位置移动合法
				return start, end 				# 出发位置赋值为空
			else:  								# 出发位置未赋值或者结束位置不合法
				start = end  					# 将出发位置设置为鼠标点击位置

	def move(self, move):
		start, end = move
		for piece in self.pieces:  			# 寻找移动的棋子位置
			if piece.position == end:  		# 棋子被吃
				piece.kill()
			if piece.position == start:  	# 棋子从出发位置移动
				piece.move(end)
		self.board.draw(self.screen)  		# 显示棋盘背景
		self.pieces.draw(self.screen)
		pygame.display.flip()

	# def pvp(self):
	# 	"""
	# 	双人对战
	# 	"""
	# 	board = pygame.sprite.Group()   			# 棋盘
	# 	board.add((Background()))
	# 	pieces = pygame.sprite.Group()   			# 所有棋子
	# 	game = Game()
	# 	for piece in game.chessboard.values():    	# 找到所有棋子
	# 		if piece:
	# 			pieces.add((AddChess(piece.picture(), piece.position)))
	# 	start = (-1, -1)     						# 棋子出发位置
	# 	while True:
	# 		for event in pygame.event.get():
	# 			if event.type == pygame.MOUSEBUTTONDOWN:    		# 点击某处
	# 				end = convert_pos(pygame.mouse.get_pos())		# 将点击位置转化为棋盘上坐标
	# 				if game.move(start, end):      					# 棋子从出发位置到鼠标点击位置移动合法
	# 					for piece in pieces:              			# 寻找移动的棋子位置
	# 						if piece.position == end:    			# 棋子被吃
	# 							piece.kill()
	# 						if piece.position == start:				# 棋子从出发位置移动
	# 							piece.move(end)
	# 					start = (-1, -1) 							# 出发位置赋值为空
	# 					if game.checkmate():
	# 						if game.red_move:
	# 							print('黑方胜')
	# 						else:
	# 							print('红方胜')
	# 						return
	# 					elif game.check():
	# 						print('将军')
	# 				else: 											# 出发位置未赋值或者结束位置不合法
	# 					start = end 								# 将出发位置设置为鼠标点击位置
	# 			elif event.type == pygame.QUIT:						# 退出游戏
	# 				return
	# 		board.draw(self.screen)									# 显示棋盘背景
	# 		pieces.draw(self.screen)								# 显示所有棋子
	# 		pygame.display.flip()
	#
	# def pvc(self):
	# 	"""
	# 	人机
	# 	"""
	# 	board = pygame.sprite.Group()				# 棋盘
	# 	board.add((Background()))
	# 	pieces = pygame.sprite.Group()				# 所有棋子
	# 	game = Game()
	# 	for piece in game.chessboard.values():		# 寻找所有棋子
	# 		if piece:
	# 			pieces.add((AddChess(piece.picture(), piece.position)))			# 将该棋子加入所有棋子的集合中
	# 	start = (-1, -1) 														# 棋子出发位置
	# 	red_or_black = random.randint(0, 1)
	# 	if red_or_black:														# 机器先手
	# 		# screen = pygame.transform.rotate(screen, 180)
	# 		possible_moves = []													# 随机确定落子
	# 		for piece in game.chessboard.values():
	# 			if piece:
	# 				if piece.red == game.red_move:
	# 					possible_moves += [(piece.position, piece.possible_moves(game.chessboard))]
	# 		choice = random.choice(range(len(possible_moves)))
	# 		start, nxt = possible_moves[choice]
	# 		choice = random.choice(range(len(nxt)))
	# 		end = nxt[choice]
	# 		game.move(start, end)
	# 		for piece in pieces:				# 寻找移动的棋子位置
	# 			if piece.position == end:		# 棋子被吃
	# 				piece.kill()
	# 			if piece.position == start:		# 棋子从出发位置移动
	# 				piece.move(end)
	# 		start = (-1, -1)
	# 	while True:
	# 		for event in pygame.event.get():
	# 			if event.type == pygame.MOUSEBUTTONDOWN:			# 点击某处
	# 				end = convert_pos(pygame.mouse.get_pos())		# 将点击位置转化为棋盘上坐标
	# 				if game.move(start, end):						# 棋子从出发位置到鼠标点击位置移动合法
	# 					for piece in pieces:						# 寻找移动的棋子位置
	# 						if piece.position == end:				# 棋子被吃
	# 							piece.kill()
	# 						if piece.position == start:				# 棋子从出发位置移动
	# 							piece.move(end)
	# 					if game.checkmate():
	# 						if game.red_move:
	# 							print('黑方胜')
	# 						else:
	# 							print('红方胜')
	# 						return
	# 					elif game.check():
	# 						print('将军')
	#
	# 					"""
	# 					此处为AI的应对
	#
	# 						def AI(chessboard):
	# 							...
	# 							start = (x, y)
	# 							end = (x_to, y_to)
	# 							...
	# 							return start, end
	#
	# 					参数为一个chessboard字典
	# 					返回两个元组，分别是将要移动棋子的所在位置和目标位置
	# 					"""
	# 					start = (-1, -1)
	# 					possible_moves = []
	# 					for piece in game.chessboard.values():
	# 						if piece and piece.red == game.red_move and len(piece.possible_moves(game.chessboard)):
	# 							possible_moves += [(piece.position, piece.possible_moves(game.chessboard))]
	# 					while not game.move(start, end):
	# 						choice = random.choice(range(len(possible_moves)))
	# 						start, nxt = possible_moves[choice]
	# 						choice = random.choice(range(len(nxt)))
	# 						end = nxt[choice]
	# 					for piece in pieces:				# 寻找移动的棋子位置
	# 						if piece.position == end:		# 棋子被吃
	# 							piece.kill()
	# 						if piece.position == start:		# 棋子从出发位置移动
	# 							piece.move(end)
	# 					if game.checkmate():
	# 						if game.red_move:
	# 							print('黑方胜')
	# 						else:
	# 							print('红方胜')
	# 						return
	# 					elif game.check():
	# 						print('将军')
	# 					start = (-1, -1) 					# 出发位置赋值为空
	# 				else: 									# 出发位置未赋值或者结束位置不合法
	# 					start = end 						# 将出发位置设置为鼠标点击位置
	# 			elif event.type == pygame.QUIT:				# 退出游戏
	# 				return
	# 		board.draw(self.screen)							# 显示棋盘背景
	# 		pieces.draw(self.screen)						# 显示所有棋子
	# 		pygame.display.flip()
