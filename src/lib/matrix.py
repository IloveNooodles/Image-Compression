import numpy as np
import sympy as sp


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
  # try:
  #   return Matrix.det()
  # except:
  #   return "Tidak memiliki determinant"
# def eigenMatrix(Matrix, eigenValue):
x = sp.Symbol('x')
ans = sp.solve(x < 3)
print(ans)


# a = np.array((m, n))
# a = np.array([0, 1, 5, 3, -6, 9, 2, 6, 1])
# a = a.reshape(3, 3)
# print(a)
# print(detMatrix(a))
