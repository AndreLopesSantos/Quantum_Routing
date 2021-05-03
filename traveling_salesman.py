import networkx  as nx 
import dwave_networkx as dnx
import dimod
from collections import defaultdict
from dwave.system import DWaveSampler, EmbeddingComposite
import sys
import numpy as np
import dwave.inspector
import math
import random

#G = nx.Graph()
#lista = dnx.traveling_salesperson_qubo(G)
#G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0),(0,3,3.0),(0,4, 5.0), (1,4,2.0), (1,5,1.0), (2,4,2.0),(3,5,6.0)})
#G.add_weighted_edges_from({(0,1,20.0),(0,2,19.0),(1,2,2.0),(1,3, 2.0),(2,3, 15.0),(3,4, 16.0),(4,5, 19.0),(5,0,14.0),(2,5, 12.0),(0,3,13.0),(0,4, 2.0), (1,4,12.0), (1,5,11.0), (2,4,2.0),(3,5,2.0)})


#resultado_teste = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1])




   
#print(G.edges())


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
    if len(node_list) != num_nodes or len(position_list) != num_nodes:
        return False
    
    return True

#valid_solution(resultado_teste)

def traveling_salesman(G):

    Q = defaultdict(int)


    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    reads = 500

    if isinstance(G, nx.classes.digraph.DiGraph):
        is_directed_graph = True
    else:
        is_directed_graph = False

    max_weight = 0
    min_weight = 10000

    listofedges = []
    for i,j in G.edges:
        if G.get_edge_data(*(i,j))['weight'] > max_weight:
            max_weight = G.get_edge_data(*(i,j))['weight']
        elif G.get_edge_data(*(i,j))['weight'] < min_weight:
            min_weight = G.get_edge_data(*(i,j))['weight']
        listofedges.append([i,j])
        
    print("max_weight: " + str(max_weight))
    print("listofedges: " + str(listofedges))

    
    B = num_nodes * min_weight
    A = num_nodes * max_weight * 6
    
    '''
    B = 1
    A = num_nodes * max_weight 
    '''
    bias = A
    '''
    Ha = A sumi(1- sumj(Xij))^2 + A sumj(1-sumi(xij)) + A sumsumXujXij+1

    Hb = B sum Wui SumXujXij+1

    H = Ha + Hb
    '''
    #print(G.get_edge_data(0,1))
    # QUBO = min(sum(xi+xj-2xixj)) + lagrange*(sum(xi)-4)^2

    #Constraint 
    #(sum(xi)-4)^2) = Sum(xi^2) + 2 Sum sum xixj - 8sum(xi) +16
    # Since xi^2 = xi
    #-7sum(xi) + 2 sum sum xixj + 16

    #penalty = 3 * A
    #worsePenalty = 5 * A
    for i in range(num_nodes**2):
        Q[(i,i)] += -A
        if i < num_nodes: #Stops the first node from being in any place than first
            Q[(i,i)] = 2 * A
        if i >= num_nodes and i % num_nodes == 0: #Stops the intermediate nodes from being the first or the last
            Q[(i,i)] =  2 * A
            Q[(i-1,i-1)] = 2 * A 
        if i // num_nodes == num_nodes-1: #Stops the last node from being any node other than last
            Q[(i,i)] = 2 * A 
        for j in range(i+1,num_nodes**2):
            first_node = i // num_nodes
            second_node = j // num_nodes
            if first_node == second_node: #all instances of the same node
                Q[(i,j)] += 2 * A 
            elif ((j-i) % num_nodes) == 0:
                Q[(i,j)] += 2 * A 
                if is_directed_graph== True:
                    if [first_node,second_node] in listofedges:
                        if j % num_nodes != 0:
                            Q[(i-1,j)] += G.get_edge_data(*(first_node,second_node))['weight'] * B
                        else:
                            Q[(i+(num_nodes-1),j)] += G.get_edge_data(*(first_node,second_node))['weight'] * B
                else:
                    if [first_node,second_node] in listofedges or [second_node,first_node] in listofedges:
                        if j % num_nodes != 0:
                            Q[(i-1,j)] += G.get_edge_data(*(first_node,second_node))['weight'] * B
                            Q[(i,j-1)] += G.get_edge_data(*(first_node,second_node))['weight'] * B
                        else:
                            Q[(i+(num_nodes-1),j)] += G.get_edge_data(*(first_node,second_node))['weight'] * B
                            Q[(i,j+(num_nodes-1))] += G.get_edge_data(*(first_node,second_node))['weight'] * B
    
    
    #First node is always the first one in the cycle
    Q[(0,0)] = -bias
    
    #Last node is always the last one in the cycle
    Q[(i,j)] = -bias


    QuantumRun = True #Temporary value for wether to run on the quantum computer or not (instead of commenting/uncommenting code)
    inspector_on = True

    chain = int((A * 5) // 1000 * 1000)





    np.set_printoptions(threshold=sys.maxsize)
    testarray = np.zeros((num_nodes**2, num_nodes**2))

    for alp in Q:
        testarray[alp]=Q[alp]

    print(testarray)

    filename = "QuboMatrix.txt"
    f = open(filename, "w")
    for linha in testarray:
        for elemento in linha:
            f.write(str(elemento) + " , ")
        f.write("\n")

    if QuantumRun == True:
        sampler = EmbeddingComposite(DWaveSampler())
        sampleset = sampler.sample_qubo(Q, num_reads=reads, chain_strength=3000)

        print(sampleset)
        ResultFile = "DwaveResult.txt"
        fi = open(ResultFile, "w")
        fi.write(str(sampleset.record))
        if inspector_on == True:
            dwave.inspector.show(sampleset)
        #Making the results easily readable
        for line in range(10):
            linestr = "LINE NUMBER:" + str(line)
            print(linestr)
            fi.write("\n" + linestr + "\n")
            resultArray = sampleset.record[line][0]
            for variavel in range(len(resultArray)):
                if resultArray[variavel] == 1:
                    xstr = "X" + str(variavel // num_nodes) + "_" + str((variavel % num_nodes) +1) + " = 1"
                    print(xstr)
                    fi.write(xstr + "\n")

        resultfound = False
        for results_iterator in range(reads):
            if valid_solution(sampleset.record[results_iterator][0]):
                resultlinestr = "Result Line: " + str(results_iterator)
                print(resultlinestr)
                bestResult = sampleset.record[results_iterator][0]
                resultfound = True
                break



    if resultfound:    
        print(bestResult)
        print("A: ", A)
        print("B: ", B)
        print("Chain: ",chain)
        np.set_printoptions(threshold = False)
        return bestResult
    else:
        print("A: ", A)
        print("B: ", B)
        print("Chain: ",chain) 
        print("No Valid Result was found")
        np.set_printoptions(threshold = False)
        return 0


def complete_graph_generator(number_of_nodes):
    G = nx.complete_graph(number_of_nodes)
    for i,j in G.edges:
        G[i][j]['weight'] = random.randint(1,20)

    return G

G = complete_graph_generator(9)
traveling_salesman(G)