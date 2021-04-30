from scip import runSCIP
from traveling_salesman import traveling_salesman
import networkx  as nx 


G = nx.Graph()
#G.add_weighted_edges_from({(0,1,20.0),(0,2,19.0),(1,2,2.0),(1,3, 2.0),(2,3, 15.0),(3,4, 16.0),(4,5, 19.0),(5,0,14.0),(2,5, 12.0),(0,3,13.0),(0,4, 2.0), (1,4,12.0), (1,5,11.0), (2,4,2.0),(3,5,2.0)})
G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0),(0,3,3.0),(0,4, 5.0), (1,4,2.0), (1,5,1.0), (2,4,2.0),(3,5,6.0)})

def statistical_test_quantum(G, repetitions):
    
    num_equal_results = 0
    for a in range(repetitions):
        scipResult = runSCIP(G)
        scipResult.pop(0)

        quantumResult = traveling_salesman(G).tolist()
        print(scipResult)
        print(quantumResult)

        num_nodes = G.number_of_nodes()
        differentResults = False

        for match in range(num_nodes**2):
            if scipResult[match] != quantumResult[match]:
                differentResults = True
                break

        if differentResults:
            print("The Results were different!")
        else:
            print("The Results were the Same!")
            num_equal_results += 1
    
    print("The number of equal results between quantum and classic: " + str(num_equal_results) + "/" + str(repetitions))

statistical_test_quantum(G,1)