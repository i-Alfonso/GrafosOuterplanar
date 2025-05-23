import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo outerplanar simple (ciclo de 4 vértices)
G_outer = nx.Graph()
G_outer.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])

# Dibujar el grafo outerplanar
plt.figure(figsize=(6, 6))
nx.draw(G_outer, with_labels=True, node_color="lightgreen", node_size=1500, font_weight="bold")
plt.title("Ejemplo de Grafo Outerplanar (Ciclo A-B-C-D-A)")
plt.show()
