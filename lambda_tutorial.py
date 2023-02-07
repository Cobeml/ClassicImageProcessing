#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 18:24:24 2023

@author: cobeliu
"""
car1_v = input('Initial velocity of car 1: ')
car1_a = input('Acceleration of car 1: ')
car2_v = input('Initial velocity of car 2: ')
car2_a = input('Acceleration of car 2: ')
time_passed = int(input('Time elapsed: '))

"""
function with inputs initial velocity and acceleration,
outputs function returning distance traveled based on time
"""
def distance_equation(v, a):
    return lambda t: v*t + 1/2*a*t**2

time1 = []
distance1 = []

time2 = []
distance2 = []

#creates two distance functions for two different cars
car1 = distance_equation(car1_v, car1_a)
car2 = distance_equation(car2_v, car2_a)

#puts respective time and distance for each car in their lists
for t in range(0, time_passed + 5, 5):
    d1 = car1(t)
    d2 = car2(t)
    
    time1.append(t)
    time2.append(t)
    
    distance1.append(d1)
    distance2.append(d2)

#plots the two different cars distance v time
from matplotlib import pyplot as plt
plt.plot(time1, distance1)
plt.plot(time2, distance2)