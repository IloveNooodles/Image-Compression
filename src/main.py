import numpy as np
import sympy
from PIL import Image
import os
import glob

with Image.open("D:\\Coding\\Algeo02-20029\src\\assets\\1.jpg", mode="r") as im:
  width, height = im.size
  print(height, width)
  im.show()

# def main():
#   image = Image.open(r"D:\Coding\Algeo02-20029\src\assets")

# if(__name__ == "__main__"):
#   main()

# a = np.array([[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]])
# print(np.transpose(a))
# # def run():


# # if __name__ == "__main__":
# #   run()