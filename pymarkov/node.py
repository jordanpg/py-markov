from typing import Any, Iterable, NamedTuple

class Node:
	def __init__(self, value: Any, links: dict['Node', int] = None):
		self.value = value
		self._links = links or {}

	def add_link(self, target: 'Node') -> int:
		if target not in self._links:
			self._links[target] = 0
		self._links[target] += 1
		return self._links[target]

	@property
	def choices(self):
		return list(self._links.keys()), list(self._links.values())

	@property
	def num_links(self):
		return len(self.links)
