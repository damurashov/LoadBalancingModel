import unittest
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them
from src import entity


class TestEntity(unittest.TestCase):

    def test_probe(self):
        n = entity.Node(per=12, eff=5)
        print(n.__dir__())