# -*- coding: utf-8 -*-
import random
import numpy as np
from search import Search
from model.mcts import MCTS


class AI:
	def __init__(self, c_put=5, n_playout=1000, train=False):
		self.train = train
		self.mcts = MCTS(c_put, n_playout)

	def get_move(self, game_state, mode=0, temperature=1e-3, return_probs=False):
		if mode == 2:
			moves = []
			for move in game_state.get_legal_moves():
				if game_state.can_move(move):
					moves.append(move)
			choice = random.choice(range(len(moves)))
			return moves[choice]
		elif mode == 1:
			search = Search()
			return search.alpha_beta(game_state)
		elif mode == 0:
			moves, probs = self.mcts.get_moves_prob(game_state, temperature)
			if self.train:
				move = np.random.choice(moves, p=0.75 * probs + 0.25 * np.random.dirichlet(0.3*np.ones(len(probs))))
				self.mcts.update_with_move(move)
			else:
				move = np.random.choice(moves, p=probs)
				self.mcts.update_with_move(((-1, -1), (-1, -1)))
			if return_probs:
				return move, (moves, probs)
			else:
				return move
