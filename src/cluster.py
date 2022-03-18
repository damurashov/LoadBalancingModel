import networkx as nx
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them

from src import entity
from src import ahp_solve


def assign_message(cluster: nx.Graph, msg: entity.Message, decision_making_node: entity.Node, decision_algorithm=ahp_solve.ahp_solve):
	"""
	Bounces the message until its TTL goes to 0, or until it will be decided to assign the message to some node

	:param cluster: Cluster of connected nodes
	:param msg: Message encapsulating task info
	:param decision_making_node: Master node
	:return:
	"""

	if 0 == msg.ttl:
		decision_making_node.add_task(msg)
		return cluster

	neighbors = tuple(cluster.neighbors(decision_making_node))
	assigned_node, _ = decision_algorithm(msg, decision_making_node, *neighbors)

	if assigned_node == decision_making_node:
		decision_making_node.add_task(msg)
		return cluster
	else:
		msg.ttl -= 1
		return assign_message(cluster, msg, assigned_node)
