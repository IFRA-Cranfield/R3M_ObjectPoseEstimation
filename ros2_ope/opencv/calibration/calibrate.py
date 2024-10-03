#!/usr/bin/python3
import sys
sys.dont_write_bytecode = True

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
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ros2_ObjectPoseEstimation', 'ros2_ope', 'opencv', 'calibration')
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