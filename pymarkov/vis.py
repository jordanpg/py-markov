from pymarkov import markov
from pyvis.network import Network
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

def visualize_markov(m: markov.Markov):
    """Create visualization using pyvis"""
    net = Network(height='100%',width='100%',bgcolor='#222222',font_color='white',directed=True)
    net.force_atlas_2based()
    
    for id in m._nodemap:
        net.add_node(id)
        
    for label,node in m._nodemap.items():
        net.add_edges([(label, n.value, node[n]) for n in node._links])
        
    net.toggle_physics(True)
    net.show_buttons(filter_=['physics'])
    net.show('markov.html')
    
def mpl_viz(m: markov.Markov):
    """Create visualization using networkx (too slow :()"""
    G = nx.DiGraph()
    
    for label,node in m._nodemap.items():
        for n in node._links:
            G.add_edge(label, n.value, weight=node[n])
            
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=True)
    plt.show()