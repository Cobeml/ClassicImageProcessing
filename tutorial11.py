#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 18:12:23 2023

@author: cobeliu
"""

m = int(input('Provide mass in kg: '))
c = 300000000
E = m * c**2

#prints energy in exponential format with two decimal places
print('Energy =', '{:.2E}'.format(E))