import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_edges_from([(0,1, {'weight': 7}),(0,2, {'weight': 9}),(1,2, {'weight': 10}),(1,3, {'weight': 15}),(2,3, {'weight': 11}),(3,4, {'weight': 6}),(4,5, {'weight': 9}),(5,0, {'weight': 14}),(2,5, {'weight': 2})])

#G = nx.petersen_graph()
plt.subplot(121)

nx.draw(G, with_labels = True , font_weight='bold')

plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()

print(nx.shortest_path(G,source=0,target=4, weight='weight'))