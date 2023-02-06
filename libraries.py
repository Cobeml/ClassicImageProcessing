# image processing libraries
from skimage import io
img1 = io.imread('images/Osteosarcoma_01.tif')

import cv2
img2 = cv2.imread('images/Osteosarcoma_01.tif')

# data analysis libraries
import numpy as np
a = np.ones((5,5))

# plotting and visualization libraries
from matplotlib import pyplot as plt
plt.imshow(img1)

