#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 19:03:44 2023

@author: cobeliu
"""
#copied from https://github.com/bnsreenu/python_for_image_processing_APEER/blob/master/tutorial23_reading_proprietary_images_into_python.py
###########Reading OME-TIFF using apeer_ometiff_library ###########
# pip install apeer-ometiff-library first 
# to import the package you need to use import apeer_ometiff_library
#OME-TIFF has tiff and metada (as XML) embedded
#Image is a 5D array.


from apeer_ometiff_library import io  #Use apeer.com free platform for image processing in the cloud

(img, omexml) = io.read_ometiff("images/Osteosarcoma_01_8bit.ome.tiff")  #Unwrap image and embedded xml metadata
print (img.shape)   #to verify the shape of the array
print(img)

print(omexml)

#Let us extract only relevant pixels, all channels in x and y
img1=img[0, 0, :, :, :]
print(img1.shape)
#Next, let us extract each channel image.
img2=img1[0,:,:]  #First channel, Red
img3=img1[1,:,:] #Second channel, Green
img4=img1[2,:,:] #Third channel, Blue

