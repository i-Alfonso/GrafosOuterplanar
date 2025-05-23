from graphviz import Digraph

dot = Digraph(comment='Detalle del Algoritmo Outerplanar + MIS')

# Nivel 1
dot.node('A', 'INICIO')

# Nivel 2
dot.node('B1', 'Construir Grafo G')
dot.node('B2', 'Agregar aristas a G')

# Nivel 3 - Outerplanaridad
dot.node('C1', 'Verificar Planaridad')
dot.node('C2', 'Calcular treewidth')
dot.node('C3', 'Detectar K4 o K2,3')

# Nivel 4 - Decisión Outerplanaridad
dot.node('D1', 'NO Outerplanar')
dot.node('D2', 'ES Outerplanar')

# Nivel 5 - Construcción Bolsas
dot.node('E1', 'Construir Bolsas de 3 nodos máx.')

# Nivel 6 - Evaluación Independencia
dot.node('F1', 'Generar subconjuntos independientes')

# Nivel 7 - Programación Dinámica
dot.node('G1', 'DP para maximizar tamaño MIS')

# Nivel 8 - Mostrar Resultados
dot.node('H1', 'Mostrar tamaño y nodos MIS')
dot.node('H2', 'FIN')

# Conexiones
dot.edges([('A', 'B1'), ('B1', 'B2'), ('B2', 'C1'), ('C1', 'C2'), ('C2', 'C3')])
dot.edge('C3', 'D1', label='Sí detecta K4/K2,3 o treewidth > 2')
dot.edge('C3', 'D2', label='No detecta K4/K2,3 y treewidth ≤ 2')
dot.edge('D1', 'H2')
dot.edge('D2', 'E1')
dot.edge('E1', 'F1')
dot.edge('F1', 'G1')
dot.edge('G1', 'H1')
dot.edge('H1', 'H2')

# Renderizar
dot.render('imagenes/detalle_algoritmo_outerplanar_mis', format='png', cleanup=False)

print("Diagrama generado como 'detalle_algoritmo_outerplanar_mis.png'")
