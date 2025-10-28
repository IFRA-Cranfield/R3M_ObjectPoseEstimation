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

# IMPORT:
import numpy as np
import cv2 as cv
import os, yaml
 
# ============================================================= #           
# EVALUATE INPUT ARGUMENTS:
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)
        
# ============================================================= #     
def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> calibration.py")
    print("")

    # === INITIAL CONDITIONS === #
    # Get CAMERA Parameter value:
    CAMERA = AssignArgument("camera")
    if CAMERA != None:
        print("Camera selected -> "+ CAMERA)
    else:
        print("")
        print("ERROR: camera INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
    # Get NUMBER Parameter value:
    NUMBER = AssignArgument("num")
    N = 0
    if NUMBER.isdigit():
        print("Sample number -> "+ NUMBER)
        print("")
        N = int(NUMBER)
    else:
        print("")
        print("ERROR: num INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()

    # Termination criteria:
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Prepare object points:
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:6,0:9].T.reshape(-1,2) * 0.05 # 0.05m is the square size (5cm).
    
    # Arrays to store object points and image points from all the images:
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    # IMAGES ARRAY:
    images = []

    # DIRECTORY:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'R3M_ObjectPoseEstimation', 'r3m_ope', 'opencv', 'calibration')
    PATH = DIR + "/" + CAMERA + "/samples/"

    # Load images:
    for i in range(1,N+1):
        imgPATH = PATH + str(i) + ".png"
        img = cv.imread(imgPATH)
        if img is not None:
            images.append(img)
    
    for fname in images:
        img = fname
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (6,9), None)
    
        # If found, add object points, image points (after refining them):
        if ret == True:
            
            print("Chessboard corners found.")
            
            objpoints.append(objp)
            imgpoints.append(corners)
            cv.drawChessboardCorners(img, (6,9), corners, ret)
            
            while True:
                cv.imshow('img', img)
                key = cv.waitKey(1)
                if key == ord('e'):
                    cv.destroyWindow('img')
                    break
        
        else:
            print("Chessboard corners not found.")
                    
    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Print the camera matrix and distortion coefficients:
    print("Camera Matrix:\n", mtx)
    print("Distortion Coefficients:\n", dist)

    # SAVE PARAMETERS:
    data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
    yamlPATH =  DIR + "/" + CAMERA + "/calibration.yaml"
    
    with open(yamlPATH, "w") as f:
        yaml.dump(data, f)

if __name__ == '__main__':
    main()