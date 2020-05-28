# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from .const import *
from board import GameState


class Flatten(nn.Module):
	@staticmethod
	def flatten(x):
		return x.view(-1, OUT_CHANNELS)

	def forward(self, x):
		return self.flatten(x)


class Net(nn.Module):
	def __init__(self, model='Model'):
		super().__init__()
		self.basic_net = nn.Sequential(
			nn.Conv2d(FEATURES_NUM, 32, kernel_size=3, padding=1),
			nn.BatchNorm2d(32),
			nn.ReLU(),
			nn.Conv2d(32, 64, kernel_size=3, padding=1),
			nn.BatchNorm2d(64),
			nn.ReLU(),
			nn.Conv2d(64, 128, kernel_size=3, padding=1),
			nn.BatchNorm2d(128),
			nn.ReLU()
		)
		self.value_net = nn.Sequential(
			nn.Conv2d(128, 1, kernel_size=1),
			nn.BatchNorm2d(1),
			nn.ReLU(),
			Flatten(),
			nn.Linear(OUT_CHANNELS, 256),
			nn.ReLU(),
			nn.Linear(256, 1),
			nn.Tanh()
		)
		self.policy_net = nn.Sequential(
			nn.Conv2d(128, 1, kernel_size=1),
			nn.BatchNorm2d(1),
			nn.ReLU(),
			Flatten(),
			nn.Linear(OUT_CHANNELS, MOVE_NUM),
			nn.LogSoftmax(dim=1)
		)
		self.optimizer = torch.optim.Adam(self.parameters())
		try:
			self.load_state_dict(torch.load(model))
		except FileNotFoundError:
			print('Model file not found')

	def forward(self, x):
		feature_map = self.basic_net(x)
		wr = self.value_net(feature_map)
		prob = self.policy_net(feature_map).exp()
		return prob, wr

	def evaluation_fn(self, game_state: GameState):
		state = game_state.state()
		prob, wr = self.forward(state)
		prob = zip(game_state.all_moves, prob.tolist()[0])
		return prob, wr

	def train_model(self, states, wr, prob, lr):
		self.train()
		states = Variable(torch.tensor(states))
		prob = Variable(torch.tensor(prob))
		wr = Variable(torch.tensor(wr))
		for param_group in self.optimizer.param_groups:
			param_group['lr'] = lr
		prob_predict, wr_predict = self.forward(states)
		loss = F.mse_loss(wr_predict.view(-1), wr) - torch.mean(torch.sum(prob*prob_predict, 1))
		loss.backward()
		self.optimizer.step()
		entropy = - torch.mean(torch.sum(torch.exp(prob_predict) * prob_predict, 1))
		return loss.item(), entropy.item()

	def save(self, filename='Model'):
		torch.save(self.state_dict(), filename)
