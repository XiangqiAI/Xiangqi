# -*- coding: utf-8 -*-
import pygame
import os
from time import sleep

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
		self.rect.center = (x * 80 + 40, y * 80 + 40)   	# 使得按钮位于合适位置
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


class CheckBox(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('check_box.jpg')
		x, y = position
		self.rect.center = (x * 80 + 40, y * 80 + 40)   	# 使得选择框位于棋盘图像中合适位置（小格内居中）


class Check(pygame.sprite.Sprite):
	def __init__(self, red):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('check.gif')		# 160*160
		if red:
			self.rect.center = (360, 680)
		else:
			self.rect.center = (360, 120)


class CheckMate(pygame.sprite.Sprite):
	def __init__(self, red):
		pygame.sprite.Sprite.__init__(self)
		if red:
			self.image, self.rect = load_image('red_win.png')		# 320*240
		else:
			self.image, self.rect = load_image('black_win.png')
		self.rect.center = (360, 400)


class Display:
	def __init__(self, is_muted=False):
		self.screen = pygame.display.set_mode((720, 800))  	# 设置屏幕大小为（720，800），方便对应棋子位置
		self.pieces = None
		self.board = pygame.sprite.Group()  				# 棋盘
		self.board.add((Background()))
		pygame.display.set_caption('中国象棋')
		icon = pygame.image.load(os.path.join(data_dir, 'icon.jpg'))
		pygame.display.set_icon(icon)
		pygame.mixer.init()
		if not is_muted:
			pygame.mixer.music.load(os.path.join(data_dir, 'easy_mode.wav'))
			pygame.mixer.music.play(-1)

	@staticmethod
	def convert_pos(position):  # 将鼠标点击位置转化为棋盘编号位置（0，0）-（9，10）
		x, y = position
		return x // 80, y // 80

	def get_pos(self):
		"""
		等待玩家点击
		:return:
		"""
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:    			# 点击某处
					pos = self.convert_pos(pygame.mouse.get_pos())		# 将点击位置转化为棋盘上坐标
					if pos:
						return pos
				elif event.type == pygame.QUIT:							# 退出游戏
					quit()

	def begin(self):
		"""
		开始界面
		:return:
		"""
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
		"""
		棋局开始
		:param game:
		:return:
		"""
		self.pieces = pygame.sprite.Group()  	# 所有棋子
		for piece in game.chessboard.values():  # 找到所有棋子
			if piece:
				self.pieces.add((AddChess(piece.picture(), piece.position)))
		self.board.draw(self.screen)  			# 显示棋盘背景
		self.pieces.draw(self.screen)  			# 显示所有棋子
		pygame.display.flip()

	def get_move(self, game):
		"""
		获取玩家操作
		:param game:
		:return:
		"""
		check_box = pygame.sprite.Group()
		start = (-1, -1)  						# 棋子出发位置
		while True:
			end = self.get_pos()				# 将点击位置转化为棋盘上坐标
			if game.can_move((start, end)):		# 棋子从出发位置到鼠标点击位置移动合法
				check_box.empty()
				return start, end 				# 出发位置赋值为空
			else:  								# 出发位置未赋值或者结束位置不合法
				start = end  					# 将出发位置设置为鼠标点击位置
				check_box.empty()
				check_box.add(CheckBox(start))
				self.board.draw(self.screen)
				check_box.draw(self.screen)
				self.pieces.draw(self.screen)
				pygame.display.flip()

	def move(self, move):
		"""
		移动棋子
		"""
		start, end = move
		for piece in self.pieces:  				# 寻找移动的棋子位置
			if piece.position == end:  			# 棋子被吃
				piece.kill()
			if piece.position == start:  		# 棋子从出发位置移动
				piece.move(end)
		self.board.draw(self.screen)  			# 显示棋盘背景
		self.pieces.draw(self.screen)
		pygame.display.flip()

	def check(self, red):
		check = pygame.sprite.Group()
		check.add(Check(red))
		check.draw(self.screen)
		pygame.display.flip()
		sleep(0.2)
		self.board.draw(self.screen)  # 显示棋盘背景
		self.pieces.draw(self.screen)
		pygame.display.flip()
