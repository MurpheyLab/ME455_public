"""
2D camera environment simulation
Date: May 27, 2024
Author: Muchen Sun
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2

# Set up the canvas
canvas_size = (800, 600)
canvas = np.zeros((canvas_size[1], canvas_size[0], 3), dtype=np.uint8)
canvas[:] = (211, 211, 211)  # Set the canvas to light gray

# Draw the green square
square_size = 200
square_x, square_y = 100, 100
canvas[square_y:square_y+square_size, square_x:square_x+square_size, 0] = 0
canvas[square_y:square_y+square_size, square_x:square_x+square_size, 1] = 255  # Green
canvas[square_y:square_y+square_size, square_x:square_x+square_size, 2] = 0

# Draw the blue triangle
triangle_points = np.array([[400, 400], [600, 400], [500, 500]], dtype=np.int32)
canvas = cv2.fillPoly(canvas, [triangle_points], (0, 0, 255))  # Blue

# Draw the red circle
circle_x, circle_y = 600, 200
circle_radius = 80
for i in range(canvas_size[1]):
    for j in range(canvas_size[0]):
        dist = np.sqrt((circle_y-i)**2 + (circle_x-j)**2)
        if dist < circle_radius:
            canvas[i,j] = (255, 0, 0)


# Simulate the camera movement
camera_width, camera_height = 400, 300
camera_speed = 2

# Create the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Initialize the camera position
camera_x = np.random.randint(0, canvas_size[0] - camera_width)
camera_y = np.random.randint(0, canvas_size[1] - camera_height)

# Function to update the camera position and captured image
def update_camera(frame):
    global camera_x, camera_y

    # Randomly sample the camera position
    camera_x_new = np.random.randint(np.maximum(0, camera_x-50), np.minimum(camera_x+50, canvas_size[0]-camera_width))
    camera_y_new = np.random.randint(np.maximum(0, camera_y-50), np.minimum(camera_y+50, canvas_size[1]-camera_height))
    camera_x = camera_x_new 
    camera_y = camera_y_new

    # Update the captured image
    ax1.cla()
    ax1.imshow(canvas[camera_y:camera_y+camera_height, camera_x:camera_x+camera_width])
    ax1.set_title(f"Captured Image (FoV: {camera_width}x{camera_height})")
    ax1.set_axis_off()

    # Update the canvas with the camera FoV
    ax2.cla()
    ax2.imshow(canvas)
    ax2.add_patch(plt.Rectangle((camera_x, camera_y), camera_width, camera_height, fill=False, color='k'))
    ax2.set_title("Full Canvas")
    ax2.set_axis_off()

    return ax1.images + ax2.images + ax2.patches

# Create the animation
ani = animation.FuncAnimation(fig, update_camera, frames=100, interval=50, blit=True)
ani.save('camera_sim_example.mp4')

plt.show()