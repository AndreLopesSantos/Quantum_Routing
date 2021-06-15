import numpy as np
import networkx  as nx
import random
import math
import re


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

def objective_function_result(G,result):
    num_nodes = G.number_of_nodes()
    sorted_nodes = np.zeros(num_nodes)
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

def best_result(G,response):
    best_result = float('inf')
    best_solution =  response.record[0][0]
    for i in range(len(response)):
        result = objective_function_result(G, response.record[i][0])
        if result < best_result and result != 0:
            best_solution = response.record[i][0]
            best_result = result
    return best_result


def random_route(G,total_tsp = True):
    total_weight = 0
    num_edges = G.number_of_edges()
    num_nodes = G.number_of_nodes()
    for i,j in G.edges:
        total_weight += G.get_edge_data(*(i,j))['weight']
        average_weight = total_weight/num_edges
    if total_tsp == True:
        route_total = average_weight * num_nodes
    else:
        route_total = average_weight * (num_nodes-1)
    return route_total

def read_solutions():
    filename= "tsp_solutions.txt"
    f = open(filename, "r")
    solutions = dict()
    for line in f:
        value = re.findall("\w+",line)
        solutions[value[0]] = value[1]
    return solutions

  
#G = nx.Graph()
#G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0),(0,3,3.0),(0,4, 5.0), (1,4,2.0), (1,5,1.0), (2,4,2.0),(3,5,6.0)})
#random_route(G,  True)
#read_solutions()