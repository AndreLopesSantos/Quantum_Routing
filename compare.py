from scip import runSCIP
from auxiliary import complete_graph_generator
from auxiliary import valid_solution
from auxiliary import objective_function_result
from traveling_salesman import traveling_salesman
import os
import time

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


G = complete_graph_generator(15)
quantum_experiment(G)
#statistical_test_quantum(G,1,False)