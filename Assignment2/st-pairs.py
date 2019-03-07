#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Given a graph G=(V,E) and s1,t1,s2,t2 in V it finds a minimum cost subset 
of the edges such that s1 is connected with t1 and s2 is connected with t2. 
V={0,1,...,n}
 s1 is point 0
 t1 is point 1
 s2 is point n-2
 t2 is point n-1

"""

import cvxpy as py
import numpy as np
import matplotlib.pyplot as plt
#from time import time

def plot_graph(points,A):
    """
    Input: 
        List of points
        Adjacency matrix A for the points
    """
    n = len(points)
    x = []; y = []
    for i in range(n):
        x.append(points[i][0])
        y.append(points[i][1])
        plt.plot(x, y, 'co',color='r',markersize=2)
    
    for i in range(n):
        for j in range(n):
            if A[i,j]==1:
                if not(i==j):
                    plt.arrow(x[i], y[i], x[j]-x[i], y[j]-y[i],head_width = 0,linewidth=0.5,
            color = 'g', length_includes_head = False)
  
    plt.text(points[0,0],points[0,1], "s1", size=15)
    plt.text(points[1,0],points[1,1], "t1", size=15)
    plt.text(points[n-2,0],points[n-2,1], "s2", size=15)
    plt.text(points[n-1,0],points[n-1,1], "t2", size=15)
    
    #Set box slitghtly larger than the range of x and y
    plt.xlim(min(x)-0.05*(max(x)-min(x)), max(x)+0.05*(max(x)-min(x)))
    plt.ylim(min(y)-0.05*(max(y)-min(y)), max(y)+0.05*(max(y)-min(y)))

    plt.show()
    
def random_points(n):
    """Makes  a list of n random points (x,y) with 0<=x,y<=1
    """
    np.random.seed(26)
    points = np.random.random(size=(n,2))    # create random points
    return(points)


def compute_distances(points):
    """
    Output: D[i,j]=D[j,i] is the Euclidean distance between points i and j
    """
    n=len(points)
    p=points
    D = np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            D[i,j]=np.sqrt((p[i,0]-p[j,0])**2+(p[i,1]-p[j,1])**2)
            D[j,i]=D[i,j]
    return D
    
def define_edges(D,n):
    """
    Some functipon for defining a random set of the edges.
    There is an edge between points i and j if their distance is below 
    some threshold value mu
    Output: Adjacency matrix A
    """
    A=np.zeros((n,n))
    mu=0.3
    for i in range(n):
        for j in range(n):
            if D[i,j]<= mu:
                A[i,j]=1
    return A
    
    
def main():
    
    
    n = 25  #number of points
    
    points = random_points(n)   # create n random points in a 1x1 square
    
    D=compute_distances(points) #D[i,j]=D[j,i]=the distance between points i and j 
                
    A=define_edges(D,n) #adjacency matrix: A[i,j]=1 if there is an edge (i,j)
    
    plot_graph(points,A) #plot the points and edges defined by A
    
    
    x = py.Variable((n,n),boolean=True)        #x[i,j]=1 if edge (i,j) is bought
    y1 = py.Variable((n,n))   #y1[i,j] is the value of flow 1 on arc (i,j)
    y2 = py.Variable((n,n))   #y2[i,j] is the value of flow 2 on arc (i,j)

    # For old version of CVXPY:
    # x = py.Bool(n,n)  # x[i,j]=1 if edge (i,j) is bought
    # y1 = py.Variable(n, n)  # y1[i,j] is the value of flow 1 on arc (i,j)
    # y2 = py.Variable(n, n)  # y2[i,j] is the value of flow 2 on arc (i,j)

    constraints = [x>=0]
    ####################
    for i in range(n):
        constraints+= [x[i,i]==0]
    for i in range(n):
        for j in range(n):
            constraints += [x[i,j] <= A[i,j]]

    for i in range(n):
        for j in range(n):
            constraints += [x[i, j] == x[j,i]]

    constraints += [sum(y1[0, j] for j in range (n)) == 1]
    constraints += [sum(y1[i, 1] for i in range (n)) == 1]
    constraints += [sum(y2[n-2, j] for j in range(n)) == 1]
    constraints += [sum(y2[i, n-1] for i in range(n)) == 1]

    for i in range(n):
        for j in range(n):
            constraints += [y1[i, j] <= x[i, j]]
    for i in range(n):
        for j in range(n):
            constraints += [y1[i, j] == -y1[j, i]]
    for i in range(n):
        for j in range(n):
            constraints += [y2[i, j] <= x[i, j]]
    for i in range(n):
        for j in range(n):
            constraints += [y2[i, j] == -y2[j, i]]

    for i in range(2,n):
        constraints += [sum(y1[i, j] for j in range(n))-sum(y1[j, i] for j in range(n))==0]
    for i in range(0,n-2):
        constraints += [sum(y2[i, j] for j in range(n))-sum(y2[j, i] for j in range(n))==0]


    objective = py.Minimize(sum(sum(x[i,j]*D[i,j] for i in range(n))for j in range(n)))
    prob = py.Problem(objective, constraints)
    print("Solving")
    prob.solve(solver=py.GLPK_MI)
    print("Solved")
    print(prob.status)
    #####################
    try:
        if prob.status == 'optimal':
            xval=np.array(x.value)
            plot_graph(points,xval)  # the edges bought
            print('Value is',prob.value)
    except:
        print('No feasible solution found')
        
        
main()    
