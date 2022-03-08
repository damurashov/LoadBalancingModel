import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))  # We need files from "src/", that's how we access them

from src.entity import Node

PROCESSORS = [
	Node(
		per=12 * 3800,
		eff=105,
		tasks=[],
		name="AMD Ryzen 9 3900X"
	),
	Node(
		per=16 * 3500,
		eff=105,
		name="AMD Ryzen 9 3950X"
	),
	Node(
		per=6 * 3600,
		eff=65,
		name="AMD Ryzen 5 3500"
	),
	Node(
		per=8 * 3000,
		eff=65,
		name="Intel Core i7-9700F"
	),
	Node(
		per=6 * 3700,
		eff=65,
		name="AMD Ryzen 5 5600X"
	),
	Node(
		per=4 * 3600,
		eff=65,
		name="Intel Core i3-10100F"
	),
	Node(
		per=6 * 2600,
		eff=65,
		name="Intel Core i5-11400F"
	),
	Node(
		per=8 * 3600,
		eff=125,
		name="Intel Core i7-11700K"
	)
]
