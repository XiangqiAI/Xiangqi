# -*- coding: utf-8 -*-
from display import Display
from board import GameState
from agent import AI
from model.train import Train
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
	python cchess.py -t
	- train the model
	"""
	parser = OptionParser(usage_str)
	parser.add_option('-m', '--mute', action='store_true', dest='isMuted', help='mute the game', default=False)
	parser.add_option('-t', '--train', action='store_true', dest='isTrainMode', help='train mode', default=False)
	options, junk = parser.parse_args(argv)
	if len(junk):
		raise Exception('Options not expected' + str(junk))
	args = dict()
	args['is_muted'] = options.isMuted
	args['is_train_mode'] = options.isTrainMode
	return args


def get_move(agent, game, layout: Display = None):					# 获取下一步落子
	if agent == 'player':
		return layout.get_move(game_state=game)
	else:
		return AI.get_move(game_state=game)


def pvn(is_muted):										# 进行游戏
	while True:
		game_state = GameState()
		display = Display(is_muted)
		agents = []
		index = 0
		mode = display.begin()							# 获取游戏模式（双人/人机）
		if mode == 'pvp':
			agents = ('player', 'player')
		elif mode == 'pvc':
			agents = ('player', 'AI')
			index = random.randint(0, 1)
		display.init(game_state)
		while True:										# 双方依次进行
			move = get_move(agents[index], game=game_state, layout=display)
			game_state.move(move)
			display.move(move)
			index = 1 - index							# index是目前回合一方
			if game_state.is_end():
				if game_state.winner == 1:
					print('红方胜')
				elif game_state.winner == -1:
					print('黑方胜')
				else:
					print('Tie')
				break
			elif game_state.check():
				print('将军')
				display.check(game_state.red_move)


def run(is_muted, is_train_mode):
	if is_train_mode:
		instance = Train()
		instance.run()
	else:
		pvn(is_muted)


if __name__ == '__main__':
	run(**read_command(sys.argv[1:]))
