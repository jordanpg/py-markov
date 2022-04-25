import re
from typing import Union
from pymarkov import node

class Markov:
    """Markov chain text generator"""
    start_flag = "|START|"
    end_flag = "|END|"
    
    def __init__(self):
        self._nodemap: dict[str, node.Node] = {}
        # Add nodes for start and end
        self.to_node(self.start_flag)
        self.to_node(self.end_flag)

    def __len__(self):
        """Number of words known to the AI"""
        return len(self._nodemap) - 2 # Subtract 2 for start and end nodes

    def to_node(self, word: str) -> node.Node:
        """Convert a string to a refernce to a new or existing node"""
        if word not in self._nodemap:
            self._nodemap[word] = node.Node(word)
        return self._nodemap[word]

    def add_link(self, a: str, b: str):
        """Add or strengthen a word pair a->b"""
        na = self.to_node(a)
        nb = self.to_node(b)

        na.add_link(nb)
    
    def generate(self, max_len: Union[int, None] = 25, weighted = True):
        """Generate a sentence of max_len maximum length. If max_len is None, length is unlimited.
        Unlimited length may result in an infinite loop.
        
        If weighted is False, then all word links will be weighted equally.
        """
        next = self.to_node(self.start_flag)
        end = self.to_node(self.end_flag)
        
        choices: list = []
        while max_len is None or len(choices) <= max_len:
            next = next.pick_next(weighted) # Pick the next node
            # Break if we've reached the end
            if not next or next is end:
                break
            choices.append(next.value)
            
        return choices
    
    def process_text(self, msg: str):
        """Process a string, adding all links"""
        # Extract each sentence
        sentences = [s.strip() for s in re.split(r'[.!?]', msg) if len(s.strip()) > 0]
        # Extract each word, inserting the sentence start and end flags
        # Convert sentence to lowercase to avoid differentiating between Aaa, aAa, aaa, etc.
        sentence_words = [[self.start_flag, *[w for w in re.split('[ ,]',sentence.lower()) if len(w) > 0], self.end_flag] for sentence in sentences]
        # Process each sentence
        for words in sentence_words:
            # Exit if there aren't any pairs to link
            if len(words) < 2:
                return
            # Add all word pairs
            prev = words[0]
            for next in words[1:]:
                self.add_link(prev, next)
                prev = next