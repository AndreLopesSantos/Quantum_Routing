import networkx  as nx 
from collections import defaultdict
from dwave.system import DWaveSampler, EmbeddingComposite

G = nx.Graph()
G.add_edges_from([(0,4),(0,5),(1,2),(1,6),(2,4),(3,7),(5,6),(6,7)])

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