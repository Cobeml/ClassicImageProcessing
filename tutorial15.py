#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 18:48:11 2023

Demonstrating differences between arrays and np arrays
@author: cobeliu
"""

a = [1, 2, 3, 4, 5]
b = 2*a

import numpy as np
c = np.array(a)
d = 2*c

x = np.array([1, 2, 3, 4])
y = np.array([3, 4, 5, 6], dtype=np.float128)

#Can add np arrays of same length
z = x + y

#No truncating when elements are floats
g = x/2
h = y/2


from skimage import io
#read as numpy array
img1 = io.imread('images/Osteosarcoma_01.tif')

#creates image where all pixels are of value one
ones = np.ones_like(img1)  

#creates numpy array with the first 10 rows in columns 4, 5, 6, and 7 from img1
piece = img1[:10, 4:8]

#creates list of sums of rows and another columns
row_sum = np.sum(img1, axis = 1)
column_sum = np.sum(img1, axis = 0)

#returns max pixel value
maxi = np.max(img1)