import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

def is_outerplanar(G):
    is_planar, _ = nx.check_planarity(G)
    return is_planar and not has_k4_or_k23(G)

def has_k4_or_k23(G):
    K4 = nx.complete_graph(4)
    K23 = nx.complete_bipartite_graph(2, 3)
    gm_k4 = nx.algorithms.isomorphism.GraphMatcher(G, K4)
    gm_k23 = nx.algorithms.isomorphism.GraphMatcher(G, K23)
    return gm_k4.subgraph_is_isomorphic() or gm_k23.subgraph_is_isomorphic()

def build_trivial_tree_decomposition(G):
    bags = []
    for u, v in G.edges():
        bags.append({u, v})
    return bags

def maximum_independent_set_from_bags(G, bags):
    memo = {}

    def dp(i, chosen):
        key = (i, tuple(sorted(chosen)))
        if key in memo:
            return memo[key]
        if i == len(bags):
            return 0, set()

        bag = bags[i]
        max_val, max_set = 0, set()
        for subset in powerset(bag):
            if is_independent(subset, G) and not chosen.intersection(subset):
                val, sub_set = dp(i + 1, chosen.union(subset))
                val += len(subset)
                if val > max_val:
                    max_val = val
                    max_set = subset.union(sub_set)

        memo[key] = (max_val, max_set)
        return memo[key]

    return dp(0, set())

def powerset(s):
    s = list(s)
    return [set(c) for i in range(len(s)+1) for c in product(s, repeat=i) if len(set(c)) == i]

def is_independent(subset, G):
    for u in subset:
        for v in subset:
            if u != v and G.has_edge(u, v):
                return False
    return True

def draw_graph(G, mis_nodes):
    pos = nx.spring_layout(G)
    node_colors = ['green' if node in mis_nodes else 'lightblue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_weight='bold')
    plt.show()

# 🧪 Ejemplo de uso
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3),
        (2, 3)
    ])

    if not is_outerplanar(G):
        print("El grafo no es outerplanar")
    else:
        print("El grafo es outerplanar")
        bags = build_trivial_tree_decomposition(G)
        size, mis_nodes = maximum_independent_set_from_bags(G, bags)
        print(f"MIS (tamaño {size}): {sorted(mis_nodes)}")
        draw_graph(G, mis_nodes)
