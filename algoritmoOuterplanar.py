import networkx as nx
import matplotlib.pyplot as plt

# Verifica si un grafo es outerplanar
def is_outerplanar(G):
    is_planar, _ = nx.check_planarity(G)
    treewidth, _ = nx.approximation.treewidth_min_fill_in(G)
    return is_planar and treewidth <= 2 and not has_k4_or_k23(G)

# Detecta si contiene subgrafos K4 o K2,3
def has_k4_or_k23(G):
    K4 = nx.complete_graph(4)
    K23 = nx.complete_bipartite_graph(2, 3)
    gm_k4 = nx.algorithms.isomorphism.GraphMatcher(G, K4)
    gm_k23 = nx.algorithms.isomorphism.GraphMatcher(G, K23)
    return gm_k4.subgraph_is_isomorphic() or gm_k23.subgraph_is_isomorphic()

# Algoritmo exacto en tiempo lineal para caminos y árboles simples
def exact_mis_path(G):
    nodes = list(nx.topological_sort(nx.bfs_tree(G, list(G.nodes())[0])))
    n = len(nodes)
    if n == 0:
        return 0, set()

    dp = [0] * (n + 1)
    include = [set() for _ in range(n + 1)]
    exclude = [set() for _ in range(n + 1)]

    dp[0] = 1
    include[0].add(nodes[0])

    for i in range(1, n):
        u = nodes[i]
        # Opción 1: excluir u → dp[i-1]
        if dp[i - 1] >= dp[i - 2] + 1 if i >= 2 else 1:
            dp[i] = dp[i - 1]
            include[i] = include[i - 1].copy()
        else:
            dp[i] = (dp[i - 2] if i >= 2 else 0) + 1
            include[i] = (include[i - 2] if i >= 2 else set()).copy()
            include[i].add(u)

    return dp[n - 1], include[n - 1]

# Dibuja el grafo con el MIS resaltado
def draw_graph(G, mis_nodes):
    pos = nx.spring_layout(G)
    node_colors = ['green' if node in mis_nodes else 'lightblue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_weight='bold')
    plt.show()

# 🧪 Ejemplo de uso
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)])

    if not is_outerplanar(G):
        print("El grafo NO es outerplanar")
    else:
        print("El grafo ES outerplanar")
        mis_size, mis_nodes = exact_mis_path(G)
        print(f"MIS (tamaño {mis_size}): {sorted(mis_nodes)}")
        draw_graph(G, mis_nodes)
