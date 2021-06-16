from scip import runSCIP
import networkx  as nx 
from auxiliary import complete_graph_generator
from auxiliary import valid_solution
from auxiliary import objective_function_result
from auxiliary import read_solutions
from auxiliary import random_route
from auxiliary import best_result
from traveling_salesman import traveling_salesman
from graphfile import extract_graph
import os
import time
import re


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



def quantum_experiment(G):
    
    #SCIP solver - Best Result Possible
    scipBest_start = time.time()
    scipBest = runSCIP(G, False)
    scipBest_end = time.time()
    scipBest_time = scipBest_end - scipBest_start
    optimal_result_classic = scipBest.pop(0)

    #SCIP solver - Worst Result Possible
    scipWorst_start = time.time()
    scipWorst = runSCIP(G, True)
    scipWorst_end = time.time()
    scipWorst_time = scipWorst_end - scipWorst_start
    worst_result_classic  = scipWorst.pop(0)
    
    #Qbsolv - classical implementation
    qbSolvResult_classic_start = time.time()
    qbSolvResult_classic = traveling_salesman(G,False,True).tolist()
    qbSolvResult_classic_end = time.time()
    qbSolvResult_classic_time = qbSolvResult_classic_end - qbSolvResult_classic_start
    objfunc_classic = objective_function_result(G,qbSolvResult_classic)
    
    #QBsolv - Quantum implementation
    qbSolvResult_quantum_start = time.time()
    qbSolvResult_quantum = traveling_salesman(G,False,False).tolist()
    qbSolvResult_quantum_end = time.time()
    qbSolvResult_quantum_time = qbSolvResult_quantum_end - qbSolvResult_quantum_start
    objfunc_quantum = objective_function_result(G,qbSolvResult_quantum)
    
    #Write data to results file
    filename = "results.csv"
    num_nodes = G.number_of_nodes()
    if os.path.exists(filename):
        resultsFile = open(filename,"a")
        exp_number = sum(1 for line in open('results.csv'))
    else:
        resultsFile = open(filename,"w")
        resultsFile.write("Experiment, Number of Nodes, SCIP best, SCIP worst, QBSolv classic, QBsolv Quantum, SCIP best time, SCIP worst time, QB classic time, QB quantum time\n")
        exp_number = 1

    resultsLine = str(exp_number) + ","  + str(num_nodes) + "," + str(optimal_result_classic) + "," + str(worst_result_classic ) + "," + str(objfunc_classic) + "," + str(objfunc_quantum) + "," + str(scipBest_time) + "," + str(scipWorst_time) + "," + str(qbSolvResult_classic_time) + "," + str(qbSolvResult_quantum_time) + "\n"
    resultsFile.write(resultsLine)

def quantum_experiment_know_solutions(graphfile):

    sample_str = re.findall("[^\.]+",re.findall("[^/]+",graphfile)[-1])[0]

    #Extract the complete graph from the file
    G = extract_graph(graphfile)

    num_nodes = G.number_of_nodes()

    #Check if the given graph is a Directed Graph or not
    if isinstance(G, nx.classes.digraph.DiGraph):
        route_type = "ATSP"
    else:
        route_type = "TSP"

    #Get the best know solutions for all TSP
    best_solutions = read_solutions()
    
    #Best Known Result Possible for this specific TSP
    best_known_result = best_solutions[sample_str]

    #Result for TSP if taken a random route
    random_route_result = random_route(G)
    
    #QBsolv - classical implementation
    qbSolvResult_classic_start = time.time()
    qbSolvResult_classic = traveling_salesman(G, inspector = False, qbsolv = True, classic = True, debug = False)
    qbSolvResult_classic_end = time.time()
    qbSolvResult_classic_time = qbSolvResult_classic_end - qbSolvResult_classic_start
    objfunc_classic = best_result(G,qbSolvResult_classic)
    fulltsp_classic = objfunc_classic + G.get_edge_data(*(0,num_nodes-1))['weight'] # Result if the Travelling Salesman returned to the first node
    print("QBsolv Classic - Complete")
    
    #QBsolv - Quantum implementation
    qbSolvResult_quantum_start = time.time()
    qbSolvResult_quantum = traveling_salesman(G, inspector = False, qbsolv = True, classic = False, debug = False)
    qbSolvResult_quantum_end = time.time()
    qbSolvResult_quantum_time = qbSolvResult_quantum_end - qbSolvResult_quantum_start
    objfunc_quantum = best_result(G,qbSolvResult_quantum)
    fulltsp_quantum = objfunc_quantum + G.get_edge_data(*(0,num_nodes-1))['weight'] # Result if the Travelling Salesman returned to the first node
    
    #Write data to results file
    filename = "results_known_solutions.csv"
    num_nodes = G.number_of_nodes()
    if os.path.exists(filename):
        resultsFile = open(filename,"a")
        exp_number = sum(1 for line in open('results_known_solutions.csv'))
    else:
        resultsFile = open(filename,"w")
        resultsFile.write("Experiment, Sample, Type,  Number of Nodes, Best Know Solution, Random route Solution, QBSolv classic, QBSolv classic full TSP, QBsolv Quantum, QBSolv Quantum full TSP, QB classic time, QB Quantum time (general), QB Quantum Time (QPU), Problems\n")
        exp_number = 1

    resultsLine = str(exp_number) + ","  + sample_str + "," + route_type + "," + str(num_nodes) + "," + best_known_result + "," + str(random_route_result) + "," + str(objfunc_classic) + "," + str(fulltsp_classic) + "," + str(objfunc_quantum) + "," + str(fulltsp_quantum) + ","+ str(qbSolvResult_classic_time) + "," + str(qbSolvResult_quantum_time) + "\n"
    resultsFile.write(resultsLine)


#G = extract_graph("graphs/symmetric/burma14.tsp")
#quantum_experiment(G)
#statistical_test_quantum(G,1,False)
quantum_experiment_know_solutions("graphs/symmetric/att48.tsp")
