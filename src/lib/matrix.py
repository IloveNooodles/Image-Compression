import numpy as np
import sympy as sp
impo
print(test)

rng = np.random.default_rng()

def eigenvalues(Matrix):
  t = sp.Symbol('t')
  rows, cols = sp.shape(Matrix)
  val = [1 for i in range(rows)]
  I = sp.diag(*val)
  eq = (t*I - Matrix).det()
  roots = sp.solve(eq)
  try:
    for i in range(len(roots)):
      roots[i] = roots[i].evalf()
    roots.sort(reverse=True)
    return np.array(roots)
  except:
    return "Akar Imajiner"

def Transpose(Matrix):
  return np.transpose(Matrix)

def MultMatrix(A, B):
  return A*B

def detMatrix(Matrix):
  x = sp.Symbol('x')
  x = Matrix.det()
  print(x)
  try:
    return Matrix.det()
  except:
    return "Tidak memiliki determinant"

def simultaneous_power_iteration(A, k):
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
    Q_prev = Q
 
    for i in range(1000):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

        # can use other stopping criteria as well 
        err = ((Q - Q_prev) ** 2).sum()
        if i % 10 == 0:
            print(i, err)

        Q_prev = Q
        if err < 1e-3:
            break

    return np.diag(R), Q




