#!/usr/bin/python3

# ===================================== COPYRIGHT ===================================== #
#                                                                                       #
#  IFRA (Intelligent Flexible Robotics and Assembly) Group, CRANFIELD UNIVERSITY        #
#  Created on behalf of the IFRA Group at Cranfield University, United Kingdom          #
#  E-mail: IFRA@cranfield.ac.uk                                                         #
#                                                                                       #
#  Licensed under the Apache-2.0 License.                                               #
#  You may not use this file except in compliance with the License.                     #
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0  #
#                                                                                       #
#  Unless required by applicable law or agreed to in writing, software distributed      #
#  under the License is distributed on an "as-is" basis, without warranties or          #
#  conditions of any kind, either express or implied. See the License for the specific  #
#  language governing permissions and limitations under the License.                    #
#                                                                                       #
#  IFRA Group - Cranfield University                                                    #
#  AUTHORS: Mikel Bueno Viso         - Mikel.Bueno-Viso@cranfield.ac.uk                 #
#           Seemal Asif              - s.asif@cranfield.ac.uk                           #
#           Phil Webb                - p.f.webb@cranfield.ac.uk                         #
#                                                                                       #
#  Date: November, 2024.                                                                #
#                                                                                       #
# ===================================== COPYRIGHT ===================================== #

# ======= CITE OUR WORK ======= #
# You can cite our work with the following statement:
# IFRA-Cranfield (2024). Object Detection and Pose Estimation within a Robot Cell. URL: https://github.com/IFRA-Cranfield/R3M_ObjectPoseEstimation

# train.py
# This script trains a RoboFlow DB to create a specific YOLO detection model.

# ===== IMPORT REQUIRED COMPONENTS ===== #
from ultralytics import YOLO
import os

# ===== TRAIN MODEL ===== #
def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> train.py")
    print("")

    # Load pre-defined YOLO model:
    model = YOLO("yolo11n.pt")

    # Load custom DB:
    DIR = os.path.join(os.path.expanduser('~'), 'DB_RoboFlow')
    PATH = DIR + "/data.yaml"

    # Train custom DB:
    TRAINING = model.train(
        data=PATH,
        epochs=50,
    )

    print("YOLO model training successfully finished.")
    print("Closing... BYE!")
    exit()

if __name__ == '__main__':
    main()