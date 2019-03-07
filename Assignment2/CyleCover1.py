
import cvxpy as cy
import numpy as np
import matplotlib.pyplot as plt


def plot_solution(points,A):
    """
    Plots the solution
    points:  an nx2 array of floats
    A: Adjacency matrix   A[i,j]=1 means an arc from i to j.
    Green  arrow:  A[i,j]=1
    Red arrow: A[i,j]=0.5
    No arrow otherwise. 
    """
    n=len(points)
  
    x = []; y = []
    for i in range(n):
        x.append(points[i][0])
        y.append(points[i][1])
    
        plt.plot(x, y, 'co',color='r',markersize=2)
#    plt.plot(x[0], y[0], 'co',color='b')
    
    a_scale = float(max(x))/float(100)

    for i in range(n):
        for j in range(n):
            if A[i,j]>0.99:
                plt.arrow(x[i], y[i], (x[j] - x[i]), (y[j] - y[i]), 
                      head_width = a_scale,linewidth=0.5, color = 'g', length_includes_head = True)
            if 0.4999< A[i,j]< 0.5001:
                plt.arrow(x[i], y[i], (x[j] - x[i]), (y[j] - y[i]), 
                      head_width = a_scale,linewidth=0.5, color = 'r', length_includes_head = True)

   #Set axis too slitghtly larger than the set of x and y
    plt.xlim(min(x)-0.05*(max(x)-min(x)), max(x)+0.05*(max(x)-min(x)))
    plt.ylim(min(y)-0.05*(max(y)-min(y)), max(y)+0.05*(max(y)-min(y)))    
    plt.show()


def plot_graph(points, A):
    """
    Input:
        List of points
        Adjacency matrix A for the points
    """
    n = len(points)
    x = [];
    y = []
    for i in range(n):
        x.append(points[i][0])
        y.append(points[i][1])
        plt.plot(x, y, 'co', color='r', markersize=2)

    for i in range(n):
        for j in range(n):
            if A[i, j] == 1:
                if not (i == j):
                    plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], head_width=0, linewidth=0.5,
                              color='g', length_includes_head=False)

    plt.text(points[0, 0], points[0, 1], "s1", size=15)
    plt.text(points[1, 0], points[1, 1], "t1", size=15)
    plt.text(points[n - 2, 0], points[n - 2, 1], "s2", size=15)
    plt.text(points[n - 1, 0], points[n - 1, 1], "t2", size=15)

    # Set box slitghtly larger than the range of x and y
    plt.xlim(min(x) - 0.05 * (max(x) - min(x)), max(x) + 0.05 * (max(x) - min(x)))
    plt.ylim(min(y) - 0.05 * (max(y) - min(y)), max(y) + 0.05 * (max(y) - min(y)))

    plt.show()


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

 
def main():

    n = 26  #number of points

    np.random.seed(14)

    points = np.random.normal(size=(n,2))    # create random points
    print(points)
    D=compute_distances(points)
               
    x = cy.Variable((n,n),boolean=True)   #x[i,j]=1 if there is an arc from i to j
    
    #########################
    
    constraints = [x>=0]

    for i in range(n):
        constraints += [sum(x[i, j] for j in range(n)) == 2]

    for i in range(n):
        for j in range(n):
            constraints += [x[i, j] == x[j,i]]
    for i in range(n):
        constraints += [x[i, i] == 0]
    objective = cy.Minimize(sum(sum(x[i,j]*D[i,j] for i in range(n))for j in range(n)))

    prob = cy.Problem(objective, constraints)
    print("Solving")
    prob.solve(solver=cy.GLPK_MI)
    print("Solved")
    
    #########################
    print(prob.status)
    try:
        xval=np.array(x.value)
        plot_solution(points,xval)
    except:
        print('No solution found')
    
main()


