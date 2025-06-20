#!/usr/bin/python3
import sys
sys.dont_write_bytecode = True

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

# PositionEstimation.py
# This script performs:
#   - Object Detection using a custom YOLO model.
#   - Object Position Estimation (center of the detected YOLO-based bounding box) by calculating the object's position relative to the OpenCV-ArUco marker.

# ===== IMPORT REQUIRED COMPONENTS ===== #
import os, sys

# Required to include ROS2 and its components:
import rclpy
from rclpy.node import Node

# ROS 2 data:
from objectpose_msgs.msg import ObjectPose
from sensor_msgs.msg import Image

# OpenCV:
import cv2
# ROS2 to OpenCV -> cv_bridge:
from cv_bridge import CvBridge, CvBridgeError

# YOLO:
from ultralytics import YOLO

# ARUCO:
from arucoMRKR import ros2ope_aruco
import numpy as np

# ================================================== #
# CLASS -> GazeboCamera:
class GazeboCamera(Node):

    def __init__(self):

        super().__init__("ros2ope_GzCAM")
        self.SubIMAGE = self.create_subscription(Image, "/camera/image_raw", self.CALLBACK_FN, 10)
        self.BRIDGE = CvBridge()

    def CALLBACK_FN(self, ROS2img):

        global Gz_CAM

        try:
            Gz_CAM = self.BRIDGE.imgmsg_to_cv2(ROS2img, "bgr8")
        except CvBridgeError as ERR:
            print("(cv_bridge): ERROR -> " + ERR) 
            print("")

# ===== EVALUATE INPUT ARGUMENTS ===== #         
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# ===== TRAIN MODEL ===== #
def main(args=None):

    global Gz_CAM

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("Object Detection and Pose Estimation in ROS 2.")
    print("Python script -> PositionEstimation_SingleMarker.py")
    print("")

    # Get ENVIRONMENT parameter value:
    ENVIRONMENT = AssignArgument("environment")
    if ENVIRONMENT == "gazebo" or ENVIRONMENT == "robot":
        print("Environment selected -> "+ ENVIRONMENT)
    else:
        print("")
        print("ERROR: environment INPUT ARGUMENT has not been properly defined (gazebo/robot). Please try again.")
        print("Closing... BYE!")
        exit()

    # Get CAMERANAME Parameter value:
    CAMName = AssignArgument("camera")
    if CAMName != None:
        print("Camera selected -> "+ CAMName)
    else:
        print("")
        print("ERROR: camera INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()

    # Get MODELname parameter value:
    MODELname = AssignArgument("model")
    if MODELname != None:
        print("YOLO model selected -> "+ MODELname)
    else:
        print("")
        print("ERROR: model INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()

    # Get VISUALIZE parameter value:
    VISUALIZE = AssignArgument("visualize")
    if VISUALIZE == "True" or VISUALIZE == "true":
        print("Visualize results -> True")
        print("")
        VISUALIZE = True
    elif VISUALIZE == "False" or VISUALIZE == "false" or VISUALIZE == None:
        print("Visualize results -> False")
        print("")
        VISUALIZE = False
    else:
        print("")
        print("ERROR: visualize INPUT ARGUMENT has not been properly defined (True/False). Please try again.")
        print("Closing... BYE!")
        exit()

    rclpy.init()

    # Initialise CAMERAS:
    if ENVIRONMENT == "gazebo":
        CAMERA = GazeboCamera()
    elif ENVIRONMENT == "robot":
        CAMERA = cv2.VideoCapture(0)

    # Load custom YOLO MODEL:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'R3M_ObjectPoseEstimation', 'r3m_ope',  'yolo', 'models')
    modelPATH = DIR + "/" + MODELname + ".pt"

    if not os.path.exists(modelPATH):
        print("Selected YOLO model file not found. Please double check and try again.")
        print("Closing... BYE!")
        exit()
    
    # YOLOmodel:
    YOLOmodel = YOLO(modelPATH)
    names = YOLOmodel.names
    print("The YOLO model will try to detect the following objects:")
    print(names)
    print("")

    ObjectList = []
    for key in names:
        ObjectList.append(names[key])

    # Initialise PUBLISHER NODE:
    PUBnode = rclpy.create_node("ros2ope_PUBLISHER")

    PUBList = {}
    for x in ObjectList:  
        TopicName = "/" + x + "/ObjectPoseEstimation"
        PUBList[x] = PUBnode.create_publisher(ObjectPose, TopicName, 10)

    # ARUCO:
    ARUCO = ros2ope_aruco(CAMName, 0.1)

    # Run execution-PREDICTION INFERENCE:
    while True:
        
        if ENVIRONMENT == "gazebo":
            rclpy.spin_once(CAMERA)
            inputIMG = Gz_CAM
        elif ENVIRONMENT == "robot":
            ret, inputIMG = CAMERA.read()

        if inputIMG is not None:
            
            # A. DETECT ARUCO and RETURN ARUCO POSITION:
            ARUCO_RES = ARUCO.EXECUTE(inputIMG)

            if not ARUCO_RES["Success"]:
                print("")
                print("ERROR: ArUco tag detection lost. Please try again.")
                print("Closing... BYE!")
                exit()
            else:
                inputIMG = ARUCO_RES["Frame"]
                ARUCOx = ARUCO_RES["x"]
                ARUCOy = ARUCO_RES["y"]
                ARUCOz = ARUCO_RES["z"]
                ROTm = ARUCO_RES["R"]

            # B. EXECUTE YOLO-based object detection:
            PREDICTION = YOLOmodel.predict(inputIMG, verbose=False)
            
            for R in PREDICTION:

                boxes = R.boxes

                for box in boxes:

                    # Get NAME of the detected OBJECT:
                    C = int(box.cls)
                    ObjectName = YOLOmodel.names[C]

                    # Calculate CENTER of BB:
                    B = box.xyxy[0]
                    BBx = (B[0] + B[2])/2
                    BBy = (B[1] + B[3])/2

                    # CALCULATE DEPTH of OBJECT:
                    OBJz = ARUCOz

                    # CALCULATE x and y COORDINATES of OBJECT:
                    OBJx = (BBx - ARUCO.camera_matrix[0, 2]) * OBJz / ARUCO.camera_matrix[0, 0]
                    OBJy = (BBy - ARUCO.camera_matrix[1, 2]) * OBJz / ARUCO.camera_matrix[1, 1]

                    print("=== CAMERA COORDINATES ===")
                    print("ARUCO -> X: " + str(ARUCOx) +", Y: " + str(ARUCOy) + ", Z: " +str(ARUCOz))
                    print("NAME: " + ObjectName + " X: " + str(OBJx.item()) +", Y: " + str(OBJy.item()) + ", Z: " + str(OBJz.item()))
                    print("")
                    
                    (gOBJx, gOBJy, gOBJz) = np.array([OBJx.item(), OBJy.item(), OBJz.item()]) @ ROTm
                    (gARUCOx, gARUCOy, gARUCOz) = np.array([ARUCOx, ARUCOy, ARUCOz]) @ ROTm
                    
                    print("=== GLOBAL COORDINATES ===")
                    print("ARUCO -> X: " + str(gARUCOx.item()) +", Y: " + str(gARUCOy.item()) + ", Z: " +str(gARUCOz.item()))
                    print("NAME: " + ObjectName + " X: " + str(gOBJx.item()) +", Y: " + str(gOBJy.item()) + ", Z: " + str(gOBJz.item()))
                    print("")
                    
                    # CALCULATE OBJECT COORDINATES RELATIVE TO ARUCO:
                    X = float(gOBJx.item() - gARUCOx.item())
                    Y = float(gOBJy.item() - gARUCOy.item())
                    Z = float(gOBJz.item() - gARUCOz.item())
                    
                    # PUBLISH POSE:
                    POSE = ObjectPose()
                    POSE.objectname = ObjectName
                    POSE.x = X
                    POSE.y = Y
                    POSE.z = Z

                    PUBList[ObjectName].publish(POSE)

                    # To visualize BoundingBoxes:
                    cv2.rectangle(inputIMG, (int(B[0]), int(B[1])), (int(B[2]), int(B[3])), (0,0,0), 2)
                    cv2.circle(inputIMG, (int(BBx), int(BBy)), radius=3, color=(0,255,0), thickness=-1)

                    # To visualize pose next to objects:
                    LABEL = ObjectName + " -> x: " + str(X) + ", y: " + str(Y)
                    cv2.putText(inputIMG, LABEL, (int(B[0]), int(B[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
                    
                print("")

            if VISUALIZE:
                
                WINDOW = cv2.resize(inputIMG, (1280, 720))
                TITLE = "YOLO MODEL -> " + MODELname + " PREDICTION RESULTS and OBJECT POSITION ESTIMATION"
                cv2.imshow(TITLE, WINDOW)

                key = cv2.waitKey(1)
                if key == ord('e'):
                    cv2.destroyWindow(TITLE)
                    break

    print("")
    print("Object POSITION ESTIMATION finalised.")
    print("Closing... BYE!")

    if ENVIRONMENT == "gazebo":
        rclpy.shutdown()

if __name__ == '__main__':
    main()