import re
from typing import Iterable, Union
from pymarkov import node

class Markov:
    """Markov chain text generator"""
    start_flag = "|START|"
    end_flag = "|END|"
    
    def __init__(self, order: int = 1):
        self._nodemap: dict[str, node.Node] = {}
        self._ngrams: dict[tuple[str, ...], node.Node] = {}
        self.order = order
        # Add nodes for start and end
        self.to_node(self.start_flag)
        self.to_node(self.end_flag)

    def __len__(self):
        """Number of words known to the AI"""
        return len(self._nodemap) - 2 # Subtract 2 for start and end nodes

    def to_ngram(self, words: Iterable[str]):
        """Convert a collection of strings to an ngram node"""
        t = tuple(words)
        if t not in self._ngrams:
            self._ngrams[t] = node.Node(t)
        return self._ngrams[t]

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
        
    def add_transition(self, ng: Iterable[str], next: str):
        """Add or strengthen an ngram transition (a,b,...) -> w"""
        ng_node = self.to_ngram(ng)
        tg_node = self.to_node(next)
        
        ng_node.add_link(tg_node)
    
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
            
        return ' '.join(choices)
    
    def process_text(self, msg: str):
        """Process a string, adding all links"""
        # Extract each sentence
        sentences = [s.strip() for s in re.split(r'[.!?]', msg) if len(s.strip()) > 0]
        # Extract each word, inserting the sentence start and end flags
        # Convert sentence to lowercase to avoid differentiating between Aaa, aAa, aaa, etc.
        sentence_words = [[self.start_flag, *[w for w in re.split(r'[ ,]',sentence.lower()) if len(w) > 0], self.end_flag] for sentence in sentences]

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
                
    def process_text_ngram(self, msg:str):
        """Process a string using ngrams"""
        if self.order == -1:
            self.process_text(msg)
            return
        
        # Extract each word
        words = [w for w in re.split(r'[,\s]', msg.lower()) if len(w) > 0]
        # Initialize rolling ngram
        history = [None] * self.order
        # Add all transitions in text to model
        for w in words:
            self.add_link(history[-1] or self.start_flag, w) # Maintain k=1 model for fallback
            self.add_transition(history, w) # Add to k=n model
            history = history[1:] + [w] # Update history
            
    def generate_text_ngram(self, max_len: int, prompt: str = None):
        """Generate text with max_len maximum words, optionally starting with prompt"""
        if self.order == -1:
            return self.generate(max_len=max_len)
        
        choices: list[str] = []
        if prompt is not None:
            # Add our input to the beginning
            pchoices: list[str] = [w for w in re.split(r'[,\s]', prompt.lower()) if len(w) > 0]
            # print(choices)
            # Initialize history to the last k words, prepending as many Nones as necessary to reach k elements
            history = ([None] * (self.order - len(pchoices)) + pchoices)[-self.order::]
            # print(history)
        else:
            history: list[Union[str, None]] = [None] * self.order
            
        while len(choices) <= max_len:
            if tuple(history) not in self._ngrams:
                # Fall back to k=1 model if the past k tokens are a new combination
                prev = history[-1] or self.start_flag
                prev_node = self.to_node(prev)
                next = prev_node.pick_next()
            else:
                prev_node = self.to_ngram(history)
                next = prev_node.pick_next()
                # Try falling back to k=1 model
                if not next:
                    prev_node = self.to_node(history[-1] or self.start_flag)
                    next = prev_node.pick_next()
            
            # print(f"{history} -> {next.value if next else None}")
            if not next or next.value == self.end_flag:
                break
            choices.append(next.value)
            history = history[1:] + [next.value]
        
        # print(choices)
        return ' '.join(choices)
            
        