import unittest
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them
from src import entity
from src import data
from src.generic import Logging


class TestData(unittest.TestCase):

	def test_generate_message(self):
		m = data.generate_message(data.RandomGeneration())
		Logging.debug(TestData.test_generate_message, m)

		m_per_prev = m.per
		m.per = None
		m2 = data.generate_message(data.RandomGeneration(), m)
		max_iter_threshold = 100

		while m2.per == m_per_prev and max_iter_threshold:
			m2 = data.generate_message(data.RandomGeneration(), m)
			max_iter_threshold -= 1

		Logging.debug(TestData.test_generate_message, m2)
		self.assertTrue(m2.per != m_per_prev)
		self.assertTrue(m != m2)

	def test_generate_node(self):
		m = data.generate_node(data.RandomGeneration())
		m2 = data.generate_node(data.RandomGeneration(), m)
		self.assertTrue(m != m2)
