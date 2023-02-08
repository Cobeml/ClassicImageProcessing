#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 18:50:11 2023

@author: cobeliu
"""
#All images are numpy arrays in these libraries  


from skimage import io, img_as_float

img = io.imread('images/Osteosarcoma_01.tif')
#prints dimensions of image/numpy array
print(img.shape)

#converts pixel to float value
img2 = img_as_float(img)

#converts pixel back to 8 bit
img3 = img_as_ubyte(img2)

import cv2

#cv2 reads images as BGR
img_cv2 = cv2.imread('images/Osteosarcoma_01.tif')
#0 as second arg makes img gray
gray_img = cv2.imread('images/Osteosarcoma_01.tif', 0)
#converts img to RGB
img_cv2_RGB = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
  