#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:35:20 2023

@author: cobeliu
"""

from skimage import io, filters
from matplotlib import pyplot as plt

def gaussian_of_img(img, sigma = 1):
    gaussian_img = filters.gaussian(img, sigma)
    return(gaussian_img)



my_image = io.imread('images/Osteosarcoma_01.tif')

filtered = gaussian_of_img(my_image, 30)

plt.imshow(filtered)
