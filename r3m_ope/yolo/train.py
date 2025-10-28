#!/usr/bin/python3

# ===================================== COPYRIGHT ===================================== #
#                                                                                       #
#                           ***** R3M Research Project *****                            #
#                                                                                       #
#  Reconfigurable Robotics for Responsive Manufacture (R3M) is a three-year research    #
#  project co-funded by the EPSRC and a group of Universities in the UK. The project    #
#  aims to develop new methods to enable the rapid and automated configuration of       #
#  robot manufacturing cells to allow mixed and variable products and processes to be   #
#  performed using the same basic hardware, the R3M Cell.                               #
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
#  R3M Project Consortium:                                                              #
#                                                                                       #
#  AUTHORS (Cranfield University):                                                      #
#           Mikel Bueno Viso       - Mikel.Bueno-Viso@cranfield.ac.uk                   #
#           Dr. Seemal Asif        - s.asif@cranfield.ac.uk                             #
#           Prof. Phil Webb        - p.f.webb@cranfield.ac.uk                           #
#                                                                                       #
#  AUTHORS (Loughborough University):                                                   #
#           Dr. Paul Anandan       - p.d.anandan2@lboro.ac.uk                           #
#           Dr. Pedro Ferreira     - P.Ferreira@lboro.ac.uk                             #
#           Prof. Niels Lohse      - n.lohse@lboro.ac.uk                                #
#                                                                                       #
#  AUTHORS (Sheffield University):                                                      #
#           Yue Yao                - yue.yao@sheffield.ac.uk                            #
#           Dr. Ze Zhang           - ze.zhang@sheffield.ac.uk                           #
#           Dr. Windo Hutabarat    - w.hutabarat@sheffield.ac.uk                        #
#           Prof. Ashutosh Tiwari  - a.tiwari@sheffield.ac.uk                           #
#                                                                                       #
#  AUTHORS (AMRC - Sheffield):                                                          #
#           Dr. Gautham Ragunathan - g.ragunathan@amrc.co.uk                            #
#           Dr. Lloyd Tinkler      - l.tinkler@amrc.co.uk                               #
#                                                                                       #
#  Date: February, 2025.                                                                #
#                                                                                       #
# ===================================== COPYRIGHT ===================================== #

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