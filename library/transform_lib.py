import numpy as np

import torch


def convert_coordinates(coordinates):
    converted_coordinates = [
        (coord[0].detach().cpu(), coord[1].detach().cpu()) for coord in coordinates]
    return converted_coordinates


# # Transformation matrix
transformation_matrix = np.array([[2.62206220e-04, -8.02909059e-02,  7.42766366e+01],
                                  [-7.78059697e-02, 4.39613517e-04, 4.73034593e+01],
                                  [8.75700314e-06, -5.61319117e-05, 1.00000000e+00]])

# Transformation matrix
# transformation_matrix = np.array([[3.44438901e-04, -7.77812382e-02,  7.42830650e+01],
#                                   [-7.50681185e-02,  1.09117811e-03,  4.66390570e+01],
#                                   [1.92547585e-05, -5.45908132e-05,  1.00000000e+00]])


def transform_coordinates(camera_coordinates):

    transformed_coords = []

    camera_coordinates = convert_coordinates(camera_coordinates)

    for coord in camera_coordinates:
        # Create homogeneous coordinates [x, y, 1]
        homogeneous_coords = np.array([[coord[0]],
                                       [coord[1]],
                                       [1]])

        # Apply transformation matrix
        real_world_coords = np.dot(transformation_matrix, homogeneous_coords)

        # Normalize the homogeneous coordinates
        real_world_coords /= real_world_coords[2]

        # Extract x and y coordinates from the transformed coordinates
        real_world_x = round(real_world_coords[0][0], 3)
        real_world_y = round(real_world_coords[1][0], 3)

        transformed_coords.append([real_world_x, real_world_y])

    return transformed_coords
