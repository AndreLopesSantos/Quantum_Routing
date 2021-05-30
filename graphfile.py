import math
import re
import networkx  as nx 

def eucledian_distance(x1, y1, x2, y2):
    return math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)


def file_to_list(filename):
    f = open(filename, "r")
    num_linha = 0
    start_coordinates = False
    nodes_list = []
    for linha in f:
        if start_coordinates:
            value = re.findall("\d+\.?\d*",linha)
            nodes_list.append(value)
        
        if linha == "NODE_COORD_SECTION\n":
            start_coordinates = True
    nodes_list = nodes_list[:-1]
    return nodes_list


def list_to_graph(graphlist):
    G = nx.Graph()
    
    for i in range(len(graphlist)-1):
        for j in range(i+1,len(graphlist)):
            node1_num = int(graphlist[i][0]) -1
            node2_num = int(graphlist[j][0]) -1
            x1 = int(graphlist[i][1])
            y1 = int(graphlist[i][2])
            x2 = int(graphlist[j][1])
            y2 = int(graphlist[j][2])
            distance = eucledian_distance(x1,y1,x2,y2)
            G.add_weighted_edges_from({(node1_num,node2_num,distance)})
    
    return G
    


def extract_graph(filename):
    return list_to_graph(file_to_list(filename))

extract_graph("graphs/a280.tsp")