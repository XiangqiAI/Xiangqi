# -*- coding: utf-8 -*-
from display import Display
from game import Game
from agent import AI
import sys
import random


def read_command(argv):									# 读取命令行参数
	"""
	Process the command used to run cchess from the command line.

	:param argv:
	:return:
	"""
	from optparse import OptionParser
	usage_str = """
	python cchess.py -m
	- starts a muted game
	"""
	parser = OptionParser(usage_str)
	parser.add_option('-m', '--mute', action='store_true', dest='isMuted', help='mute the game', default=False)
	options, junk = parser.parse_args(argv)
	if len(junk):
		raise Exception('Options not expected' + str(junk))
	args = dict()
	args['is_muted'] = options.isMuted
	return args


def get_move(agent, game, layout=None):					# 获取下一步落子
	if agent == 'player':
		return layout.get_move(game=game)
	else:
		return AI.get_move(game=game)


def pvn(is_muted):										# 进行游戏
	while True:
		game = Game()
		display = Display(is_muted)
		agents = []
		index = 0
		mode = display.begin()							# 获取游戏模式（双人/人机）
		if mode == 'pvp':
			agents = ('player', 'player')
		elif mode == 'pvc':
			agents = ('player', 'AI')
			index = random.randint(0, 1)
		display.init(game)
		while True:										# 双方依次进行
			move = get_move(agents[index], game=game, layout=display)
			game.move(move)
			display.move(move)
			index = 1 - index							# index是目前回合一方
			if game.checkmate():
				if game.red_move:
					print('黑方胜')
				else:
					print('红方胜')
				break
			elif game.check():
				print('将军')


def run(is_muted, train=False, graphics=False):
	if train:
		pass
	else:
		pvn(is_muted)


if __name__ == '__main__':
	run(**read_command(sys.argv[1:]))
