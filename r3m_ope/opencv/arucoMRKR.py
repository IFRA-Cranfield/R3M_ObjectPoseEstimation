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

# arucoMRKR.py
# This script contains the ros2ope_ARUCO class and its functions.

# ===== IMPORT REQUIRED COMPONENTS ===== #
import os, cv2, yaml, time
import scipy.spatial.transform as spt
import numpy as np
from cv_bridge import CvBridge

# Import ROS 2:
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# =========================================== #
# Image SUBSCRIBER class:
class imgSUB(Node):
    
    def __init__(self, TOPICNAME):
        
        # Declare NODE:
        super().__init__("r3m_imgSUB")
        
        # Declare SUBSCRIBER:
        self.subscription = self.create_subscription(
            Image,                                             
            TOPICNAME, 
            self.listener_callback, 
            1) 
        self.subscription 
        
        self.IMAGE = Image()
        self.BRIDGE = CvBridge()

    def listener_callback(self, IMG):
        self.IMAGE = IMG

    def toCV2_fromTOPIC(self):
        IMG_CV2 = self.BRIDGE.imgmsg_to_cv2(self.IMAGE, "passthrough")
        return(IMG_CV2)
    
# =========================================== #
# FUNCTION -> GET image (CV2 format) from ROS 2 topic:
def toCV2_fromTOPIC(TOPIC):
    
    # INITIALISE CLASSES:
    BRIDGE = CvBridge()
    SUB = imgSUB(TOPIC)
    
    # Get IMAGE (sensor_msgs/Image format) from ROS 2 TOPIC:
    T = time.time() + 0.25
    while time.time() < T:
        rclpy.spin_once(SUB)   
    IMG_ROS2 = SUB.IMAGE
    
    # CONVERT:
    IMG_CV2 = BRIDGE.imgmsg_to_cv2(IMG_ROS2, "bgr8")
    
    # Delete CLASS INSTANCES:
    del BRIDGE, SUB
    
    # Return IMAGE (OpenCV format):
    return(IMG_CV2)

# =========================================== #
# ARUCO class:
class ros2ope_aruco():

    def __init__(self, CAMERA, length):

        self.ARUCOdict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)

        self.CAMERA = CAMERA
        self.camera_matrix = None
        self.dist_coeffs = None
        self.loadCALIBPARAMS()
        
        self.ARUCOlength = length # (m)

    def loadCALIBPARAMS(self):

        DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'R3M_ObjectPoseEstimation', 'r3m_ope', 'opencv', 'calibration')
        
        yamlPATH =  DIR + "/" + self.CAMERA + "/calibration.yaml"
        with open(yamlPATH) as f:
            loaded_dict = yaml.load(f, Loader=yaml.FullLoader)

        self.camera_matrix = np.array(loaded_dict.get('camera_matrix'))
        self.dist_coeffs = np.array(loaded_dict.get('dist_coeff'))
    
        return()
    
    def detectARUCO(self, IMG):

        gray = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
        parameters = cv2.aruco.DetectorParameters()
        corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, self.ARUCOdict, parameters=parameters)

        return(corners, ids)
    
    def getARUCOpose(self, corners, ids):

        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, self.ARUCOlength, self.camera_matrix, self.dist_coeffs)
        
        return(rvecs, tvecs)
    
    def getARUCOposition(self, tvec, rvec):
        
        x, y, z = tvec[0]
        
        R, _ = cv2.Rodrigues(rvec[0])
        xG, yG, zG = tvec[0] @ R
        
        print("ARUCO marker detected.")
        print("Relative pose to camera, in camera coordinates:")
        print(" - x: " + str(x))
        print(" - y: " + str(y))
        print(" - z: " + str(z))
        
        print("Relative pose to camera, in global coordinates:")
        print(" - x: " + str(xG))
        print(" - y: " + str(yG))
        print(" - z: " + str(zG))
        print("")

        return(x, y, z, R)
    
    def EXECUTE(self, IMG):

        RES = {}
        RES["Success"] = False
        RES["Frame"] = None
        RES["x"] = None
        RES["y"] = None
        RES["z"] = None

        # Detect ARUCO:
        corners, ids = self.detectARUCO(IMG)

        if ids is not None:
        
            # GET ARUCO POSE:
            rvecs, tvecs = self.getARUCOpose(corners, ids)

            for i in range(len(ids)):

                rvec = rvecs[i]
                tvec = tvecs[i]

                # Draw ArUco markers on the image:
                frame = cv2.aruco.drawDetectedMarkers(IMG, corners)

                # Draw FRAME AXES:
                if (rvec is not None) and (tvec is not None):
                    cv2.drawFrameAxes(frame, self.camera_matrix, self.dist_coeffs, rvec, tvec, self.ARUCOlength * 0.5)

                # Get POSITION of ARUCO marker:
                x, y, z, R = self.getARUCOposition(tvec, rvec)

                RES["Success"] = True
                RES["Frame"] = frame
                RES["x"] = x
                RES["y"] = y
                RES["z"] = z
                RES["R"] = R

                return(RES)
        
        else:
            return(RES)
        
# =========================================== #
# arucoGRID class:
class arucoGRID():
    
    def __init__(self, H, W):

        self.ARUCOdict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
        self.params = cv2.aruco.DetectorParameters()
        
        self.H = H # Height of ARUCO-GRID (mm)
        self.W = W # Width of ARUCO-GRID (mm)
        
    def detectGRID(self, FRAME):
        
        RES = {}
        RES["GRID"] = None
        RES["Success"] = False
        
        # Detect ArUco markers:
        corners, ids, rejected_img_points = cv2.aruco.detectMarkers(FRAME, self.ARUCOdict, parameters=self.params)
        
        if ids is not None:

            if len(ids) is not 4:
                return(RES)
            
            # cv2.aruco.drawDetectedMarkers(FRAME, corners, ids)
        
            # Calibration process:
            src = np.zeros((4, 2), dtype=np.float32)  # Points of the corners from the input image.
            dst = np.array([[0.0, 0.0], [self.W, 0.0], [0.0, self.H], [self.W, self.H]], dtype=np.float32)  # Points calibrated with w and h.
            
            poly_corner = np.zeros((4, 3), dtype=np.int32)
            
            # Get the first corner & ID of the markers:
            for i in range(4):
                poly_corner[i][0] = int(ids[i][0])
                poly_corner[i][1] = int(corners[i][0][0][0])
                poly_corner[i][2] = int(corners[i][0][0][1])

            # Arrange by ID: 
            for i in range(3):
                for j in range(i + 1, 4):
                    if poly_corner[i][0] > poly_corner[j][0]:
                        for k in range(3):
                            aux = poly_corner[i][k]
                            poly_corner[i][k] = poly_corner[j][k]
                            poly_corner[j][k] = aux

            # Get the source vector:
            for i in range(4):
                src[i] = np.array([poly_corner[i][1], poly_corner[i][2]], dtype=np.float32)

            # Get the transform matrix:
            perspTransMatrix = cv2.getPerspectiveTransform(src, dst)
            
            # Get the TRANSFORMED IMAGE:
            perspectiveImg = cv2.warpPerspective(FRAME, perspTransMatrix, (int(self.W), int(self.H)))
            
            # RESULT:
            RES["GRID"] = perspectiveImg
            RES["Success"] = True
            return(RES)
        
        else:
            
            return(RES)
    
# ===================================================================================== #
# ======================================= MAIN ======================================== #
# ===================================================================================== #

def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> arucoMRKR.py")
    print("")

    rclpy.init(args=None)
    camTOPIC = "camera/image_raw"
    CAMERA = "lenovoFHD_gazebo"
    ARUCO = ros2ope_aruco(CAMERA, 0.1)

    while True:
    
        # GET IMAGE, from GAZEBO:
        IMG = toCV2_fromTOPIC(camTOPIC)

        # Detect ARUCO:
        corners, ids = ARUCO.detectARUCO(IMG)
        
        if ids is not None:
        
            # GET ARUCO POSE:
            rvecs, tvecs = ARUCO.getARUCOpose(corners, ids)

            for i in range(len(ids)):

                rvec = rvecs[i]
                tvec = tvecs[i]

                # Draw ArUco markers on the image:
                frame = cv2.aruco.drawDetectedMarkers(IMG, corners)

                # Draw FRAME AXES:
                if (rvec is not None) and (tvec is not None):
                    cv2.drawFrameAxes(frame, ARUCO.camera_matrix, ARUCO.dist_coeffs, rvec, tvec, ARUCO.ARUCOlength * 0.5)

                # Get POSITION of ARUCO marker:
                x, y, z, R = ARUCO.getARUCOposition(tvec, rvec)

            cv2.imshow('=== ARUCO MARKER DETECTION and POSE ESTIMATION ===', frame)

            key = cv2.waitKey(1)
            if key == ord('e'):
                cv2.destroyAllWindows()
                break

        else:
            print("ARUCO marker not detected.")
            break

    rclpy.shutdown()
    print("")
    print("Closing... BYE!")
    exit()

if __name__ == '__main__':
    main()