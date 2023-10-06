import numpy as np
from PIL import Image
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy import interpolate
import sympy as syp
import pandas as pd
import cv2
import math

def rotate_bicubic(image, angle):
    print('rotate bi cubic is run ')
    height, width, _ = image.shape
    rotated_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Calculate the rotation angle in radians.
    theta = math.radians(angle)

    # Calculate the coordinates of the center of the image.
    center_x = width / 2
    center_y = height / 2

    for i in range(height):
        print(f'\rrun bicubic: [{i}/{new_height}]', end='')
        for j in range(width):
            # Calculate the new coordinates after rotation.
            x = j - center_x
            y = i - center_y
            new_x = x * math.cos(theta) - y * math.sin(theta) + center_x
            new_y = x * math.sin(theta) + y * math.cos(theta) + center_y

            # Check if the new coordinates are within the bounds of the image.
            if 0 <= new_x < width and 0 <= new_y < height:
                # Perform bicubic interpolation using the provided bicubic_kernel function.
                x1, y1 = int(new_x), int(new_y)
                dx = new_x - x1
                dy = new_y - y1

                interpolated_pixel = [0, 0, 0]
                for c in range(3):  # Iterate over color channels (R, G, B).
                    channel_value = 0
                    for m in range(-1, 3):
                        for n in range(-1, 3):
                            x_index = min(max(x1 + n, 0), width - 1)
                            y_index = min(max(y1 + m, 0), height - 1)
                            coefficient = bicubic_kernel(dx - n) * bicubic_kernel(dy - m)
                            channel_value += coefficient * image[y_index, x_index, c]

                    interpolated_pixel[c] = np.clip(int(channel_value), 0, 255)

                rotated_image[i, j] = interpolated_pixel
    print('rotate bi cubic is run ')
    return rotated_image

# تابع بای‌کیوبیکی ارائه شده توسط شما
def bicubic_kernel(x):
    x = abs(x)
    if 0 <= x < 1:
        return 1 - 2 * x ** 2 + x ** 3
    elif 1 <= x < 2:
        return 4 - 8 * x + 5 * x ** 2 - x ** 3
    else:
        return 0