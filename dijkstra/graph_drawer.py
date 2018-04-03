import click
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import time

G = nx.Graph()
plt.ion()

def draw_graph(filename, red_edges, fig=None):
  figure = plt.figure() if fig is None else fig
  with open(filename, 'r') as source:
    edges = []
    for line in source.readlines():
      source, target, eweight = line.strip().split(',')
      edges.append((source, target, eweight))
      G.add_edge(source, target, weight=100/float(eweight))

  edge_labels = {(u,v): w for u,v,w in edges}

  with open(red_edges, 'r') as red_edge_source:
    red_edges = []
    final_targets = set()
    for line in red_edge_source.readlines():
      source, target = line.strip().split(',')
      red_edges.append((source, target))
      red_edges.append((target, source))
      final_targets.add(source)
      final_targets.add(target)
  edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
  values = ['red' if node in final_targets else 'green' for node in G.nodes()]

  pos = nx.spring_layout(G, weight='weight', random_state=1)
  nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                         node_color = values, node_size = 200)
  nx.draw_networkx_labels(G, pos)
  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
  nx.draw(G, pos, node_color=values, node_size=200, edge_color=edge_colors, edge_cmap=plt.cm.Reds)
  figure.canvas.draw()
  #pylab.show()


@click.command()
@click.option('-f', '--filename', help='graph file name')
@click.option('--red_edges', help='list of red edges')
def main(filename, red_edges):
  draw_region(filename, red_edges)


if __name__ == '__main__':
  main()
