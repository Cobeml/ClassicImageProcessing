#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 19:56:50 2023

@author: cobeliu
NOT ENOUGH OR ACCURATE SEGMENTATION: SOMETHING WRONG WITH WATERSHED PARAM MAYBE?
"""

import cv2
import numpy as np

# Read the image
img = cv2.imread('images/Osteosarcoma_01.tif')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary mask
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# Perform morphological opening to remove noise
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)

# Perform morphological closing to fill holes
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations = 3)

# Perform distance transform
dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)

# Threshold the distance transform image to obtain markers for watershed segmentation
ret, markers = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, cv2.THRESH_BINARY)

# Convert the markers to 8-bit unsigned integers
markers = np.uint8(markers)

# Apply watershed segmentation
markers = cv2.connectedComponents(markers)[1]
markers = cv2.watershed(img, markers)

# Overlay the markers on the original image
img[markers == -1] = [0,0,255]

# Display the segmented image
cv2.imshow('Segmented image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
