
from ultralytics import YOLO
# from library import nlp_command as nc
from library import problem_lib as pl
from library import transform_lib as tl
from inverse_MPC import driverCodeMPC_4 as mpc
import numpy as np

import cv2
import time

import serial


model = YOLO('best.pt')

cap = cv2.VideoCapture(1)
# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize a dictionary to store camera coordinates for each class
class_coordinates = {}
# initial_guess = np.array([0.0, 0.0, 0.0, 0.0])


# arduino = serial.Serial(port='COM10',  baudrate=9600, timeout=.1)


# def write_read(x):
#     x = x + '\r'
#     arduino.write(bytes(x,  'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data


# Main loop to continuously process the camera image
while True:

    print("entered loop")
    coor_cup = []
    coor_obstacle = []
    coor_dispenser = []

    command = input("enter command input: ")
    # Convert command to integer to perform comparison
    command = int(command)

    if command == 0:  # Exit the loop if 0 is entered
        break
    elif command == 1:

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # Capture a single frame
        ret, frame = cap.read()
        if ret:
            results = model.predict(frame, show=True, save=False
                                    )

        # # cv2.imshow(frame, "current camera frame")
        # # Clear the dictionary at the beginning of each frame
        # class_coordinates = {}

        # # Process the detected objects
        # for result in results:
        #     for box in result.boxes:
        #         class_id = box.cls[0].item()
        #         class_label = result.names[class_id]
        #         # Get the normalized bounding box coordinates
        #         x_center, y_center, norm_width, norm_height = box.xywh[0]

        #         # Store the camera coordinates in the dictionary
        #         if class_label not in class_coordinates:
        #             class_coordinates[class_label] = []

        #         class_coordinates[class_label].append((x_center, y_center))

        # target_class_label = "0"
        # if target_class_label in class_coordinates:
        #     coor_fallencup = class_coordinates[target_class_label]

        # target_class_label = "1"
        # if target_class_label in class_coordinates:
        #     coor_cup = class_coordinates[target_class_label]

        # # target_class_label = "4"
        # # if target_class_label in class_coordinates:
        # #     coor_obstacle = class_coordinates[target_class_label]
        # coor_cup = [[(42-6), -21.5]]
        # coor_cup = tl.transform_coordinates(coor_cup)
        # print(F'THI IS cup cordniate: {coor_cup}')
        # optimizedJointAngles, _ = mpc.invOpt(
        #     0, 0, 0, 0, (coor_cup[0][0]/100), (coor_cup[0][1]/100), 0.02)
        # print(f'this is angles: {optimizedJointAngles}')

        # value = str(-optimizedJointAngles[0][0])+','+str(optimizedJointAngles[1][0])+','+str(
        #     optimizedJointAngles[2][0])+','+str(-optimizedJointAngles[3][0])
        # print(value)
        # value1 = write_read(value)

        time.sleep(5)
