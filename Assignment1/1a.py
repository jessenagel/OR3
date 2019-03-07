

import cvxpy as py
import numpy as np

n=8
k=5
V = [[] for i in range (n)]
Vertices = [0,1,2,3,4,5,6,7]
V[0] = [1,2,3,4,7]
V[1] = [0,5,7]
V[2] = [0,3,4,5]
V[3] = [0,2,7]
V[4] = [0,2,6]
V[5] = [1,2,6]
V[6] = [4,5]
V[7] = [0,1,3]

E = [(0,1),(0,2),(0,3),(0,4),(0,7),(1,5),(1,7),(2,3),(2,4),(2,5),(3,7),(4,6),(5,6)]
wave=[[[] for i in range(n)] for i in range(n)]

wave[0][1]=[1,2,3,4]
wave[0][2]=[0,1]
wave[0][3]=[1]
wave[0][4]=[0,3]
wave[0][7]=[0,1,3]
wave[1][5]=[2]
wave[1][7]=[1,4]
wave[2][3]=[0,1,3,4]
wave[2][4]=[0,2]
wave[2][5]=[3]
wave[3][7]=[0,2,3]
wave[4][6]=[0]
wave[5][6]=[4]

for u in range(n):
    for v in range(u+1,n):
        wave[v][u]=wave[u][v]


# Note: cvxpy does not take 3-dimensional arrays as variables.
# The function idx solves this issue.
# In stead of writing x[u,v,j] we now write x[idx(u,v,j)]


def idx(u,v,j):
    """
    Converts triple coordinates into a 1-dimensional array.
    u=0..n-1, v=0..n-1, j=0..k-1
    """
    return u*n*k+ v*k + j

#To see what idx does uncomment the next 4 lines :

# for u in range(n):
#     for v in range(n):
#         for j in range (k):
#             print(idx(u,v,j))

x=py.Variable(n*n*k,boolean=True)  # binary variable, old syntax x=py.Bool(n*n*k)

Demuxer=[2,4,5,6]

constraints=[x>=0]
for e in E:
    for i in range(0,k):
        if i in wave[e[0]][e[1]]:
            w_e =1
        else:
            w_e =0
        constraints += [x[idx(e[0],e[1],i)]+ x[idx(e[1],e[0],i)] <= w_e ]

for v in Vertices:
    if v not in Demuxer:
        if v != 0 and v != 7:
            for i in range(0, k):
                constraints += [sum(x[idx(v,w,i)]-x[idx(w,v,i)] for w in V[v]) == 0]

for v in Vertices:
    if v in Demuxer:
        if v != 0 and v != 7:
            constraints += [(sum(sum((x[idx(v,w,i)] - x[idx(w,v,i)]) for w in V[v]) for i in range (0,k))) == 0]

for u in range (0,n):
    for v in range (0,n):
        if (u,v) not in E and (v,u) not in E:
            for i in range (0,k):
               constraints += [x[idx(u,v,i)] == 0]

objective = py.Maximize(sum(sum((x[idx(0,w,i)] - x[idx(w,0,i)]) for w in V[0]) for i in range (0,k)) )

prob = py.Problem(objective, constraints)

prob.solve(solver=py.GLPK_MI)


print('objective =', prob.value)

xval = x.value

for u in range(n):
   for v in range(n):
       for j in range(k):
           if xval[idx(u,v,j)]>0.5:
               print('x[%s,%s,%s]=' %(u,v,j),int(xval[idx(u,v,j)]))
