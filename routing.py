import networkx  as nx 
import dwave_networkx as dnx
import dimod
from collections import defaultdict
from dwave.system import DWaveSampler, EmbeddingComposite

G = nx.Graph()
G.add_weighted_edges_from([(0,1,7),(0,2,9),(1,2,10),(1,3, 15),(2,3, 11),(3,4, 6),(4,5, 9),(5,0,14),(2,5, 2)])
dnx.traveling_salesperson(G, dimod.ExactSolver(), start=0)

'''
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