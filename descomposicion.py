import networkx as nx
from networkx.algorithms.approximation import treewidth_min_fill_in
from itertools import chain, combinations


def is_outerplanar(G):
    is_planar, _ = nx.check_planarity(G)
    treewidth, _ = treewidth_min_fill_in(G.copy())
    return is_planar and treewidth <= 2


def build_tree_decomposition(G_original):
    G = G_original.copy()
    treewidth, td = treewidth_min_fill_in(G)

    # 🛑 Detectamos si 'td' ya es un grafo con bolsas
    if isinstance(td, nx.Graph) and all('bag' in td.nodes[n] for n in td.nodes):
        return td  # es una descomposición válida

    # 🚧 Si no lo es, lo construimos manualmente (como en versiones viejas)
    T = nx.Graph()
    for i, v in enumerate(td):  # asumimos que 'td' es orden de eliminación
        if not G.has_node(v):
            continue
        neighbors = list(G.neighbors(v))
        bag = set(neighbors + [v])
        T.add_node(i, bag=bag)
        for j in range(i - 1, -1, -1):
            if j in T.nodes and not bag.isdisjoint(T.nodes[j]['bag']):
                T.add_edge(i, j)
                break
        G.remove_node(v)
    return T


def mis_tree_decomposition(G):
    T = build_tree_decomposition(G)

    if len(T.nodes) == 0:
        raise ValueError("Error: descomposición vacía.")

    def powerset(s):
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    dp = {}

    def solve(bag, parent):
        bag_nodes = T.nodes[bag]['bag']
        children = [v for v in T.neighbors(bag) if v != parent]
        results = {}

        for subset in powerset(bag_nodes):
            subset_set = set(subset)
            if any(G.has_edge(u, v) for u in subset_set for v in subset_set if u != v):
                continue
            total = len(subset_set)
            valid = True

            for child in children:
                child_result = solve(child, bag)
                best = float('-inf')
                for child_subset, child_value in child_result.items():
                    if subset_set.isdisjoint(child_subset):
                        best = max(best, child_value)
                if best == float('-inf'):
                    valid = False
                    break
                total += best

            if valid:
                results[frozenset(subset_set)] = total

        dp[bag] = results
        return results

    root = list(T.nodes)[0]
    result = solve(root, None)
    best_set = max(result.items(), key=lambda x: x[1])[0]
    return len(best_set), set(best_set)


# -----------------------
# 🧪 PRUEBA
# -----------------------
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # ciclo
        (5, 1), (5, 3)
    ])

    print("Nodos:", list(G.nodes))
    print("¿Outerplanar?:", is_outerplanar(G))

    if is_outerplanar(G):
        size, mis = mis_tree_decomposition(G)
        print(f"MIS tamaño: {size}")
        print(f"Nodos en el MIS: {sorted(mis)}")
    else:
        print("El grafo NO es outerplanar.")
