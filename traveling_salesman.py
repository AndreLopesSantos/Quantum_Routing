import networkx  as nx 
import dwave_networkx as dnx
import dimod
from collections import defaultdict
from dwave.system import DWaveSampler, EmbeddingComposite
import sys
import numpy as np

G = nx.Graph()
#G.add_weighted_edges_from({(0, 1, 1), (0, 2, 2), (0, 3, 3), (1, 2, 4),(1, 3, 5), (2, 3, 6)})
#G.add_weighted_edges_from({(0, 1, .5), (0, 2, .1), (0, 3, .1), (1, 2, .1),(1, 3, .1), (2, 3, .5)})
#G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0)}) #complete
#lista = dnx.traveling_salesperson_qubo(G)
G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0),(0,3,3.0),(0,4, 5.0), (1,4,2.0), (1,5,1.0), (2,4,2.0),(3,5,6.0)})

def traveling_salesman(G):

    Q = defaultdict(int)


    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    if isinstance(G, nx.classes.digraph.DiGraph):
        is_directed_graph = True
    else:
        is_directed_graph = False

    max_weight = 0

    B = 1
    listofedges = []
    for i,j in G.edges:
        if G.get_edge_data(*(i,j))['weight'] > max_weight:
            max_weight = G.get_edge_data(*(i,j))['weight']
        listofedges.append([i,j])
        
    print("max_weight: " + str(max_weight))
    print("listofedges: " + str(listofedges))

    A = num_nodes * max_weight
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
    for i in range(num_nodes**2):
        Q[(i,i)] += -1*A # -1 sum xi * A
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










    np.set_printoptions(threshold=sys.maxsize)
    testarray = np.zeros((num_nodes**2, num_nodes**2))

    for alp in Q:
        testarray[alp]=Q[alp]

    print(testarray)
    np.set_printoptions(threshold = False)
    '''
    lista = nx.to_dict_of_lists(G)
    lista2 = nx.to_edgelist(G)
    print("Dict of lists")
    print(lista)
    print(lista[0])
    print("edgelist")
    print(lista2)
    sampler = EmbeddingComposite(DWaveSampler())
    lista = dnx.traveling_salesperson(G, sampler = sampler, start=0)
    print(lista)




    Q = defaultdict(int)

    # QUBO = min(sum(xi+xj-2xixj)) + lagrange*(sum(xi)-4)^2

    #Constraint 
    #(sum(xi)-4)^2) = Sum(xi^2) + 2 Sum sum xixj - 8sum(xi) +16
    # Since xi^2 = xi
    #-7sum(xi) + 2 sum sum xixj + 16
    lagrange = 4
    for i in range(8):
        Q[(i,i)] += -7*lagrange # -7 sum xi
        for j in range(i+1,8):
            Q[(i,j)] += 2*lagrange # 2 sum sum xixj


    #Objective
    #min(sum(xi+xj-2xixj))
    for i,j in G.edges:
        Q[(i,i)] += 1 #xi
        Q[(j,j)] += 1 #xj
        Q[(i,j)] += -2 # -2xixj


    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample_qubo(Q, num_reads=10, chain_strength=10)

    print(sampleset)
    '''


traveling_salesman(G)