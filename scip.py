import networkx  as nx
import os
import re


def write_lp_file(G):
    filename = "simple.lp"
    f = open(filename, "w")
    f.write("Maximize\n")
    f.write(" obj: x1 + 2 x2 + 3 x3 + x4\n")
    f.write("Subject To\n")
    f.write(" c1: - x1 + x2 + x3 + 10 x4 <= 20\n")
    f.write(" c2: x1 - 3 x2 + x3 <= 30\n")
    f.write(" c3: x2 - 3.5 x4 = 0\n")
    f.write("Bounds\n")
    f.write(" 0 <= x1 <= 40\n")
    f.write(" 2 <= x4 <= 3\n")
    f.write("General\n")
    f.write(" x4\n")
    f.write("End")
    f.close()


def read_sol_file():
    print("READING SOLUTION FILE")
    filename = "simple.sol"
    f = open(filename, "r")
    
    for x in f:
        print("linha")
        print(x)
        print(type(x))
    
    #f.readline()
    #linha = f.readline()
    
    #objective_value = float(re.findall("\d+\.\d*",linha)[0])
    #linha = f.readline
    #print(objective_value)

#G = nx.Graph()
#G.add_weighted_edges_from({(0,1,7.0),(0,2,9.0),(1,2,10.0),(1,3, 15.0),(2,3, 11.0),(3,4, 6.0),(4,5, 9.0),(5,0,14.0),(2,5, 2.0)})
#write_lp_file(G)

#os.system('cmd /c "scip -c "read simple.lp optimize display solution write solution simple.sol quit""')
read_sol_file()

