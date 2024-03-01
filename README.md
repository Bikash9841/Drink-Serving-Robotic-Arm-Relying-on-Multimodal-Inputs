# Learning-based Model Predictive Controller for Drink Dispensing Robotic Arm Relying on Multimodal Inputs

The project presents a voice-controlled four degrees of freedom robotic arm to
automate the monotonous task of drink serving in a bartender domain. The system also
consists of vision sensor to localize the glasses, drink dispenser and any obstacles
within the robot’s workspace. It incorporates a Squeezeformer architecture for voice
command recognition where customers can request drinks using voice commands, You
Only Look Once (YOLO) architecture to detect and localize the glasses, Model
Predictive Control (MPC) for precise movement of robotic arm and drink dispenser to
dispense the ordered drink by the customer. The whole system is realized in virtual as
well as physical environment. CoppeliaSim is used to design the virtual environment
where the robotic arm designed in Fusion360 is imported. The physical robot
implements the cyclodial drive to increase the output torque of bipolar Nema17 motor
and Gradient Descent method is used to perform the inverse kinematics calculations.
The object detection model provides the mAP50 score of 0.989 for virtual environment
and mAP50 score of 0.989 for physical environment. Also, the speech recognition
model generated a Character Error Rate (CER) of 3.47% and Word Error Rate (WER)
of 4.46% on training dataset.
