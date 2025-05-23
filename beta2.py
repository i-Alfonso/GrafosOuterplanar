import networkx as nx
from itertools import combinations, chain
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.treewidth import treewidth_min_fill_in, tree_decomposition

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def is_independent_set(G, nodes):
    return all(not G.has_edge(u, v) for u, v in combinations(nodes, 2))

def build_tree_decomposition(G):
    _, elim_order = treewidth_min_fill_in(G)
    tree_decomp = tree_decomposition(G, elim_order)
    return tree_decomp

def mis_tree_decomposition(G):
    tree_decomp = build_tree_decomposition(G)
    tree = nx.Graph()

    for u, v in tree_decomp.edges():
        tree.add_edge(u, v)

    root = list(tree_decomp.nodes())[0]
    parent = {root: None}
    order = []

    def dfs(u):
        for v in tree.neighbors(u):
            if v == parent[u]:
                continue
            parent[v] = u
            dfs(v)
        order.append(u)

    dfs(root)

    dp = {}

    for node in order:
        bag = tree_decomp.nodes[node]['bag']
        dp[node] = {}

        for subset in powerset(bag):
            if not is_independent_set(G, subset):
                continue
            subset_set = frozenset(subset)
            score = len(subset)
            valid = True

            for child in tree.neighbors(node):
                if child == parent[node]:
                    continue
                max_child = float('-inf')
                for child_set, child_val in dp[child].items():
                    if set(subset) & set(child_set):
                        continue
                    max_child = max(max_child, child_val)
                if max_child == float('-inf'):
                    valid = False
                    break
                score += max_child

            if valid:
                dp[node][subset_set] = score

    best_set = max(dp[root], key=lambda x: dp[root][x])
    max_score = dp[root][best_set]
    return max_score, set(best_set)

# 🧪 Ejemplo de uso
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
        (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)
    ])

    is_planar, _ = nx.check_planarity(G)
    if not is_planar:
        print("El grafo NO es planar (luego tampoco outerplanar)")
    else:
        print("El grafo es planar (posible outerplanar)")
        mis_size, mis_nodes = mis_tree_decomposition(G)
        print(f"MIS (tamaño {mis_size}): {sorted(mis_nodes)}")

        pos = nx.spring_layout(G)
        colors = ['green' if node in mis_nodes else 'lightblue' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, font_weight='bold')
        plt.title("Maximum Independent Set (MIS)")
        plt.show()