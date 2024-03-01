#
from ultralytics import YOLO
from library import nlp_command as nc
from library import problem_lib as pl
from library import transform_lib as tl
from library import threshold as th
from inverse_MPC import driverCodeMPC_4 as mpc
import pygame
import numpy as np
import cv2
import time
import nemo
import nemo.collections.asr as nemo_asr
import torch
import serial


## ----------------ASR INITIALIZATION--------------##
# Specify the path to the .wav file you want to transcribe
wav_file_path = 'datasets/67-602650-0039.wav'

# Load the pre-trained ASR model from NeMo
asr_model = nemo.collections.asr.models.EncDecCTCModelBPE.restore_from(
    'model_3.nemo')
asr_model = asr_model.to('cuda' if torch.cuda.is_available() else 'cpu')

words_to_check = ["sprite", "water", "coffee", "orange"]


## -----------------VISION INITIALIZATION--------------##
region_corners = [(57, 18), (57, -11),
                  (40, 20), (40, -12)]

model = YOLO('best.pt')

cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize a dictionary to store camera coordinates for each class
class_coordinates = {}

initial_guess = np.array([0.0, 0.0, 0.0, 0.0])


# establish connection with arduino board for serial communication
arduino = serial.Serial(port='COM10',  baudrate=9600, timeout=.1)


# write-to/read-from arduino board
def write_read(x):
    x = x + '\r'
    arduino.write(bytes(x,  'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


# Main loop to continuously process the camera image
while True:

    pygame.init()

    coor_cup = []
    coor_obstacle = []
    coor_dispenser = []
    command_label = -1
    # Check for command

    th.record_audio_with_threshold(wav_file_path)

    transcription = asr_model.transcribe([wav_file_path])

    transcription = transcription[0].replace(
        "['", "").replace("']", "")
    print(transcription)
    flagis = nc.check_sentence(transcription, words_to_check)
    flaghy = nc.check_sentence(transcription, ["hey", "arm"])
    print(flagis, flaghy)
    if (flaghy == 1 or flaghy == 2):
        print("command now enters hereeeeeeee")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # Capture a single frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if ret:
            results = model.predict(frame, show=True, save=False
                                    )

        # Clear the dictionary at the beginning of each frame
        class_coordinates = {}

        # Process the detected objects
        for result in results:
            for box in result.boxes:
                class_id = box.cls[0].item()
                class_label = result.names[class_id]
                # Get the normalized bounding box coordinates
                x_center, y_center, norm_width, norm_height = box.xywh[0]

                # Store the camera coordinates in the dictionary
                if class_label not in class_coordinates:
                    class_coordinates[class_label] = []

                class_coordinates[class_label].append((x_center, y_center))

        target_class_label = "3"
        if target_class_label in class_coordinates:
            coor_dispenser = class_coordinates[target_class_label]

        target_class_label = "1"
        if target_class_label in class_coordinates:
            coor_cup = class_coordinates[target_class_label]

        target_class_label = "4"
        if target_class_label in class_coordinates:
            coor_obstacle = class_coordinates[target_class_label]

        coor_obstacle = tl.transform_coordinates(coor_obstacle)
        coor_cup = tl.transform_coordinates(coor_cup)
        print(f"this is cup coordinate: {coor_cup}")

        # choose glass to pick here ....................
        if coor_cup != []:
            to_pick = pl.pick_glass(coor_cup)
            x_cup, y_cup = to_pick
            print(F"XCUP : {x_cup}, Y:CUP{y_cup}")

       # problems are estimated here...................
        problem_count = pl.vision_problem_check(coor_cup)

        blockage = pl.block_check(coor_obstacle, region_corners)

        print(f"problemcount {problem_count}")
        print(f"blockage {blockage}")
        # vision problems .................
        if len(coor_dispenser) == 0:
            print("vision_obstructed")
            # Something is blocking the vision sensor. Could you please clear it
            # Load and play the audio file
            pygame.mixer.music.load(
                r'feedback_aud/obstruction.mp3')
            pygame.mixer.music.play()

            # Wait until the audio finishes playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Quit pygame
            pygame.quit()
        else:
            if problem_count == 0:

                if len(blockage) != 0:

                    for block in blockage:
                        print(block)
                        if block == True:
                            print("something is blocking the dispensor")
                            pygame.mixer.music.load(
                                r'feedback_aud/blocking dispenser.mp3')
                            pygame.mixer.music.play()
                            break

                elif len(blockage) == 0:
                    print("no problems")
                    print('Order your desired drink')

                    nc.record_and_save_audio(
                        5, wav_file_path, sample_rate=16000)

                    print(f"Audio recorded and saved at {wav_file_path}")

                    # Assuming asr_model and check_sentence() are defined elsewhere

                    transcription = asr_model.transcribe([wav_file_path])

                    transcription = transcription[0].replace(
                        "['", "").replace("']", "")
                    print(transcription)
                    flagis = nc.check_sentence(transcription, words_to_check)
                    flaghy = nc.check_sentence(transcription, ["hey", "arm"])
                    print(flagis, flaghy)
                    if (flaghy == 1 or flaghy == 2):
                        print("command now enters hereeeeeeee")
                    else:
                        continue

                    # arm moves here.....................................arm ......... arm ,,,,,,,,,,2
                    optimizedJointAngles, _ = mpc.invOpt(
                        0, 0, 0, 0, (x_cup/100), (y_cup/100), 0.01)

                    value = str(-optimizedJointAngles[0][0])+','+str(optimizedJointAngles[1][0])+','+str(
                        optimizedJointAngles[2][0])+','+str(-optimizedJointAngles[3][0])+','+'4'

                    print(f'this is angles: {optimizedJointAngles}')
                    # print(
                    # f'this is the drink (1-sprite, 2-water, 3-coffee, 4-orangeJ): {flagis}')
                    value1 = write_read(value)
                    print(value1)

                    time.sleep(5)

            elif problem_count == 1:
                print("glasses are unreachable")
                # Load and play the audio file
                pygame.mixer.music.load(
                    r'feedback_aud/unreachable.mp3')
                pygame.mixer.music.play()

                # Wait until the audio finishes playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                # Quit pygame
                pygame.quit()

            elif problem_count == 2:
                print("no glass available")
                # The drinking glasses are currently unavailable. Kindly restock them
                pygame.mixer.music.load(
                    r'feedback_aud/noglass.mp3')
                pygame.mixer.music.play()

                # Wait until the audio finishes playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                # Quit pygame

                pygame.quit()
    else:
        continue
