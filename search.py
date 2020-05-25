# -*- coding: utf-8 -*-
from game import Game


class Search:
	def __init__(self):
		self.discount = 0.1
		self.value = {
			'兵': 100,
			'炮': 450,
			'车': 900,
			'马': 400,
			'象': 200,
			'士': 200,
			'帅': 100000
		}
		self.depth = 1

	def evaluation(self, game: Game):
		score = 0
		if game.checkmate():
			return -1000000
		chessboard = game.chessboard
		for piece in chessboard.values():
			if piece:
				score += self.value[piece.name] * (1 if game.red_move == piece.red else -1)
				for x, y in piece.possible_moves(chessboard):
					if chessboard[x, y]:
						if chessboard[x, y].red == piece.red:
							score += self.value[chessboard[x, y].name] * (1 if game.red_move == piece.red else -1)
						else:
							score += self.value[chessboard[x, y].name] * (1 if game.red_move == piece.red else -.1)
		score = -1000000 if score < -1000000 else 1000000 if score > 1000000 else score
		return score

	def max_value(self, game, alpha, beta, depth):
		depth += 1
		if game.checkmate() or depth == self.depth:
			return self.evaluation(game)
		v = -float('Inf')
		for move in game.get_legal_moves():
			v = max(v, self.min_value(game.generate_successor(move), alpha, beta, depth))
			if v > beta:
				return v
			alpha = max(alpha, v)
		return v

	def min_value(self, game, alpha, beta, depth):
		if game.checkmate():
			return self.evaluation(game)
		v = float('Inf')
		for move in game.get_legal_moves():
			v = min(v, self.max_value(game.generate_successor(move), alpha, beta, depth))
			if v < alpha:
				return v
			beta = min(beta, v)
		return v

	def alpha_beta(self, game):
		v_start = -float('Inf')
		alpha_start = -float('Inf')
		beta_start = float('Inf')
		best_move = None
		for start_move in game.get_legal_moves():
			curr = self.min_value(game.generate_successor(start_move), alpha_start, beta_start, 0)
			if curr > v_start:
				v_start = curr
				best_move = start_move
			alpha_start = max(alpha_start, v_start)
		return best_move
