# -*- coding: utf-8 -*-
"""
    Solves a random knapsack instance 
"""

import cvxpy as cy
import numpy as np
import gurobipy
import time

np.set_printoptions(precision=3)   # print only a few decimals

np.random.seed(1)  # fix the random number generator 

n=5   # number of items

x = cy.Variable(n)  # continues variable
# x=cy.Bool(n)  # binary variable
#x=cy.Int(n)  # integer variable
a = [2,3,4,15,6]  # random weights
c = [9,12,7,6,5]  # random costs
print(a,c)
b = 21   # b is the capacity of the knapsack


### setting the constraints
constraints = [x>=0]  

constraints += [a*x<=b]

### Form objective.
obj = cy.Maximize(c*x)

### Define the problem.
prob = cy.Problem(obj, constraints)

### Solve the problem

tic = time.time()  # start timing

# prob.solve(solver=cy.GLPK)  # Solves the problem with the standard solver.

prob.solve(solver=cy.GLPK)  # uses GLPK instead of the standard solver

# prob.solve(solver=cy.GLPK_MI)  # uses GLPK_MI instead of the standard solver

toc = time.time()  # stop timing
elapsed = toc-tic


print("status:", prob.status)
print("optimal value:", prob.value)
print("optimal variables\n", x.value)
print("elapsed time:", "%.6f" % elapsed  )

