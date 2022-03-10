import matplotlib.pyplot as plt
import networkx
import pathlib
import sys
import plotly.express as px
import pandas
import csv

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))  # We need files from "src/", that's how we access them

from res.processors import PROCESSORS
from src import data, entity, cluster
from src.generic import Logging
from copy import deepcopy

cluster_topology = [
	3, 4,
	16, 17,
	12, 13,
	14, 16,
	0, 2,
	8, 9,
	8, 12,
	17, 18,
	11, 14,
	1, 3,
	16, 19,
	15, 17,
	18, 19,
	4, 5,
	5, 6,
	4, 20,
	0, 1,
	0, 7,
	# 9, 10,
	1, 2,
	10, 11,
	11, 13,
	7, 9,
	19, 20,
	15, 16,
	10, 12,
	6, 10,
	16, 18,
	3, 5,
	14, 20,
	2, 6,
	13, 15,
	7, 8,
]
cluster_size = len(set(cluster_topology))


def profile_load_distribution():
	rg = data.RandomGeneration(
		msg_score_min=5,
		msg_score_max=10
	)

	message_template = entity.Message(
		ttl=int(cluster_size * 1.5),
		per=None,
		# Message's performance requirements (that's how `per` field may be interpreted) will be the only varying metric
		eff=5,
		dtr=8,
		crit=3
	)

	return rg, message_template


def profile_energy_efficiency():
	rg = data.RandomGeneration(
		msg_score_min=2,
		msg_score_max=4
	)

	message_template = entity.Message(
		ttl=int(cluster_size * 1.5),
		per=None,
		# Message's performance requirements (that's how `per` field may be interpreted) will be the only varying metric
		eff=8,
		dtr=4,
		crit=2
	)

	return rg, message_template


def plot_cluster(cl):
	p = plt.subplot(111)
	networkx.draw(cl, with_labels=True, pos=networkx.spectral_layout(cl, weight="name"), font_weight='bold', node_color='white', node_size=700, font_size=17)
	plt.show()


def plot_fit_performance():
	d = dict()
	d["per"] = list()
	d["load"] = list()

	nodes_max_performance = data.nodes_max_per(nodes)
	for n in nodes:
		d["per"].append(n.per / nodes_max_performance)
		d["load"].append(data.node_tasks_sum_per(n))

	df = pandas.DataFrame(data=d)
	fig = px.scatter(df, x="per", y="load", trendline="ols")
	fig.show()


def plot_fit_efficiency():
	d = dict()
	d["eff"] = list()
	d["load"] = list()

	nodes_max_inefficiency = data.nodes_max_eff(nodes)

	for n in nodes:
		d["eff"].append(n.eff / nodes_max_inefficiency)
		d["load"].append(data.node_tasks_sum_per(n))

	df = pandas.DataFrame(data=d)
	fig = px.scatter(df, x="eff", y="load", trendline="ols")
	fig.show()


def cluster_populate(cl):
	entry_node = nodes[0]
	for _ in range(rounds_number):
		msg = data.generate_message(rg, message_template)
		cl = cluster.assign_message(cl, msg, entry_node)

	nodes_max_performance = data.nodes_max_per(nodes)
	nodes_max_power_consumption = data.nodes_max_eff(nodes)
	for n in nodes:
		Logging.info(__file__, "node:", n.identifier,
			"tasks count:", data.node_tasks_count(n),
			"tasks load:", data.node_tasks_sum_per(n),
			"rel. perf.", n.per / nodes_max_performance,
			"rel. pwr. consumption:", n.eff / nodes_max_power_consumption)  # Performance related to max


def print_network_table_file(filename):
	with open(filename, 'w') as f:
		csvw = csv.writer(f)
		offset = min([n.identifier for n in nodes]) - 1  # Node identifiers do not count from 1
		csvw.writerow(['Id', 'Name', 'Performance (CPU clock * N cores)', 'Thermal output, W', 'Tasks assigned', 'Tasks overall complexity', 'Neighbors'])
		csvw.writerow(['Количество узлов', 'Имя узла', 'Производительность (CPU clock * N cores)', 'Мощность, Вт', 'Количество назначенных задач', 'Общая сложность задач', 'Список соседей'])

		for node in cl.nodes:
			neighbors = ', '.join([str(n.identifier - offset) for n in cl.neighbors(node)])
			csvw.writerow([node.identifier - offset, node.name, node.per, node.eff, len(node.tasks), data.node_tasks_sum_per(node), neighbors])


if __name__ == "__main__":
	# rg, message_template = profile_load_distribution()
	rg, message_template = profile_energy_efficiency()
	rounds_number = 500
	processors_number = len(PROCESSORS)
	nodes = [data.generate_node(rg, PROCESSORS[cluster_topology[i] % processors_number]) for i in range(cluster_size)]
	cl = data.make_cluster(nodes, cluster_topology)
	Logging.debug(cl)

	cluster_populate(cl)
	plot_fit_performance()
	plot_fit_efficiency()
	plot_cluster(cl)
	print_network_table_file('cluster.csv')
