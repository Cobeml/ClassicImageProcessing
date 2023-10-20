#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:01:24 2023

@author: cobeliu
"""

import bm3d
import cv2
from skimage import img_as_float, img_as_ubyte
from skimage.restoration import denoise_tv_chambolle
import os

### Functions to perform their process on img

def bilateral(in_img):
    try:
        kernel_size = int(input('Kernel Size (int): '))
        sigma_color_int = float(input('Sigma Color Int (spatial weighting)(0 to 1): '))
        sigma_space_int = float(input('Sigma Space Int (range weighting)(0 to 1): '))
        out_img = cv2.bilateralFilter(in_img, kernel_size, sigma_color_int, sigma_space_int, borderType = cv2.BORDER_CONSTANT)
        return out_img
    except:
        print('ERROR')
        
def bm3d_func(in_img):
    try: 
        sigma_psd_input = float(input('Noise Standard Deviation (0 to 1): '))
        stage_arg_input = ''
        while stage_arg_input == '':
            stage = input('All Stages (A) or Hard Thresholding (H): ')
            if stage == 'A':
                stage_arg_input = 'BM3DStages.ALL_STAGES'
            elif stage == 'H':
                stage_arg_input = 'BM3DStages.HARD_THRESHOLDING' 
        out_img = bm3d.bm3d(in_img, sigma_psd = sigma_psd_input, stage_arg = stage_arg_input)
        return out_img
    except:
        print('ERROR')
        
def canny(in_img):
    try:    
        lower_threshold = float(input('Lower Threshold (0 to 1): '))
        upper_threshold = float(input('Upper Threshold (0 to 1): '))
        in_img = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
        out_img = cv2.Canny(in_img, lower_threshold, upper_threshold)
        return out_img
    except:
        print('ERROR')

def channel_isolation(in_img):
    channel = -1
    while not (channel == 0 or channel == 1 or channel == 2):
        try: 
            channel = int(input('Channel (blue(0), green(1), red(2)): '))
        except:
            print('Channel must be int 0, 1, or 2')
    out_img = in_img[:, :, channel]
    return out_img

def gaussian(in_img):
    try:
        kernel_size = int(input('Kernel Size (int): '))
        sigma = float(input('Sigma (0 to 1): '))
        out_img = cv2.GaussianBlur(in_img, (kernel_size, kernel_size), sigma, borderType = cv2.BORDER_CONSTANT)
        return out_img
    except:
        print('ERROR')

def gray(in_img):
    out_img = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
    return out_img

def median(in_img):
    try:
        kernel_size = int(input('Kernel Size (int): '))
        out_img = cv2.medianBlur(in_img, kernel_size)
        return out_img
    except:
        print('ERROR')

def non_local_means(in_img):
    try:
        h = float(input('Filter Strength (float): '))
        template_window_size = int(input('Template Window Size (num of pixels) (should be odd) (e.g. 7): '))
        search_window_size = int(input('Search Window Size (num of pixels) (should be odd) (e.g. 21): '))
        out_img = cv2.fastNlMeansDenoisingColored(in_img, None, h, h, template_window_size, search_window_size)
        return out_img
    except:
        print('ERROR')
        
def rescale(in_img):
    try:
        fx_input = float(input('x Scale: '))
        fy_input = float(input('y Scale: '))
        out_img = cv2.resize(in_img, None, fx = fx_input, fy = fy_input, interpolation = cv2.INTER_CUBIC)
        return out_img
    except:
        print('ERROR')

def sobel(in_img):
    in_img = gray(in_img)
    out_img = cv2.Sobel(in_img, None, -1, 1, 1)
    return out_img

def total_variation(in_img):
    try:
        weight_input = float(input('Weight (0 to 1): '))
        eps_input = float(input('Passable Error (e.g. 0.0002): '))
        n_inter_max_input = int(input('Maximum # of Iterations: '))
        
        correct_input = False
        multichannel_input = False
        while correct_input == False:
            multichannel = input('Multichannel (y or n): ')
            if multichannel == 'y':
                multichannel_input = True
                correct_input = True
            elif multichannel == 'n':
                multichannel_input = False
                correct_input = True
        
        out_img = denoise_tv_chambolle(in_img, weight = weight_input, eps = eps_input, max_num_iter = n_inter_max_input, multichannel = multichannel_input)
        return out_img
    except: 
        print('ERROR')
        
def unsharp_mask(in_img):
    try:
        amount = float(input('Mask Multiplication Factor (e.g. 2): '))
        mask = (in_img - gaussian(in_img)) * amount
        out_img = in_img + mask
        return out_img
    except:
        print('ERROR') 

processes = ['bilateral', 'bm3d', 'canny', 'channel isolation', 'gaussian', 'gray', 'median', 'non-local means', 'rescale', 'sobel', 'total variation', 'unsharp mask']
image_list = os.listdir('/Users/cobeliu/ImageProcessing/images')

process = ''
image = ''

### Get image and process from user

while not image in image_list:
    image = input('Image (input o to see options)(image processed as float): ')
    if image == 'o':
        for item in image_list:
            print(item)
    
while not process in processes:
    process = input('Process (input o to see options): ')
    if process == 'o':
        for item in processes:
            print(item)

img = img_as_float(cv2.imread('images/' + image))

### process image

processed_img = []
if process == 'bilateral':
    processed_img = bilateral(img)
elif process == 'bm3d':
    processed_img = bm3d_func(img)
elif process == 'canny':
    processed_img = canny(img)
elif process == 'channel isolation':
    processed_img = channel_isolation(img)
elif process == 'gaussian':
    processed_img = gaussian(img)
elif process == 'gray':
    processed_img = gray(img)
elif process == 'median':
    processed_img = median(img)
elif process == 'non-local means':
    processed_img = non_local_means(img)
elif process == 'rescale':
    processed_img = rescale(img)
elif process == 'sobel':
    processed_img = sobel(img)
elif process == 'total variation':
    processed_img = total_variation(img)
elif process == 'unsharp mask':
    processed_img = unsharp_mask(img)

### show image
processed_img = img_as_ubyte(processed_img)
img = img_as_ubyte(img)

cv2.imshow('Original Image', img)
cv2.imshow('Processed Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
