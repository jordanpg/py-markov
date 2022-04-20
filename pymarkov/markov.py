from pymarkov.node import Node, Link

class Markov:
	def __init__(self):
		self._nodemap: dict[str, Node] = {}

	@property
	def words(self):
		return len(self._nodemap)

	def to_node(self, word: str) -> Node:
		if word not in self._nodemap:
			self._nodemap[word] = Node(word)
		return self._nodemap[word]

	def add_link(self, a: str, b: str) -> int:
		na = self.to_node(a)
		nb = self.to_node(b)

		