import random
from typing import Any

class Node:
    """Represents a node and its connections to other nodes"""
    def __init__(self, value: Any, links: dict['Node', int] = None):
        self.value = value
        self._links = links or {}

    def add_link(self, target: 'Node') -> int:
        """Add or strengthen a linked node"""
        if target not in self._links:
            self._links[target] = 0
        self._links[target] += 1
        return self._links[target]

    def pick_next(self, weighted=True):
        """Selects a node adjacent to this node, optionally using their weights, or None if there are no connections."""
        if self.num_links == 0:
            return None
        # Get possible links and their weights
        links, weights = self.choices
        # Select a node
        choice = random.choices(links, weights if weighted else None, k=1)
        if len(choice) == 0:
            return None

        return choice[0]
    
    def __getitem__(self, key):
        if isinstance(key, Node):
            return self._links[key] or None
        for n in self._links:
            if n.value == key:
                return self._links[n]
        return None

    @property
    def choices(self):
        """List of linked nodes and a list of their weights"""
        return list(self._links.keys()), list(self._links.values())

    @property
    def num_links(self):
        """Number of links"""
        return len(self._links)

    