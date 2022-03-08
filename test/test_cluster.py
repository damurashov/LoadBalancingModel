import unittest
import networkx as nx
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them
from src import entity, data, cluster
from src.generic import Logging


class TestEntity(unittest.TestCase):

	def setUp(self) -> None:
		def np(a, b):  # Get pair
			return n[a], n[b]

		def lnp(l, *pairs):  # List of pairs
			a = pairs[0]
			b = pairs[1]
			l.append(np(a, b))

			if len(pairs) > 2:
				return lnp(l, *pairs[2:])
			else:
				return l

		rg = data.RandomGeneration()
		n = [data.generate_node(rg) for _ in range(6)]
		self.cluster = nx.Graph(lnp([], 0, 1, 0, 4, 1, 3, 1, 2, 4, 3, 4, 5, 3, 2, 3, 5, 2, 5))
		self.entry_node = n[0]
		self.nodes = n

	def test_adjacency(self):
		n1 = entity.Node(per=12, eff=5)
		n2 = entity.Node(per=12, eff=5)
		g = nx.Graph([(n1, n2)])
		self.assertTrue(1 == len(list(g.neighbors(n1))))
		self.assertTrue(1 == len(list(g.neighbors(n2))))

	def test_assign_message(self):
		cl = None
		target_node = self.nodes[5]
		max_iter_threshold = 10000

		for _ in range(max_iter_threshold):
			cl = cluster.assign_message(self.cluster, data.generate_message(data.RandomGeneration()), self.entry_node)

			hist = {n.identifier: len(n.tasks) for n in cl.nodes}
			Logging.debug(hist)

			if len(target_node.tasks):
				return

		self.assertTrue(False)
