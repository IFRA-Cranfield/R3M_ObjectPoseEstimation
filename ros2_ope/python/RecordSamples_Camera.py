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
# IFRA-Cranfield (2024). Object Detection and Pose Estimation within a Robot Cell. URL: https://github.com/IFRA-Cranfield/r3m_ObjectPoseEstimation

# RecordSamples_Gazebo.py
# This script records pictures of the desired objects within the Robot Cell (in GAZEBO) and stores them for future labelling.

# ===== IMPORT REQUIRED COMPONENTS ===== #
import os, sys, yaml, ast, time, cv2

# =============================================================================== #           
# EVALUATE INPUT ARGUMENTS:
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# ===================================================================================== #
# ======================================= MAIN ======================================== #
# ===================================================================================== #

def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> RecordSamples_Camera.py")
    print("")

    # Get USE-CASE Parameter value:
    USECASE = AssignArgument("usecase")
    if USECASE != None:
        print("Use-case selected -> " + USECASE)
    else:
        print("ERROR: usecase INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
    # Get sampleNUM Parameter value:
    sampleNUM = AssignArgument("sample")
    if sampleNUM is None:
        smpl = False
    elif sampleNUM.isdigit():
        smpl = True
    else:
        print("ERROR: sample INPUT ARGUMENT has not been correctly defined. Please try again.")
        print("Closing... BYE!")
        exit()
        
    print("")

    homeDIR = os.path.expanduser('~')
    folderPATH = os.path.join(homeDIR, USECASE)
    
    if not os.path.exists(folderPATH):
        
        os.mkdir(folderPATH)
        print("Folder /" + USECASE + " created successfully in your home directory.")
        
        if smpl:
            
            print("Samples will be generated starting from NUMBER -> " + sampleNUM + ".")
            print("")
            
            i = int(sampleNUM)
        
        else:
           
            print("")
            i = 1
               
    else:
        
        if smpl:
        
            print("Folder /" + USECASE + " already exists in your home directory.")
            print("Samples will be generated starting from NUMBER -> " + sampleNUM + ".")
            print("")
            
            i = int(sampleNUM)
            
        else:
        
            print("Folder /" + USECASE + " already exists in your home directory.")
            print("Please remove the folder and execute this script again.")
            print("Closing... BYE!")
            exit()
        
    # ========== SAMPLE COLLECTION ========== #
    
    # Initialise camera:
    print("Initialising CAMERA...")
    CAMERA = cv2.VideoCapture(0)
    if not CAMERA.isOpened():
        print("ERROR: CAMERA could not be opened.")
        print("Closing... BYE!")
        exit()
    else:
        print("CAMERA successfully initialised.")
        print("")
    
    while True:
        
        ret, frame = CAMERA.read()
        
        if not ret:
            print("ERROR: Connection with CAMERA lost.")
            print("Closing... BYE!")
            exit()
            
        OUTPUT = cv2.resize(frame, (1280, 720))
        cv2.imshow('=== FRAME CAPTURE: PRESS "P" TO SAVE IMAGE AND "E" TO EXIT ===', OUTPUT)
        
        key = cv2.waitKey(1)
        if key == ord('p'):
            
            imgPATH = folderPATH + "/" + str(i) + ".png"
            
            cv2.imwrite(imgPATH, frame)
            
            print("Frame captured from camera and saved to -> " + imgPATH)
            print("")
            
            i = i+1
            
        elif key == ord('e'):
            print("Program EXIT requested.")
            break

    print("Sample/Data collection successfully finished.")
    print("Closing... BYE!")
    exit()

if __name__ == '__main__':
    main()