#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:20:21 2024

@author: xpsy1114
"""

import scipy.io
import os
import pickle
import matplotlib.pyplot as plt
import json


control_path_motor = "/Users/xpsy1114/Documents/projects/BAMB2024/group_project/data/motorData_PDM.json"

with open(control_path_motor, 'r') as f:
    control_motor = json.load(f)






wt_path = "/Users/xpsy1114/Documents/projects/BAMB2024/group_project/PDM-DN_wt background/"

motor_data_wt = scipy.io.loadmat(wt_path + 'motorData.mat')

with open(f"{wt_path}/control_motor.p", 'rb') as file:
    motor_data_wt = pickle.load(file)
            
       
headXY = []
for animal in range(0, len(motor_data_wt)):
    headXY.append(motor_data_wt[animal]['headXY'])
    

x_coords_all = []
y_coords_all = []
 
for coordinates in headXY:
  x_coords_all.extend([coord[0] for coord in coordinates])
  y_coords_all.extend([coord[1] for coord in coordinates])

x_min, x_max = min(x_coords_all), max(x_coords_all)
y_min, y_max = min(y_coords_all), max(y_coords_all)

# Define the corners of the global bounding square
square_x = [x_min, x_max, x_max, x_min, x_min]
square_y = [y_min, y_min, y_max, y_max, y_min]

# Plot each trajectory

def generate_colors(n):
    # Use a colormap (e.g., 'viridis', 'plasma', 'inferno', 'magma', 'cividis', etc.)
    colormap = plt.cm.get_cmap('hsv', n)  # Change 'hsv' to any preferred colormap
    colors = [colormap(i) for i in range(n)]
    return colors

# Generate 36 distinct colors
n_colors = len(headXY)
colors = generate_colors(n_colors)



for i, coordinates in enumerate(headXY):
    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]
    plt.plot(x_coords, y_coords, marker='o', color=colors[i], label=f'Trajectory {i+1}')

# Plot the global bounding square
plt.plot(square_x, square_y, color='m', linestyle='--', label='Bounding Square')

# Adding labels and title
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Trajectories and Global Bounding Square')
plt.legend()

# Display the plot
plt.show()

  
coordinates = motor_data_wt[0]['headXY']
# Extract x and y coordinates
x_coords = [coord[0] for coord in coordinates]
y_coords = [coord[1] for coord in coordinates]

# Determine the min and max values for x and y
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)

# Define the corners of the square
square_x = [x_min, x_max, x_max, x_min, x_min]
square_y = [y_min, y_min, y_max, y_max, y_min]

# Plot the trajectory
plt.plot(x_coords, y_coords, marker='o', color='b', label='Trajectory')

# Plot the square
plt.plot(square_x, square_y, color='r', linestyle='--', label='Bounding Square')

# Adding labels and title
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Trajectory and Bounding Square')
plt.legend()

# Display the plot
plt.show()