import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

def is_outerplanar(G):
    is_planar, _ = nx.check_planarity(G)
    return is_planar and not has_k4_or_k23(G)

def has_k4_or_k23(G):
    K4 = nx.complete_graph(4)
    K23 = nx.complete_bipartite_graph(2, 3)
    gm_k4 = nx.algorithms.isomorphism.GraphMatcher(G, K4)
    gm_k23 = nx.algorithms.isomorphism.GraphMatcher(G, K23)
    return gm_k4.subgraph_is_isomorphic() or gm_k23.subgraph_is_isomorphic()

def build_bags(G):
    bags = []
    for u in G.nodes():
        neighbors = list(G.neighbors(u))
        bag = {u} | set(neighbors[:2])  # Máximo 3 nodos por bolsa
        bags.append(bag)
    return bags

def valid_independent_sets(bag, G):
    bag = list(bag)
    valid_sets = []
    for r in range(len(bag) + 1):
        for subset in combinations(bag, r):
            if is_independent(subset, G):
                valid_sets.append(set(subset))
    return valid_sets

def maximum_independent_set(G):
    bags = build_bags(G)
    memo = {}

    def dp(i, prev_choice):
        key = (i, frozenset(prev_choice))
        if key in memo:
            return memo[key]
        if i == len(bags):
            return 0, set()

        best_size, best_set = 0, set()
        for choice in valid_independent_sets(bags[i], G):
            if not choice & prev_choice:  # No conflict with previous bag
                size, result_set = dp(i + 1, choice)
                size += len(choice)
                if size > best_size:
                    best_size = size
                    best_set = set(choice) | result_set

        memo[key] = (best_size, best_set)
        return memo[key]

    return dp(0, set())

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
        (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)
    ])

    if not is_outerplanar(G):
        print("El grafo no es outerplanar")
    else:
        print("El grafo es outerplanar")
        size, mis_nodes = maximum_independent_set(G)
        print(f"MIS (tamaño {size}): {sorted(mis_nodes)}")
        draw_graph(G, mis_nodes)
