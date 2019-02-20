

import cvxpy as py


n=8
k=5


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

for u in range(n):
    for v in range(n):
        for j in range (k):
            print(idx(u,v,j))




x=py.Variable(n*n*k,boolean=True)  # binary variable

Demuxer=[2,4,5,6]

constraints=[x>=0]
for
for v in range (1,7):
    for i in range (0,k):
        if v not in Demuxer:
            constraints += [sum(x[idx(v,w,i)]-x[idx(w,v,i)] for w in range (0,8))]

for v in range (1,7):
    if v in Demuxer:
        constraints += [sum(sum(x[idx(v,w,i)]-x[idx(w,v,i)] for w in range (0,8)) for i in (0,k))]



# objective = py.Maximize( sum(sum(x[i] for i in )) )

#prob = py.Problem(objective, constraints)
#
#prob.solve(solver=py.GLPK_MI)


#
#
#print('objective =', prob.value)
#
#xval = x.value
#
#for u in range(n):
#    for v in range(n):
#        for j in range(k):
#            if xval[idx(u,v,j)]>0.5:
#                print('x[%s,%s,%s]=' %(u,v,j),int(xval[idx(u,v,j)]))
