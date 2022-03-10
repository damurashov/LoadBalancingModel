from dataclasses import dataclass, field
from itertools import count

@dataclass
class Message:
	ttl: int  # Time-to-live

	# Scores
	per: int  # How important a node's performance is
	eff: int  # How important a node's efficiency is
	dtr: int  # How important it is to distribute load evenly
	crit: int  # How important it is to make decision now

@dataclass
class Node:
	per: int  # Performance
	eff: int  # Energy consumption (opposite to efficiency)
	tasks: list = field(default_factory=list)  # List of tasks
	identifier: int = field(default_factory=count().__next__)
	name: str = ""

	def __repr__(self):
		return str(self.identifier)

	def __eq__(self, other):
		return self.identifier == other.identifier

	def __hash__(self):
		return hash(self.identifier)

	def add_task(self, task):
		self.tasks.append(task)
