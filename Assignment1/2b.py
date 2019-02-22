

import cvxpy as py
import numpy as np

n = 14
v = [-3,-4,-5,-6,-8,2,3,4,-3,-4,7,8,5,5]
# Note: cvxpy does not take 3-dimensional arrays as variables.
# The function idx solves this issue.
# In stead of writing x[u,v,j] we now write x[idx(u,v,j)]

#To see what idx does uncomment the next 4 lines :

# for u in range(n):
#     for v in range(n):
#         for j in range (k):
#             print(idx(u,v,j))

x=py.Variable(n,boolean=True)  # binary variable


constraints=[x>=0]
constraints+=[x[v[11]]>=x[v[13]]]
constraints+=[x[v[10]]>=x[v[13]]]
constraints+=[x[v[10]]>=x[v[12]]]
constraints+=[x[v[9]]>=x[v[12]]]
constraints+=[x[v[8]]>=x[v[11]]]
constraints+=[x[v[7]]>=x[v[11]]]
constraints+=[x[v[7]]>=x[v[10]]]
constraints+=[x[v[6]]>=x[v[10]]]
constraints+=[x[v[6]]>=x[v[9]]]
constraints+=[x[v[5]]>=x[v[9]]]
constraints+=[x[v[4]]>=x[v[8]]]
constraints+=[x[v[3]]>=x[v[8]]]
constraints+=[x[v[3]]>=x[v[7]]]
constraints+=[x[v[2]]>=x[v[7]]]
constraints+=[x[v[2]]>=x[v[6]]]
constraints+=[x[v[1]]>=x[v[6]]]
constraints+=[x[v[1]]>=x[v[5]]]
constraints+=[x[v[0]]>=x[v[5]]]

constraints+=[x<=1]
objective = py.Maximize(sum(x[l]*l for l in v))

prob = py.Problem(objective, constraints)

prob.solve(solver=py.GLPK_MI)




print('objective =', prob.value)

xval = x.value
for l in v:
    print xval[l]

