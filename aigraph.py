# AIGraph (AIG stuff with NetworkX, based on PyAIGER)
# AIGER format support
import matplotlib.pyplot as plt
import networkx as nx

class AIGraph():
    def __init__(self, G=None):
        self.G = nx.DiGraph() if G is None else G
        # keep track of nodes and their connections
        self.node_table = {}
        self.next_val = -1

    def from_aiger(self, fname):
        from AIGER.aigsim import Reader, Model
        r = Reader()
        r.openFile(fname)
        m = Model()
        r.readHeader(m)
        r.readModel(m)
        r.procModelNames(m)

        for input_obj in m.inputs:
            self.G.add_node(input_obj.lit, label=f"INP_{input_obj.lit}")
        for gate in m.ands:
            self.G.add_node(gate.lit, label=f"AND_{gate.lit}")
            self.G.add_edge((gate.rhs0) if gate.rhs0 % 2 == 0 else gate.rhs0 - 1, gate.lit, weight=int(gate.rhs0 % 2 != 0))
            self.G.add_edge((gate.rhs1) if gate.rhs1 % 2 == 0 else gate.rhs1 - 1, gate.lit, weight =int(gate.rhs1 % 2 != 0))
            # add and gate to node_table
            self.node_table[(gate.rhs0, gate.rhs1)] = gate.lit
        for output_obj in m.outputs:
            self.G.add_node((output_obj.lit) if output_obj.lit % 2 == 0 else output_obj.lit - 1, label=f"OUT_{output_obj.lit}")
        self.next_val = m.ands[-1].lit + 2

    def node_lookup(self, n1, n2):
        if (n1,n2) in self.node_table.keys(): return self.node_table[(n1,n2)]
        if(n2,n1) in self.node_table.keys(): return self.node_table[(n2,n1)]
        return -1

    def create_node(self, n1, n2):
        # create an AND gate between 
        # DOES NOT CREATE N1/N2 IF THEY DON'T EXIST
        nn = self.next_val
        self.next_val = nn + 2
        print(nn)
        if not self.G.has_node(n1) or not self.G.has_node(n2):
            print(f"WARNING: Trying to create node between non-existing fanins {n1,n2}")
            return -1
        self.G.add_node(nn, label = f"AND_{nn}")
        self.G.add_edge((n1) if n1 % 2 == 0 else n1 - 1, nn, weight=int(n1 % 2 != 0))
        self.G.add_edge((n2) if n2 % 2 == 0 else n2- 1, nn, weight =int(n2 % 2 != 0))
        self.node_table[(n1, n2)] = nn
        return nn
    def operation_and(self, n1, n2):
        # TODO: support constants?
        if n1 == n2: return n1
        if abs(n1 - n2) == 1: return 0
        res = self.node_lookup(n1, n2)
        if res != -1: 
            print(f"Node with fanins {n1,n2} already exists")
            return res
        return self.create_node(n1, n2)
    def plot(self):
        pos = nx.nx_pydot.graphviz_layout(self.G, prog='dot')
        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, labels=nx.get_node_attributes(self.G, 'label'),
                node_shape='o', node_color='lightblue', node_size=1200, arrowsize=20)

        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=labels)

def main():
    AIG = AIGraph()
    AIG.from_aiger('./input_graph.aag')
    # ts = list(nx.topological_sort(AIG.G))
    AIG.operation_and(6,2)
    AIG.operation_and(6,3)
    AIG.plot()
    plt.show()


if __name__ == '__main__':
    main()
