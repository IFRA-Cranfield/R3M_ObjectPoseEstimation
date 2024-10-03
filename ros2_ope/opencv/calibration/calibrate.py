#!/usr/bin/python3
import sys
sys.dont_write_bytecode = True

# IMPORT:
import numpy as np
import cv2 as cv
import os
 
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
    objp = np.zeros((7*10,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:10].T.reshape(-1,2) * 0.05 # 0.05m is the square size (5cm).
    
    # Arrays to store object points and image points from all the images:
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    # IMAGES ARRAY:
    images = []

    # DIRECTORY:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ros2_ObjectPoseEstimation', 'ros2_ope', 'opencv', 'calibration')
    PATH = DIR + "/" + CAMERA + "/samples/"

    # Load images:
    for i in range(1,N):
        imgPATH = PATH + str(i) + ".png"
        img = cv.imread(imgPATH)
        if img is not None:
            images.append(img)
    
    for fname in images:
        img = fname
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7,10), None)
    
        # If found, add object points, image points (after refining them):
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            cv.drawChessboardCorners(img, (7,10), corners, ret)
            cv.imshow('img', img)
            cv.waitKey(0)
    
    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Print the camera matrix and distortion coefficients:
    print("Camera Matrix:\n", mtx)
    print("Distortion Coefficients:\n", dist)

    # Save the calibration parameters:
    np.savez("calibration_data.npz", mtx=mtx, dist=dist)

    cv.destroyAllWindows()

    cv.destroyAllWindows()

if __name__ == '__main__':
    main()