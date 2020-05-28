# -*- coding: utf-8 -*-
import random
import numpy as np
from board import GameState
from agent import AI
from .net import Net


class Train(object):
	def __init__(self, batch_num=100):
		self.lr = 2e-3
		self.lr_multiplier = 1.0
		self.net = Net()
		self.ai = AI(train=True, evaluation_fn=self.net.evaluation_fn)
		self.data_buffer = []
		self.game_len = 0
		self.epochs = 5
		self.batch_size = 512
		self.batch_num = batch_num
		self.kl_trigger = 0.2

	def self_play(self):
		game_state = GameState()
		states = []
		probs = []
		players = []
		while True:
			move, moves_probs = self.ai.get_move(game_state, return_probs=True)
			states.append(game_state.state())
			probs.append(moves_probs)
			players.append(game_state.red_move)
			if game_state.is_end():
				wrs = np.zeros(len(players))
				if game_state.winner:
					wrs[np.array(players) == game_state.red_move] = -1.0
					wrs[np.array(players) != game_state.red_move] = 1.0
				return zip(states, probs, wrs)


	def collect_data(self, n=1):
		for i in range(n):
			data = self.self_play()
			data = list(data)[:]
			self.game_len = len(data)
			self.data_buffer.extend(data)

	def policy_update(self):
		kl, loss, entropy = 0, 0, 0
		batch = random.sample(self.data_buffer, self.batch_size)
		state_batch = [data[0] for data in batch]
		probs_batch = [data[1] for data in batch]
		wr_batch = [data[2] for data in batch]
		probs_old, wr_old = self.net.forward(state_batch)
		for i in range(self.epochs):
			loss, entropy = self.net.train_model(state_batch, wr_batch, probs_batch, self.lr*self.lr_multiplier)
			probs_new, entropy_new = self.net.forward(state_batch)
			kl = np.mean(np.sum(probs_old*(np.log(probs_old+1e-10)-np.log(probs_new+1e-10)), axis=1))
			if kl > self.kl_trigger * 4:
				break
		if kl > self.kl_trigger * 2 and self.lr_multiplier > 0.1:
			self.lr_multiplier /= 1.5
		elif kl < self.kl_trigger / 2 and self.lr_multiplier < 10:
			self.lr_multiplier *= 1.5
		print('kl: {}, lr: {}, loss: {}, entropy: {}'.format(kl, self.lr*self.lr_multiplier, loss, entropy))

	def run(self):
		for i in range(self.batch_num):
			self.collect_data()
			print('Game {}: size {}'.format(i + 1, self.game_len))
			if len(self.data_buffer) > self.batch_size:
				print('Updating policy')
				self.policy_update()
				self.data_buffer = []
			self.net.save()
