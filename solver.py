import numpy as np

def Gauss_elim(A, AX):
    B = np.zeros((len(A), len(A)))
    BX = np.zeros((len(A)))
    for i in range(len(A)):
        for j in range(len(A)):
            B[i, j] = A[i, j]
    for i in range(len(A)):
        BX[i] = AX[i]
    size = len(AX)
        
    for i in range(1, size, 1):
    
        for j in range(i, size, 1):
            BX[j] -= BX[i-1] * (B[j, i-1] / B[i-1, i-1])
            B[j, i-1:size] -= B[i-1, i-1:size] * (B[j, i-1] / B[i-1, i-1])
    
    X = BackwardSub(B, BX)
    
    return X

def BackwardSub (A, AX):
    size = len(AX)
    X = np.zeros(size)
    
    for i in range(size - 1, -1, -1):
        X[i] = AX[i]
    
        for j in range(size - 1, i, -1):
            X[i] -= (A[i, j] * X[j])
        
        X[i] /= A[i, i]
    
    return X

def Linear_LS_Regression(x, y, n):
    Sxy = 0
    Sx = Sy = 0
    Sx2 = 0
    
    for i in range(n):
        Sxy += x[i] * y[i]
        Sx += x[i]
        Sy += y[i]
        Sx2 += x[i] * x[i]
        
    a = (n*Sxy - Sx*Sy) / (n * Sx2 - Sx * Sx)
    b = Sy / n - a * Sx / n
    
    return a, b

def poly_regress(x, y, order):
    order=order+1
    A = np.zeros((order,order))
    SXi = np.zeros(2*order)
    Y = np.zeros(order)
    
    for i in range(2*order):
        temp = 0
        for j in range(len(x)):
            temp += x[j] ** i
        SXi[i] = temp
    
    for i in range(order):
        for j in range(order):
            A[i][j] = SXi[i+j]
    for i in range(order):
        temp = 0
        for j in range(len(y)):
            temp += y[j] * (x[j]** i)
        Y[i] = temp
    
    return Gauss_elim.Gauss_elim(A, Y)  
