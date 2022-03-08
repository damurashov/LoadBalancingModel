import unittest
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them
from src import entity


class TestEntity(unittest.TestCase):

	def test_hashable(self):
		n1 = entity.Node(per=12, eff=5)
		n2 = entity.Node(per=12, eff=5)

		d = {n1: "a", n2: "b"}

		self.assertTrue(d[n1] == "a")
