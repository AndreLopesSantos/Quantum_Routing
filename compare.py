from scip import runSCIP
from traveling_salesman import traveling_salesman
from traveling_salesman import valid_solution
import networkx  as nx
import random 
import numpy as np


#G = nx.Graph()
#G.add_weighted_edges_from({(0,1,20.0),(0,2,19.0),(1,2,2.0),(1,3, 2.0),(2,3, 15.0),(3,4, 16.0),(4,5, 19.0),(5,0,14.0),(2,5, 12.0),(0,3,13.0),(0,4, 2.0), (1,4,12.0), (1,5,11.0), (2,4,2.0),(3,5,2.0)})
#G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0),(0,3,3.0),(0,4, 5.0), (1,4,2.0), (1,5,1.0), (2,4,2.0),(3,5,6.0)})


def complete_graph_generator(number_of_nodes):
    G = nx.complete_graph(number_of_nodes)
    for i,j in G.edges:
        G[i][j]['weight'] = random.randint(1,20)

    return G

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


                


def statistical_test_quantum(G, repetitions, inspector = False):
    
    num_equal_results = 0
    scipResult = runSCIP(G)
    optimal_result_classic = scipResult.pop(0)
    non_optimal_quantum_results = []
    for a in range(repetitions):

        quantumResult = traveling_salesman(G,inspector).tolist()
        print(scipResult)
        print(quantumResult)

        num_nodes = G.number_of_nodes()
        differentResults = False

        for match in range(num_nodes**2):
            if scipResult[match] != quantumResult[match]:
                differentResults = True
                non_optimal_quantum_results.append(objective_function_result(G,quantumResult))
                break

        if differentResults:
            print("The Results were different!")
        else:
            print("The Results were the Same!")
            num_equal_results += 1
    
    print("The number of equal results between quantum and classic: " + str(num_equal_results) + "/" + str(repetitions))
    print("Optimal Result (objective function) with SCIP (classical computation): ", optimal_result_classic)
    print("Non optimal results from quantum computing (results of 0 are invalid): ")
    print(non_optimal_quantum_results)


G = complete_graph_generator(9)
statistical_test_quantum(G,1,True)