# -*- coding: utf-8 -*-
import numpy as np
from board import GameState
from .net import Net


class Node(object):
	def __init__(self, prior_p, parent=None):
		self.parent = parent
		self.children = {}
		self.N = 0
		self.Q = 0
		self.U = 0
		self.p = prior_p

	def expand(self, prior_moves):
		for move, prob in prior_moves:
			if move not in self.children:
				self.children[move] = Node(self, prob)

	def select(self, c_puct):
		return max(self.children.items(), key=lambda node: node[1].get_value(c_puct))

	def update(self, sub_value):
		self.N += 1
		self.Q += 1.0 * (sub_value - self.Q) / self.N

	def update_above(self, sub_value):
		if self.parent:
			self.parent.update_above(-sub_value)
		self.update(sub_value)

	def get_value(self, c_puct):
		self.U = (c_puct * self.p * np.sqrt(self.parent.N) / (1 + self.N))
		return self.Q + self.U

	def is_leaf(self):
		return self.children == {}

	def is_root(self):
		return self.parent is None


class MCTS(object):
	def __init__(self, c_puct=5, evaluation_fn=None, n_playout=1000):
		self.root = Node(1.0)
		self.c_puct = c_puct
		self.evaluation_fn = evaluation_fn
		self.n_playout = n_playout

	@staticmethod
	def softmax(x):
		probs = np.exp(x - np.max(x))
		probs /= np.sum(probs)
		return probs

	def playout(self, game: GameState):
		node = self.root
		while True:
			if node.is_leaf():
				break
			move, node = node.select(self.c_puct)
			game.move(move)
		prob, wr = Net('Model').evaluation_fn(game)
		if not game.checkmate():
			node.expand(prob)
		else:
			wr = -1.0
		node.update_above(-wr)

	def	get_moves_prob(self, state: GameState, temperature):
		for i in range(self.n_playout):
			state_copy = state.copy()
			self.playout(state_copy)
		move_visits = [(move, node.N) for move, node in self.root.children.items()]
		moves, visits = zip(*move_visits)
		probs = self.softmax(1.0 / temperature * np.log(np.array(visits) + 1e-10))
		return moves, probs

	def update_with_move(self, last_move):
		if last_move in self.root.children:
			self.root = self.root.children[last_move]
			self.root.parent = None
		else:
			self.root = Node(1.0, None)
