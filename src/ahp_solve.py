import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them

from ahpy.ahpy.ahpy import Graph, to_pairwise
from src import entity
from generic import Logging


def ahp_solve(msg: entity.Message, decision_making_node: entity.Node, *candidate_nodes):

	graph = Graph("root")
	graph.set_weights("root", to_pairwise({
		"per": msg.per,
		"eff": msg.eff,
		"dtr": msg.dtr,
		"crit": msg.crit,
	}))

	all_nodes = (decision_making_node,) + candidate_nodes

	graph.set_weights("per", to_pairwise({str(node.identifier): node.per for node in all_nodes}))  # Performance weights
	graph.set_weights("eff", to_pairwise({str(node.identifier): 1 / node.eff for node in all_nodes}))  # Efficiency weights

	# Compose str weights
	all_tasks = 1
	for node in all_nodes:
		for task in node.tasks:
			all_tasks += task.per
	graph.set_weights("dtr", to_pairwise({str(node.identifier): all_tasks / (sum([task.per for task in node.tasks]) + 1) for node in all_nodes}))

	graph.set_weights("crit", to_pairwise({str(node.identifier): msg.ttl + 1 if node == decision_making_node else msg.ttl for node in all_nodes}))

	# Match the result with the node it points to
	weights = graph.get_weights()
	weights = {int(i[0]) : i[1] for i in weights.items()}
	max_node_identifier = max(weights, key=weights.get)
	result_node = list(filter(lambda n: n.identifier == max_node_identifier, all_nodes))[0]

	return result_node, weights
