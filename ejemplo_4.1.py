import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo no dirigido
G = nx.Graph()

# Agregar nodos y aristas
G.add_edges_from([
    ("A", "B"),
    ("B", "C"),
    ("C", "D"),
    ("D", "A"),
    ("A", "C")  # Diagonal entre A y C
])

# Dibujar el grafo
nx.draw(G, with_labels=True, node_color="lightblue", node_size=1500, font_weight="bold")
plt.title("Ejemplo de Grafo No Dirigido")
plt.show()

