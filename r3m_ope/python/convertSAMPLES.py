#!/usr/bin/python3
import sys
sys.dont_write_bytecode = True

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

# convertSAMPLES.py
# This script converts sample images, by cutting the picture to the ArUco grid-marked zone.

# ===== IMPORT REQUIRED COMPONENTS ===== #
import os, sys

# OpenCV:
import cv2

# ARUCO:
from ament_index_python.packages import get_package_share_directory
PATH_F = os.path.join(get_package_share_directory("r3m_ope"), 'opencv')
sys.path.append(PATH_F)
from arucoMRKR import arucoGRID
from gridPARAMS import grid

# ===== EVALUATE INPUT ARGUMENTS ===== #         
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# ===== TRAIN MODEL ===== #
def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> convertSAMPLES.py")
    print("")

    # Get FOLDER parameter value:
    FOLDER = AssignArgument("SampleFolder")
    if FOLDER != None:
        print("SAMPLE FOLDER selected -> "+ FOLDER)
    else:
        print("")
        print("ERROR: SampleFolder INPUT ARGUMENT has not been properly defined. Please try again.")
        print("Closing... BYE!")
        exit()

    # Get CELLname parameter value:
    CELLname = AssignArgument("cell")
    if CELLname != None:
        print("Cell model selected, for correction application -> "+ CELLname)
    else:
        print("")
        print("ERROR: cell INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
        
    # ARUCO:
    GRID = grid(CELLname)
    ARUCO = arucoGRID(GRID.H,GRID.W)

    # CHECK if -> Folder exists:
    print("")
    homeDIR = os.path.expanduser('~')
    folderPATH = os.path.join(homeDIR, FOLDER)
    newfolderPATH = os.path.join(homeDIR, FOLDER + "_NEW")
    
    if not os.path.exists(folderPATH):
        print("")
        print("ERROR: The selected folder does not exist. Please try again.")
        print("Closing... BYE!")
        exit()
    
    else:

        os.mkdir(newfolderPATH)
        print("")
        print("Selected folder found, and /_converted folder created successfully in your home directory. Converting images...")
        print("")

        images = os.listdir(folderPATH)
        for image in images:

            imgPATH = os.path.join(folderPATH, image)
            IMG = cv2.imread(imgPATH)

            ARUCO_RES = ARUCO.detectGRID(IMG)
            if not ARUCO_RES["Success"]:
                print("ERROR: ArUco grid not detected in image -> " + image + ". Image not converted!")
                print("")
            else:
                convertedIMG = ARUCO_RES["GRID"]
                filePATH = os.path.join(newfolderPATH, image)
                cv2.imwrite(filePATH, convertedIMG)
                print(filePATH + " converted image created!")

    print("")
    print("All images converted from folder -> " + folderPATH + " to folder -> " + newfolderPATH + ". Closing... BYE!")
    exit()

if __name__ == '__main__':
    main()