```python
def balance(AIG: AIGraph) -> AIGraph:
    uninvert = lambda x: x if x % 2 == 0 else x + 1
    OUT_AIG = AIGraph()
    depth = {}
    processed_nodes_map = {}
    node_fanins = dict(reversed(i) for i in AIG.node_table.items())
    for i in AIG.PI:
        OUT_AIG.create_pi(i)
        # kinda like a keep track of thing
        processed_nodes_map[i] = i
        depth[i] = 0
    
    for x in AIG.topo_ordering():
        if x in AIG.PI: continue
        a,b = node_fanins[x]
        inv_a = a % 2 != 0
        inv_b = b % 2 != 0
        a = processed_nodes_map[a + 1] if inv_a else processed_nodes_map[a]
        b = processed_nodes_map[b + 1] if inv_b else processed_nodes_map[b]

        leaves = []
        def gather_leaves(curr_node, inverted):
            if curr_node not in OUT_AIG.PI and curr_node not in OUT_AIG.PO:
                # print('node fanins: ', node_fanins)
                gather_leaves(node_fanins[curr_node][0], inverted ^ (node_fanins[curr_node][0] % 2 != 0))
                gather_leaves(node_fanins[curr_node][1], inverted ^ (node_fanins[curr_node][1] % 2 != 0))

            else:
                leaves.append((curr_node, inverted))

        gather_leaves(a, inv_a)
        gather_leaves(b, inv_b)
        leaves.sort(key=lambda p: depth[uninvert(p[0])])
        while len(leaves) > 1:
            n1, inv1 = leaves.pop(0)
            n2, inv2 = leaves.pop(0)
            # perform inversions
            n1 = n1 if ~inv1 else AIG.invert(n1)
            n2 = n2 if ~inv2 else AIG.invert(n2)

            andg = OUT_AIG.operation_and(n1, n2)
            depth[andg] = max(depth[uninvert(n1)], depth[uninvert(n2)]) + 1
            leaves.append((andg, False))
            leaves.sort(key=lambda p: depth[uninvert(p[0])])

        node, flag = leaves[0]
        if flag: node = AIG.invert(node)
        processed_nodes_map[node] = x
        depth[node] = depth.get(node, 0)

    print(processed_nodes_map)
    return OUT_AIG
    ```