import numpy as np
import sympy
from PIL import Image
import os
import glob
# z = np.random.rand(5, 4)
# a, b = np.linalg.qr(z)
# print(a, b)

# for i in range(1000):

#ini buat 1 channel
def simultaneous_power_iteration(A, k):
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
    Q_prev = Q

    for i in range(200):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

        # can use other stopping criteria as well 
        err = ((Q - Q_prev) ** 2).sum()
        if i % 10 == 0:
          pass

        Q_prev = Q
        if err < 1e-3:
            break

    return np.diag(R), Q
  
# AING GATAU CARA IMPORT GIMANA INTINYA


with Image.open("D:\\Coding\\Algeo02-20029\src\\assets\\13.jpg", mode="r") as im:
  # im.show()
  
  width, height = im.size
  print(width, height)
  
  imarray = np.asarray(im) #Ini buat convert ke image
  print(imarray.shape)
  
  r, g, b = Image.Image.split(im)
  R = np.asarray(r)
  G = np.asarray(g)
  B = np.asarray(b)
  
  Rheight, Rwidth = R.shape
  print(Rwidth, Rheight)

  #M X N -> M x M @ M X N @ N x N
  
  # Channel Red
  def SVD(Matrix):
    Matrix_R = Matrix @ np.transpose(Matrix) #kiri
    SIG, U = simultaneous_power_iteration(Matrix_R, 100)
    uRow, uWidth = U.shape
    U_2 = np.pad(U, ((0,0), (0, height - uWidth)))
    
    SIG = np.diag(SIG)
    SIGRow, SIGWidth = SIG.shape
    SIG_2 = np.pad(SIG, ((0, height - SIGRow), (0, width - SIGWidth)))
    
    Matrix_L = np.transpose(R) @ R #Kanan
    _, V = simultaneous_power_iteration(Matrix_L, 100)
    VT = np.transpose(V)
    VWidth, Vheigth = VT.shape #udah di tarnspose
    VT_2 = np.pad(VT, ((0, width - VWidth), (0, 0)))
    
    return U_2 @ SIG_2 @ VT_2
    
  svdR = SVD(R)
  svdG = SVD(G)
  svdB = SVD(B)
  print(svdR, svdG, svdB)
  
  IM_matr = np.dstack((svdR, svdG, svdB)).astype(np.uint8)
  IM_Final = Image.fromarray(np.uint8(IM_matr))
  IM_Final.show()
  
  # a, b = simultaneous_power_iteration(R, 100)
  # print(a, b)
  # print(R, G ,B)
  
  
  # im2 = Image.fromarray(np.uint8(imarray)) #convert balik
  # im2.show()
# if(__name__ == "__main__"):
#   main()

# a = np.array([[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]])
# print(np.transpose(a))
# # def run():


# # if __name__ == "__main__":
# #   run()