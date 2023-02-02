import numpy as np

def sd(x,Y,grad,f):
    """Steepest descent solution of linear equation system"""
    
    R  = Y-f(x)
    g  = grad(x)
    G = f(g)
    alpha = np.dot(R,G)/np.dot(G,G)
    x = x + alpha*g
    print("alpha: ", alpha)
    print("x: ",x)



