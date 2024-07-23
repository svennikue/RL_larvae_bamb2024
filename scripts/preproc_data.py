#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:20:21 2024

@author: Svenja Kuchenhoff

headTheta - head angle
headXY 	- head position

"""

import scipy.io
import os
import pickle
import matplotlib.pyplot as plt
import json


control_path_motor = "/Users/xpsy1114/Documents/projects/BAMB2024/group_project/RL_larvae_bamb2024/data/motorData_control.json"
with open(control_path_motor, 'r') as f:
    control_motor = json.load(f)






# wt_path = "/Users/xpsy1114/Documents/projects/BAMB2024/group_project/PDM-DN_wt background/"

# motor_data_wt = scipy.io.loadmat(wt_path + 'motorData.mat')

# with open(f"{wt_path}/control_motor.p", 'rb') as file:
#     motor_data_wt = pickle.load(file)
            
       
headXY = []
for animal in range(0, len(control_motor['motorData'])):
    headXY.append(control_motor['motorData'][animal]['headXY'])
    

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
    plt.scatter(x_coords, y_coords, marker='o', color=colors[i], label=f'Trajectory {i+1}')

# Plot the global bounding square
# plt.plot(square_x, square_y, color='m', linestyle='--', label='Bounding Square')

# Adding labels and title
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Trajectories and Global Bounding Square')
plt.legend()

# Display the plot
plt.show()

  
coordinates = control_motor['motorData'][0]['headXY']
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
#plt.plot(x_coords, y_coords, marker='o', color='b', label='Trajectory')

# Plot the square
# plt.plot(square_x, square_y, color='r', linestyle='--', label='Bounding Square')

# Adding labels and title
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Trajectory and Bounding Square')
plt.legend()

# Display the plot
plt.show()


import numpy as np
import matplotlib.pyplot as plt

def map_to_action(current_state, previous_state, grid_size=100):
    #import pdb; pdb.set_trace()
    # Unpack states
    x, y, _ = current_state
    prev_x, prev_y, _ = previous_state

    # Calculate the grid cell for each point
    current_cell = (int(np.round(x)), int(np.round(y)))
    previous_cell = (int(np.round(prev_x)), int(np.round(prev_y)))

    # If we're in the same cell, it's a 'stay' action
    if current_cell == previous_cell:
        return 0

    # Calculate the difference in cell coordinates
    dx = current_cell[0] - previous_cell[0]
    dy = current_cell[1] - previous_cell[1]

    # Map the difference to an action
    # 0: stay, 1: east, 2: northeast, 3: north, 4: northwest, 
    # 5: west, 6: southwest, 7: south, 8: southeast
    action_map = {
        (1, 0): 1, (1, 1): 2, (0, 1): 3, (-1, 1): 4,
        (-1, 0): 5, (-1, -1): 6, (0, -1): 7, (1, -1): 8
    }

    return action_map.get((dx, dy), 0)  # Default to 'stay' if not in map

# Generate sample data
np.random.seed(42)
n_points = 500
x = np.cumsum(np.random.normal(0, 0.01, n_points)) % 1  # Wrap around at 1
y = np.cumsum(np.random.normal(0, 0.01, n_points)) % 1  # Wrap around at 1
angle = np.cumsum(np.random.normal(0, 0.1, n_points))


x = x_coords
y = y_coords

angle = coordinates = control_motor['motorData'][0]['headTheta']

# Create arrays to store discretized data
x_disc = []
y_disc = []
actions = []

# Map actions and create discretized data
for i in range(5, n_points, 5):
    current_state = (x[i], y[i], angle[i])
    previous_state = (x[i-5], y[i-5], angle[i-5])
    action = map_to_action(current_state, previous_state)
    actions.append(action)
    
    # Store the previous point for discretized data
    x_disc.append(x[i-5])
    y_disc.append(y[i-5])

# Plotting
plt.figure(figsize=(12, 12))

# Plot grid
for i in range(101):
    plt.axhline(y=i/100, color='gray', linestyle=':', alpha=0.5)
    plt.axvline(x=i/100, color='gray', linestyle=':', alpha=0.5)

# Plot original trajectory
plt.plot(x, y, 'b-', alpha=0.5, label='Original')

# Plot discretized points with action colors
action_colors = ['black', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'pink']
for i, action in enumerate(actions):
    plt.scatter(x_disc[i], y_disc[i], c=action_colors[action], s=50, label=f'Action {action}' if action not in plt.gca().get_legend_handles_labels()[1] else "")

# Draw arrows for non-stay actions
for i in range(len(actions)):
    if actions[i] != 0:
        dx = x[(i+1)*5] - x[i*5]
        dy = y[(i+1)*5] - y[i*5]
        plt.arrow(x_disc[i], y_disc[i], dx, dy, head_width=0.01, head_length=0.01, fc=action_colors[actions[i]], ec=action_colors[actions[i]], alpha=0.7)

plt.title('Grid World Trajectory with Actions')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.show()

