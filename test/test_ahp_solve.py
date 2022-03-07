import unittest
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them
from src import entity, ahp_solve


class TestAhpSolve(unittest.TestCase):

    def setUp(self) -> None:
        self.nodes = [
            entity.Node(per=10, eff=4, tasks=[]),
            entity.Node(per=7, eff=7, tasks=[]),
            entity.Node(per=6, eff=3, tasks=[]),
        ]

        self.message = entity.Message(ttl=3, per=10, eff=9, dtr=7, crit=3)

    def test_probe(self):
        ahp_solve.ahp_solve(self.message, self.nodes[0], *self.nodes[1:])