
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
    
    D=compute_distances(points)
               
    x = cy.Variable((n,n),boolean=True)   #x[i,j]=1 if there is an arc from i to j
    
    #########################
    
    
    """
    
    
    TO: Add missing code
    
    
    """
    
    #########################

    try:
        xval=np.array(x.value)
        plot_solution(points,xval)
    
    except:
        print('No solution found')
    
main()


    