# AIGraph (AIG stuff with NetworkX, based on PyAIGER)
# AIGER format support
import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass

# TODO: Move off of networkx and into a custom edgelist structure (C++)
@dataclass(frozen=True)
class AIGraphNode():
    lit: int
    inverted: bool = False


class AIGraph():
    def __init__(self, G=None):
        self.G = nx.DiGraph() if G is None else G
        # keep track of nodes and their connections
        self.PI = set()
        self.PO = set()
        self.nodes = set()
        self.node_table = {}
        self.next_val = 2
    def from_aiger(self, fname):
        from AIGER.aigsim import Reader, Model
        r = Reader()
        r.openFile(fname)
        m = Model()
        r.readHeader(m)
        r.readModel(m)
        r.procModelNames(m)
        for input_obj in m.inputs:
            self.PI.add(AIGraphNode(input_obj.lit))
            self.G.add_node(input_obj.lit, label=f"INP_{input_obj.lit}")
        for gate in m.ands:
            self.G.add_node(gate.lit, label=f"AND_{gate.lit}")
            self.nodes.add(AIGraphNode(gate.lit))
            self.G.add_edge((gate.rhs0) if gate.rhs0 % 2 == 0 else gate.rhs0 - 1, gate.lit, weight=int(gate.rhs0 % 2 != 0))
            self.G.add_edge((gate.rhs1) if gate.rhs1 % 2 == 0 else gate.rhs1 - 1, gate.lit, weight =int(gate.rhs1 % 2 != 0))
            # add and gate to node_table
            rhs0 = AIGraphNode(gate.rhs0) if gate.rhs0 % 2 == 0 else AIGraphNode(gate.rhs0-1, inverted=True)
            rhs1 = AIGraphNode(gate.rhs1) if gate.rhs1 % 2 == 0 else AIGraphNode(gate.rhs1-1, inverted=True)
            self.node_table[(rhs0, rhs1)] = AIGraphNode(gate.lit)
        for output_obj in m.outputs:
            self.PO.add(AIGraphNode(output_obj.lit) if output_obj.lit % 2 == 0 else AIGraphNode(output_obj.lit-1, inverted=True))
            self.G.add_node((output_obj.lit) if output_obj.lit % 2 == 0 else output_obj.lit - 1, label=f"OUT_{output_obj.lit}")
        self.next_val = m.ands[-1].lit + 2
    def topo_ordering(self):
        return list(nx.topological_sort(self.G))
    def node_lookup(self, n1, n2):
        if (n1,n2) in self.node_table.keys(): return self.node_table[(n1,n2)]
        if(n2,n1) in self.node_table.keys(): return self.node_table[(n2,n1)]
        return -1
    def create_pi(self, pi1):
        self.PI.add(pi1)
        self.next_val += 2
        self.G.add_node(pi1.lit, label=f"INP_{pi1.lit}")
    def create_po(self, node):
        self.PO.add(node)
        self.G.add_node(node.lit, label=f"OUT_{node.lit}")
    def create_node(self, n1, n2):
        # create an AND gate between 
        # DOES NOT CREATE N1/N2 IF THEY DON'T EXIST
        nn = self.next_val
        self.next_val = nn + 2
        # TODO: add ability to create node between complemented inputs
        if not self.G.has_node(n1.lit) or not self.G.has_node(n2.lit):
        # if not n1 in self.nodes or not n2 in self.nodes:
            print(f"WARNING: Trying to create node between non-existing fanins {n1,n2}")
            return -1
        self.G.add_node(nn, label = f"AND_{nn}")
        self.G.add_edge(n1.lit, nn, weight=int(n1.inverted))
        self.G.add_edge(n2.lit, nn, weight=int(n2.inverted))
        self.node_table[(n1, n2)] = AIGraphNode(nn)
        return AIGraphNode(nn)
    @staticmethod
    def invert(n1):
        return AIGraphNode(n1.lit, inverted=~n1.inverted)

    def operation_and(self, n1, n2):
        if n1 == n2: return n1
        if n1.lit == n2.lit and n1.inverted != n2.inverted: return 0
        res = self.node_lookup(n1, n2)
        if res != -1: 
            print(f"NOTE: Node with fanins {n1,n2} already exists")
            return res
        return self.create_node(n1, n2)
    def plot(self):
        pos = nx.nx_pydot.graphviz_layout(self.G, prog='dot')
        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, labels=nx.get_node_attributes(self.G, 'label'), node_shape='o', node_color='lightblue', node_size=1200, arrowsize=20)
        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=labels)


def main():
    AIG1 = AIGraph()
    AIG1.from_aiger('./input_graph.aag')
    print(AIG1.operation_and(AIGraphNode(112, inverted=True), AIGraphNode(150)))
    print(AIG1.operation_and(AIGraphNode(4, inverted=True), AIGraphNode(112, inverted=False)))
    print(AIG1.operation_and(AIGraphNode(154), AIGraphNode(156)))
    AIG1.create_po(AIGraphNode(158))
    # print(AIG1.operation_and(AIGraphNode(112, inverted=True), AIGraphNode(150)))
    # # AIG1.operation_and(AIGraphNode())
    AIG1.plot()
    # plt.show()
    plt.show()


if __name__ == '__main__':
    main()
