import networkx as nx
import matplotlib.pyplot as plt

# Crear el ciclo A-B-C-D-A
G_cycle = nx.Graph()
G_cycle.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])

# Resaltar el MIS {A, C}
node_colors = ["lightgreen" if n in ["A", "C"] else "lightgray" for n in G_cycle.nodes()]

plt.figure(figsize=(6, 6))
nx.draw(G_cycle, with_labels=True, node_color=node_colors, node_size=1500, font_weight="bold")
plt.title("Conjunto Independiente Máximo (MIS) Ejemplo: {A, C}")
plt.show()
