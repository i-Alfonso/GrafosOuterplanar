import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, chain

# -----------------------------------------
# Utilidades
# -----------------------------------------

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def is_independent(G, subset):
    return all(not G.has_edge(u, v) for u, v in combinations(subset, 2))

# -----------------------------------------
# Heurística de orden de eliminación
# -----------------------------------------

def min_degree_ordering(G):
    """Orden de eliminación basado en el nodo de menor grado."""
    G = G.copy()
    order = []
    while G.nodes:
        u = min(G.nodes, key=lambda x: G.degree[x])
        order.append(u)
        G.remove_node(u)
    return order

# -----------------------------------------
# Construcción de tree decomposition
# -----------------------------------------

def tree_decomposition_from_order(G, order):
    H = G.copy()
    tree = nx.Graph()
    bags = []

    for node in order:
        neighbors = list(H.neighbors(node))
        bag = set(neighbors + [node])
        bags.append((node, bag))
        for u in neighbors:
            for v in neighbors:
                if u != v:
                    H.add_edge(u, v)
        H.remove_node(node)

    for i in range(len(bags) - 1):
        tree.add_edge(bags[i][0], bags[i + 1][0])
    for node, bag in bags:
        tree.add_node(node, bag=bag)
    return tree

# -----------------------------------------
# Algoritmo DP para MIS en outerplanar
# -----------------------------------------

def maximum_independent_set_outerplanar(G):
    order = min_degree_ordering(G)
    tree = tree_decomposition_from_order(G, order)

    root = list(tree.nodes())[0]
    parent = {root: None}
    postorder = []

    def dfs(u):
        for v in tree.neighbors(u):
            if v != parent[u]:
                parent[v] = u
                dfs(v)
        postorder.append(u)

    dfs(root)

    dp = {}
    back = {}

    for node in postorder:
        bag = tree.nodes[node]['bag']
        dp[node] = {}
        back[node] = {}

        for subset in powerset(bag):
            if not is_independent(G, subset):
                continue
            subset = frozenset(subset)
            total = len(subset)
            choice = {}

            for child in tree.neighbors(node):
                if child == parent[node]:
                    continue
                best_val, best_child = -1, None
                for child_set, val in dp[child].items():
                    if not set(subset) & set(child_set):
                        if val > best_val:
                            best_val = val
                            best_child = child_set
                if best_child is None:
                    break
                total += best_val
                choice[child] = best_child
            else:
                dp[node][subset] = total
                back[node][subset] = choice

    best_set = max(dp[root], key=lambda x: dp[root][x])
    max_size = dp[root][best_set]

    result = set()
    def reconstruct(node, subset):
        result.update(subset)
        for child in tree.neighbors(node):
            if child == parent[node]:
                continue
            child_set = back[node][subset][child]
            reconstruct(child, child_set)

    reconstruct(root, best_set)
    return max_size, result

# -----------------------------------------
# Visualización
# -----------------------------------------

def draw_graph(G, mis_nodes):
    pos = nx.spring_layout(G)
    colors = ['green' if node in mis_nodes else 'lightblue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, font_weight='bold')
    plt.title("Maximum Independent Set (MIS)")
    plt.show()

# -----------------------------------------
# Ejemplo de uso
# -----------------------------------------

if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5)
    ])

    # Verificación práctica: planaridad + ancho de árbol aproximado
    is_planar, _ = nx.check_planarity(G)
    tw, _ = nx.approximation.treewidth_min_fill_in(G)

    if is_planar and tw <= 2:
        print("✅ El grafo ES outerplanar")
        size, mis = maximum_independent_set_outerplanar(G)
        print(f"MIS (tamaño {size}): {sorted(mis)}")
        draw_graph(G, mis)
    else:
        print("❌ El grafo NO es outerplanar")