

import cvxpy as py
import numpy as np


# Note: cvxpy does not take 3-dimensional arrays as variables.
# The function idx solves this issue.
# In stead of writing x[u,v,j] we now write x[idx(u,v,j)]

#To see what idx does uncomment the next 4 lines :

# for u in range(n):
#     for v in range(n):
#         for j in range (k):
#             print(idx(u,v,j))

x=py.Variable((4,7),integer=True)  # binary variable

matrix = np.zeros((7,4))
matrix[0][0]=3.6
matrix[0][1]=9.6
matrix[0][2]=3.6
matrix[0][3]=16.3
matrix[1][0]=6.8
matrix[1][1]=2.4
matrix[1][2]=1.2
matrix[1][3]=10.4
matrix[2][0]=7.3
matrix[2][1]=0.7
matrix[2][2]=6.5
matrix[2][3]=14.5
matrix[3][0]=5.2
matrix[3][1]=2.2
matrix[3][2]=7.1
matrix[3][3]=14.5
matrix[4][0]=0.1
matrix[4][1]=2.3
matrix[4][2]=5.5
matrix[4][3]=7.8
matrix[5][0]=3.2
matrix[5][1]=4.9
matrix[5][2]=3.3
matrix[5][3]=11.4
matrix[6][0]=26.7
matrix[6][1]=22.1
matrix[6][2]=27.2
matrix=matrix.transpose()

constraints=[x>=0]
for i in range (0,4):
    for j in range(0,7):
        constraints+= [x[i,j] - matrix[i,j] <=1]
for i in range (0,4):
    for j in range(0,7):
        constraints+= [x[i,j] - matrix[i,j] >=-1]

for i in range (0,3):
        constraints+= [sum(x[i,j] for j in range(0,6))-x[i,6] ==0]

for j in range (0,6):
        constraints+= [sum(x[i,j] for i in range(0,3))-x[3,j] ==0]



objective = py.Minimize(0)

prob = py.Problem(objective, constraints)

prob.solve(solver=py.GLPK_MI)




print('objective =', prob.value)

xval = x.value
print xval

