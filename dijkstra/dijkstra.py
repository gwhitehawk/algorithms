# python dijkstra.py -f <input_file> -s <source_id> -t <target_id>
# Assumes weights to be non-negative (because Dijkstra).
# Returns shortest path from source to target, or -1 if target
# unreachable from source.

import click


class Edge(object):
    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = weight

class Node(object):
    def __init__(self, label):
        self.label = label
        self.distance = -1
        self.neighbors = {}
        self.final = False

    def add_neighbor(self, neighbor, weight):
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = weight

class Graph(object):
    def __init__(self, filename):
        self.nodes = {}
        with open(filename, "r") as f:
            for line in f.readlines():
                key, dest, weight = line.strip().split(',')
                node = self.get_or_create_node(key)
                node.add_neighbor(dest, float(weight))
                target = self.get_or_create_node(dest)
                target.add_neighbor(key, float(weight))

    def get_or_create_node(self, label):
        if label not in self.nodes:
            node = Node(label)
            self.nodes[label] = node
            return node
        else:
            return self.nodes[label]

    def update(self, final):
        min_dist = -1
        next_final = None
        for v in final:
            current = self.nodes[v]
            for w, weight in current.neighbors.iteritems():
                nextv = self.nodes[w]
                if not nextv.final:
                    new_weight = current.distance + weight
                    if nextv.distance == -1 or nextv.distance > new_weight:
                        nextv.distance = new_weight
                    if min_dist < 0 or nextv.distance < min_dist:
                        min_dist = nextv.distance
                        next_final = w

        if next_final is not None:
            final.append(next_final)
            self.nodes[next_final].final = True
        return next_final is None

    def shortest_path(self, source, target):
        final = [source]
        source_v = self.nodes[source]
        source_v.distance = 0
        source_v.final = True
        end = False
        while not self.nodes[target].final and not end:
            end = self.update(final)
        return self.nodes[target].distance

@click.command()
@click.option("-f", "--filename", help="graph file name")
@click.option("-s", "--source", help="source")
@click.option("-t", "--target", help="target")
def main(filename, source, target):
    graph = Graph(filename)
    print graph.shortest_path(source, target)

if __name__ == '__main__':
    main()
