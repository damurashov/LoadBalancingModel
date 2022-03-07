import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))  # We need files from "src/", that's how we access them

from ahpy.ahpy.ahpy import Graph, to_pairwise
from src import entity


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
    all_tasks = 0
    for node in all_nodes:
        for task in node.tasks:
            all_tasks += task.per
    graph.set_weights("dtr", to_pairwise({str(node.identifier): all_tasks / sum([task.per for task in node.tasks]) if len(node.tasks) else 1 for node in all_nodes}))

    graph.set_weights("crit", to_pairwise({str(node.identifier): msg.ttl + 1 if node.identifier == decision_making_node.identifier else msg.ttl for node in all_nodes}))

    print(graph.get_weights())

