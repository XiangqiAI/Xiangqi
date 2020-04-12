# -*- coding: utf-8 -*-
import random


class AI:
	@staticmethod
	def get_move(game):										# 随机选择
		moves = []
		for move in game.get_legal_moves():
			if game.can_move(move):
				moves.append(move)
		choice = random.choice(range(len(moves)))
		return moves[choice]
