from graphviz import Digraph

# Crear diagrama de flujo
dot = Digraph(comment='Algoritmo Outerplanar + MIS Exacto')

# Nodos principales del sistema
dot.node('A', 'INICIO')
dot.node('B', 'Crear grafo: G = nx.Graph()')
dot.node('C', 'Agregar aristas: G.add_edges_from([...])')
dot.node('D', 'Verificar outerplanaridad:\ncheck_planarity, treewidth, K4/K2,3')
dot.node('E1', 'NO es outerplanar\n→ Terminar')
dot.node('E2', 'SI es outerplanar')
dot.node('F', 'Aplicar algoritmo exact_mis_path(G)')
dot.node('G', 'Resultado: MIS (tamaño N): sorted(mis_nodes)')
dot.node('H', 'Visualizar grafo con nodos MIS en verde')
dot.node('Z', 'FIN')

# Conexiones del flujo
dot.edge('A', 'B')
dot.edge('B', 'C')
dot.edge('C', 'D')
dot.edge('D', 'E1', label='No')
dot.edge('D', 'E2', label='Sí')
dot.edge('E2', 'F')
dot.edge('F', 'G')
dot.edge('G', 'H')
dot.edge('E1', 'Z')
dot.edge('H', 'Z')

# Guardar y renderizar el diagrama
dot.render('algoritmo_outerplanar_mis_diagrama', format='png', cleanup=False)

print("✅ Diagrama generado como 'algoritmo_outerplanar_mis_diagrama.png'")
