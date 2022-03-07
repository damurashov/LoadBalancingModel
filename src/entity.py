from dataclasses import dataclass, field
from itertools import count

@dataclass
class Message:
    ttl: int  # Time-to-live

    # Scores
    per: int  # How important a node's performance is
    eff: int  # How important a node's efficiency is
    dtr: int  # How important it is to distribute load evenly
    crit: int  # How important it is to make decision now


@dataclass
class Node:
    per: int  # Performance
    eff: int  # Energy consumption (opposite to efficiency)
    tasks: list  # List of tasks
    identifier: int = field(default_factory=count().__next__)
