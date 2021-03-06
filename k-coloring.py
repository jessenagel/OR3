# -*- coding: utf-8 -*-

"""
    Find a maximum independent set of vertices in a graph. 
"""

import cvxpy as cy
#import numpy as np


n=10
vertices = range(n)
edges = [(0,1),(0,4),(0,5),(1,6),(1,2),(2,3),(2,7),(3,4),(3,8),(4,9),(5,7),(5,8),(6,8),(6,9),(7,9)]    # a cycle on 5 vertices


x=cy.Variable(n,boolean=True)  # continues variable
# x=cy.Bool(n)  # binary variable
#x=cy.Int(n)  # integer variable


# setting the constraints
constraints = [x>=0]  

for e in edges:
	constraints += [x[e[0]] + x[e[1]] <= 1]
  
    
# Form objective.
obj = cy.Maximize( sum(x[v] for v in vertices) )

# Form and solve problem.
prob = cy.Problem(obj, constraints)

#prob.solve()  # standard solver.
#prob.solve(solver=cy.GLPK)  # uses GLPK instead of the standard solver
prob.solve(solver=cy.GLPK_MI)  # uses GLPK_MI instead of the standard solver

print ("status:", prob.status)
print ("optimal value = ", prob.value)

print ("optimal var = \n", x.value)
print ('\n')

for v in vertices:    
	if x[v].value==1: 
		print( "Vertex %s is in the independent set." %(v+1))



