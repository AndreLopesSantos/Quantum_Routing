import networkx  as nx
import os
import re
from datetime import datetime


def write_lp_file(G,A_value,B_value):
    num_nodes = G.number_of_nodes()
    num_variables = num_nodes **2
    #now = datetime.now()
    #date_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    #filename = "nodes_"+str(num_nodes)+"_date_"+date_string+".lp"
    filename = "simple.lp"
    f = open(filename, "w")
    f.write("Minimize\n")
    f.write(" obj: x1 + 2 x2 + 3 x3 + x4\n")
    f.write("Subject To\n")
    f.write(" c1: - x1 + x2 + x3 + 10 x4 <= 20\n") #dependendo do número de nós será algo do tipo x11 + x12 + x13 + x14 = 1 e x21 + x22 + x23 + x24 = 1 , etc.
    f.write(" c2: x1 - 3 x2 + x3 <= 30\n")
    f.write(" c3: x2 - 3.5 x4 = 0\n")
    f.write("Bounds\n")
    f.write(" 0 <= x1 <= 40\n") #bounds para todos serão 0<= x1 <= 1
    f.write(" 2 <= x4 <= 3\n")
    f.write("General\n")
    f.write(" x4\n")
    f.write("End")
    f.close()


def read_sol_file(G):
    print("READING SOLUTION FILE")
    filename = "simple.sol"
    f = open(filename, "r")
    resultados = [0] * (G.number_of_nodes()+1)
    num_linha = 0
    for linha in f:
        num_linha += 1
        if num_linha == 2:
            objective_value = float(re.findall("\d+\.*\d*",linha)[0])
            resultados[0] = objective_value
            print("Objective value: " ,objective_value)
        if num_linha > 2:
            x_value = re.findall("\d+",linha)
            print("x_value: " ,x_value)
            resultados[int(x_value[0])] = int(x_value[1])

    print("Resultados:")
    print(resultados)
    return resultados        


    
    #f.readline()
    #linha = f.readline()
    
    #objective_value = float(re.findall("\d+\.\d*",linha)[0])
    #linha = f.readline
    #print(objective_value)

G = nx.Graph()
G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0)})
#write_lp_file(G)
print("Number of nodes in G: ",G.number_of_nodes() **2 )

os.system('cmd /c "scip -c "read simple.lp optimize display solution write solution simple.sol quit""')
read_sol_file(G)
