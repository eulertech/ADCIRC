# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 11:54:53 2016

@author: liang.kuang
"""

import numpy as np

def check(p1, p2, base_array):
    """
    Uses the line defined by p1 and p2 to check array of 
    input indices against interpolated value

    Returns boolean array, with True inside and False outside of shape
    """
    idxs = np.indices(base_array.shape) # Create 3D array of indices

    p1 = p1.astype(float)
    p2 = p2.astype(float)

    # Calculate max column idx for each row idx based on interpolated line between two points
    max_col_idx = (idxs[0] - p1[0]) / (p2[0] - p1[0]) * (p2[1] - p1[1]) +  p1[1]    
    sign = np.sign(p2[0] - p1[0])
    return idxs[1] * sign <= max_col_idx * sign

def create_polygon(shape, vertices):
    """
    Creates np.array with dimensions defined by shape
    Fills polygon defined by vertices with ones, all other values zero"""
    base_array = np.zeros(shape, dtype=float)  # Initialize your array of zeros

    fill = np.ones(base_array.shape) * True  # Initialize boolean array defining shape fill

    # Create check array for each edge segment, combine into fill array
    for k in range(vertices.shape[0]):
        fill = np.all([fill, check(vertices[k-1], vertices[k], base_array)], axis=0)

    # Set all values inside polygon to one
    base_array[fill] = 1

    return base_array


# (Row, Col) Vertices of Polygon (Defined Clockwise)
vertices = np.array([
    [5,12],
    [8,18],
    [13,14],
    [11,6],
    [4,6],
])

polygon_array = create_polygon([20,20], vertices)

# This section prints numbers at each vertex for visual check, just comment out 
# to print an array of only zeros and ones
for n, vertex in enumerate(vertices):
    polygon_array[vertex[0],vertex[1]] = 10*(n+1)

# Simple routine to print the final array
for row in polygon_array.tolist():
    for c in row:
        print ('%4.1f'%c)
    print('')