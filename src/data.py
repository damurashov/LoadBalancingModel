import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them

from src import entity
from random import randint
from dataclasses import dataclass, field
import copy
import networkx

@dataclass
class RandomGeneration:
	cpu_clock_min: int = 1200  # Min clock freq. in MHz
	cpu_clock_max: int = 6000  # Max clock freq. in MHz
	cpu_n_cores_max: int = 16  # Max number of CPU cores
	cpu_eff_min: int = 40  # CPU's min thermal radiation, in W, opposite to thermal efficiency
	cpu_eff_max: int = 200  # CPU's max thermal radiation, in W, opposite to thermal efficiency
	msg_ttl_min: int = 5  # Min ttl of a message
	msg_ttl_max: int = 10  # Max ttl of a message
	msg_score_min: int = 1  # Min score that can be assigned to "per", "eff", "crit", or "dtr". Min = 1
	msg_score_max: int = 10  # Max score that can be assigned to "per", "eff", "crit", or "dtr". Min = 1


def generate_message(r: RandomGeneration, m: entity.Message = None):
	"""
	:param r: Configuration for the random generator
	:param m: Message instance. Fields different from None will be inherited without generation. E.g., if a Message's
	          TTL=None, a new TTL value will be generated, but if the message has TTL=10, it will be inerited by the
	          generated one
	"""

	if m is None:
		m = entity.Message(None, None, None, None, None)

	res = copy.deepcopy(m)

	if res.ttl is None:
		res.ttl = randint(r.msg_ttl_min, r.msg_ttl_max)

	if res.per is None:
		res.per = randint(r.msg_score_min, r.msg_score_max)

	if res.eff is None:
		res.eff = randint(r.msg_score_min, r.msg_score_max)

	if res.dtr is None:
		res.dtr = randint(r.msg_score_min, r.msg_score_max)

	if res.crit is None:
		res.crit = randint(r.msg_score_min, r.msg_score_max)

	return res


def generate_node(r: RandomGeneration, n: entity.Node = None):

	if n is None:
		n = entity.Node(None, None, [])

	res = copy.deepcopy(n)

	if res.per is None:
		res.per = randint(1, r.cpu_n_cores_max) * randint(r.cpu_clock_min, r.cpu_clock_max)

	if res.eff is None:
		res.eff = randint(r.cpu_eff_min, r.cpu_eff_max)

	return res


def make_cluster(nodes, topology):
	"""
	:param nodes: Ordered list of nodes
	:param topology: List of numbers which will be parsed into pairs, each pair will represent an edge
	:return: `networkx.Graph` object

	Example: cl = make_cluster([generate_node(RandomGeneration()), generate_node(RandomGeneration()], [0, 1])
	"""
	assert (len(topology) % 2 == 0)  # Must be pairs of numbers
	assert all([type(topology[i]) is int for i in range(len(topology))])

	def np(a, b):  # Get pair
		return nodes[a], nodes[b]

	def lnp(l, *pairs):  # List of pairs
		a = pairs[0]
		b = pairs[1]
		l.append(np(a, b))

		if len(pairs) > 2:
			return lnp(l, *pairs[2:])
		else:
			return l

	return networkx.Graph(lnp([], *topology))
