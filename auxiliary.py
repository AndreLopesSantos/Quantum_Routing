import numpy as np
import networkx  as nx
import random
import math 


def complete_graph_generator(number_of_nodes):
    G = nx.complete_graph(number_of_nodes)
    for i,j in G.edges:
        G[i][j]['weight'] = random.randint(1,20)

    return G


def valid_solution(result):
    node_list = []
    position_list = []
    num_nodes = math.sqrt(len(result))
    for numero in range(len(result)):
                if result[numero] == 1:
                    num_no = numero // num_nodes
                    num_pos = (numero % num_nodes) +1
                    if num_no in node_list or  num_pos in position_list:
                        return False
                    else:
                        node_list.append(num_no)
                        position_list.append(num_pos)
    if len(node_list) != num_nodes or len(position_list) != num_nodes or result[0] != 1 or result[len(result)-1] != 1:
        return False
    
    return True

def objective_function_result(G, result):
    num_nodes = G.number_of_nodes()
    sorted_nodes = np.zeros(G.number_of_nodes())
    resultado_final = 0
    if valid_solution(result):
        for numero in range(len(result)):
                if result[numero] == 1:
                    num_no = numero // num_nodes
                    num_pos = (numero % num_nodes) +1
                    sorted_nodes[num_pos-1] = num_no
    else:
        return 0
    
    for no in range(len(sorted_nodes)-1):
        i = sorted_nodes[no]
        j = sorted_nodes[no+1]
        resultado_final += G.get_edge_data(*(i,j))['weight']

    
    
    return resultado_final