# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.nn.functional as F
from const import *


class Flatten(nn.Module):
	@staticmethod
	def flatten(x):
		return x.view(-1, OUT_CHANNELS)

	def forward(self, x):
		return self.flatten(x)


class BasicBlock(nn.Module):
	def __init__(self, in_channels, out_channels):
		super().__init__()
		self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3)
		self.bn1 = nn.BatchNorm2d(out_channels)
		self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3)
		self.bn2 = nn.BatchNorm2d(out_channels)

	def forward(self, x):
		res = x
		out = self.conv1(x)
		out = F.relu(self.bn1(out))

		out = self.conv2(out)
		out = self.bn2(out)

		out += res
		out = F.relu(out)

		return out


class Extractor(nn.Module):
	def __init__(self, in_channels, filter_size):
		super().__init__()
		self.conv = nn.Conv2d(in_channels, filter_size, kernel_size=3)
		self.bn = nn.BatchNorm2d(filter_size)

		for index in range(BLOCK_NUM):
			setattr(self, 'res{}'.format(index), BasicBlock(filter_size, filter_size))

	def forward(self, x):
		x = F.relu(self.bn(self.conv(x)))
		for index in range(BLOCK_NUM - 1):
			x = getattr(self, 'res'.format(index))(x)
		maps = getattr(self, 'res'.format(BLOCK_NUM - 1))(x)
		return maps


class ValueHead(nn.Module):
	def __init__(self, in_channels, out_channels):
		super().__init__()
		self.net = nn.Sequential(
			nn.Conv2d(in_channels, 1, kernel_size=1),
			nn.BatchNorm2d(1),
			nn.ReLU(),
			Flatten(),
			nn.Linear(out_channels, 256),
			nn.ReLU(),
			nn.Linear(256, 1),
			nn.Tanh()
		)

	def forward(self, x):
		return self.net(x)


class PolicyHead(nn.Module):
	def __init__(self, in_channels, out_channels):
		super().__init__()
		self.net = nn.Sequential(
			nn.Conv2d(in_channels, 1, kernel_size=1),
			nn.BatchNorm2d(1),
			nn.ReLU(),
			Flatten(),
			nn.Linear(out_channels, MOVE_NUM),
			nn.LogSoftmax(dim=1)
		)

	def forward(self, x):
		return self.net(x).exp()
