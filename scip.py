import networkx  as nx
import os
import re
from datetime import datetime


def write_lp_file(G,B_value):
    num_nodes = G.number_of_nodes()
    num_variables = num_nodes **2

    #Writing the objective function
    objective=" obj: "
    for i,j in G.edges:
        weight = G.get_edge_data(*(i,j))['weight']
        weight *= 2
        for b in range(num_nodes):
            objective +=  " [ " + str(weight) + " x" + str(i) + "_" + str(b+1) + " * " + "x" + str(j) + "_" + str(b+2) + " ]/2 + "
            if isinstance(G, nx.classes.digraph.DiGraph) == False:
                objective += " [ " + str(weight) + " x" + str(j) + "_" + str(b+1) + " * " + "x" + str(i) + "_" + str(b+2) + " ]/2 + "

            if b == num_nodes -2:
                break
        
    objective = objective[:-3]
    objective += "\n"

    #Writing constraints
    constraint = 1
    constraint_str = ""
    for a in range(num_nodes):
        constraint_str += " c" + str(constraint) + ": "
        for c in range(num_nodes):
            constraint_str +=  "x" + str(a) + "_" + str(c+1) + " + "

        constraint_str = constraint_str[:-3]
        constraint_str += " = 1\n"
        constraint += 1

    for n in range(num_nodes):
        constraint_str += " c" + str(constraint) + ": "
        for m in range(num_nodes):
            constraint_str +=  "x" + str(m) + "_" + str(n+1) + " + "

        constraint_str = constraint_str[:-3]
        constraint_str += " = 1\n"
        constraint += 1


    constraint_str += " c" + str(constraint) + ": "  + "x0_1 = 1\n"
    constraint += 1
    constraint_str += " c" + str(constraint) + ": "  + "x" + str(num_nodes-1) + "_" + str(num_nodes) + " = 1\n"

    #Binary Variables
    binstr = ""
    for k in range(num_nodes):
        for h in range(num_nodes):
            binstr += " x" + str(k) + "_" + str(h+1) + "\n"




    #now = datetime.now()
    #date_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    #filename = "nodes_"+str(num_nodes)+"_date_"+date_string+".lp"
    filename = "simple.lp"
    f = open(filename, "w")
    f.write("Minimize\n")
    f.write(objective)
    f.write("Subject To\n")
    f.write(constraint_str) #dependendo do número de nós será algo do tipo x11 + x12 + x13 + x14 = 1 e x21 + x22 + x23 + x24 = 1 , etc.)
    f.write("Binary\n")
    f.write(binstr)
    f.write("End")
    f.close()


def read_sol_file(G):
    print("READING SOLUTION FILE")
    filename = "simple.sol"
    f = open(filename, "r")
    number_of_nodes = G.number_of_nodes()
    resultados = [0] * ((number_of_nodes**2) + 1)
    num_linha = 0
    for linha in f:
        num_linha += 1
        if num_linha == 2:
            objective_value = float(re.findall("\d+\.*\d*",linha)[0])
            resultados[0] = objective_value
            print("Objective value: " ,objective_value)
        if num_linha > 2:
            x_value = re.findall("\d+",linha)
            if len(x_value) > 2:
                print("x_value: " ,x_value)
                local_x = int(x_value[0]) * number_of_nodes + int(x_value[1])
                resultados[local_x] = int(x_value[2])

    print("Resultados:")
    print(resultados)
    return resultados        


    
    #f.readline()
    #linha = f.readline()
    
    #objective_value = float(re.findall("\d+\.\d*",linha)[0])
    #linha = f.readline
    #print(objective_value)

G = nx.Graph()
#G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0),(0,3,3.0),(0,4, 5.0), (1,4,2.0), (1,5,1.0), (2,4,2.0),(3,5,6.0)})
G.add_weighted_edges_from({(0,1,20.0),(0,2,19.0),(1,2,2.0),(1,3, 2.0),(2,3, 15.0),(3,4, 16.0),(4,5, 19.0),(5,0,14.0),(2,5, 12.0),(0,3,13.0),(0,4, 2.0), (1,4,12.0), (1,5,11.0), (2,4,2.0),(3,5,2.0)})

def runSCIP (G):
    write_lp_file(G,1)
    os.system('cmd /c "scip -c "read simple.lp optimize display solution write solution simple.sol quit""')
    read_sol_file(G)

