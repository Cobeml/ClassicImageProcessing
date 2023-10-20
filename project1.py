#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 00:45:01 2023

This code reads in two medical images of cells and then processes them and counts the cells and returns information on each cell.

@author: cobeliu
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage.measure import regionprops
from skimage.feature import graycomatrix, graycoprops
import math
import urllib.request
    
def analyze_nuclei(color_image, single_channel_image, blur_sigma, close_kernel_size, open_kernel_size, canny_low, canny_high, filename):
    # Apply Gaussian blur with a 5x5 kernel
    blurred_image = cv2.GaussianBlur(single_channel_image, (5, 5), blur_sigma)
    
    # Apply Otsu's thresholding
    threshold_value, thresholded_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Perform closing 
    close_kernel = np.ones((close_kernel_size, close_kernel_size), np.uint8)
    closed_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_CLOSE, close_kernel)
    
    # Perform opening
    open_kernel = np.ones((open_kernel_size, open_kernel_size), np.uint8)
    cleaned_image = cv2.morphologyEx(closed_image, cv2.MORPH_OPEN, open_kernel)
    
    # Apply median filter
    median_image = cv2.medianBlur(cleaned_image, 3)
    
    # Apply Gaussian blur with a 5x5 kernel
    gaussian_image = cv2.GaussianBlur(median_image, (5, 5), blur_sigma)
    
    # Apply canny edge detection
    edges = cv2.Canny(gaussian_image,canny_low,canny_high)

    # Find contours
    contours, num_of_cells = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    copy_image = color_image.copy()
    
    # Draw contours
    img_contours = cv2.drawContours(copy_image, contours, -1, (0,255,0), 3)
    
    # Create an empty image to draw contours on
    labelled_image = np.zeros_like(single_channel_image)
    
    # Draw each contour by filling it with a distinct label
    for idx, contour in enumerate(contours, start=1):
        cv2.drawContours(labelled_image, [contour], -1, (idx), thickness=cv2.FILLED)
    """
    # store images in list
    images = [color_image, single_channel_image, blurred_image, thresholded_image, closed_image, cleaned_image, median_image, gaussian_image, edges, img_contours, labelled_image]
    titles = ["Color Image", "Single Channel Image", "Gaussian Blurred Image (Kernel Size: 5, Sigma: " + str(blur_sigma) + ")", "Otsu's Thresholded Image", "Closed Image (Kernel Size: " + str(close_kernel_size) + ")", "Opened Image (Kernel Size: " + str(open_kernel_size) + ")", 'Median Image', "Gaussian Blurred Image (Kernel Size: 5, Sigma: " + str(blur_sigma) + ")", 'Canny Edges (Low Threshhold: ' + str(canny_low) + ', High Threshold: ' + str(canny_high) + ')', 'Contours Image', 'Labeled Image']
    
    # Calculate number of rows needed
    n = len(images)
    n_rows = n // 2 + n % 2
    
    # Create subplots
    fig, axs = plt.subplots(n_rows, 2, figsize=(10, n_rows*5))
    for i, ax in enumerate(axs.flat):
        # Remove axes for empty subplots
        if i >= n:
            ax.axis('off')
            continue
        
        
        
        ax.imshow(images[i], cmap='gray')  # Display image, use cmap='gray' for grayscale images
        ax.set_title(titles[i])
        ax.axis('off')  # Hide axes
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    """
    # Apply regionprops
    regions = regionprops(labelled_image)
    
    # Create a list to hold dictionaries of data for each region
    region_data = []
    
    # Iterate over each region to gather properties
    for i, region in enumerate(regions):
        # Get a patch for each region
        minr, minc, maxr, maxc = region.bbox
        region_patch = single_channel_image[minr:maxr, minc:maxc]
        
        # Compute GLCM features
        glcm = graycomatrix(region_patch, distances=[5], angles=[0, math.pi/2, math.pi, 3*math.pi/2], levels=256, symmetric=False, normed=False)
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        correlation = graycoprops(glcm, 'correlation')[0, 0]
    
        region_info = {
            "Area": region.area,
            "Centroid": region.centroid,
            "BoundingBox": region.bbox,
            "Perimeter": region.perimeter,
            "Orientation": region.orientation,
            "Major Axis Length": region.major_axis_length,
            "Minor Axis Length": region.minor_axis_length,
            "Contrast": contrast,
            "Dissimilarity": dissimilarity,
            "Homogeneity": homogeneity,
            "Energy": energy,
            "Correlation": correlation
        }
        
        region_data.append(region_info)
    
    # Create DataFrame
    df = pd.DataFrame(region_data)
    
    # Remove rows from the DataFrame where 'Area' is less than 5
    df = df[df['Area'] > 5].reset_index(drop=True)
    
    
    # Return the DataFrame
    return df, img_contours


    
# Read the image
image_path = 'images/Case_1-06.tif'
image = cv2.imread(image_path)

# Extract blue channel
blue_channel = image[:, :, 2];

best_filters = []

for i in range(1, 50, 10):
    for j in range(1, 50, 10):
        for k in range(1, 255, 30):
            for l in range (k, 256, 30):
                image_data, contours_image = analyze_nuclei(image, blue_channel, 15, i, j, k, l, 'image1.csv')
                
                print('cells: ' + str(len(image_data))) 
                if len(image_data) > 250 and len(image_data) < 400:
                    info = {
                        'Cells Counted': len(image_data),
                        'Close Kernel Size': i,
                        'Open Kernel Size': j,
                        'Canny Low Threshold': k,
                        'Canny High Threshold': l,
                        'Contours Image': contours_image
                    }
                    best_filters.append(info)

df = pd.DataFrame(best_filters)