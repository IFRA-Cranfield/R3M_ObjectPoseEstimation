#!/usr/bin/python3
import sys
sys.dont_write_bytecode = True

# IMPORT:
import time, os

# IMPORT OpenCV:
import cv2
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
# Function -> Save IMAGE:
def saveIMG(i, PATH, IMG):
    imgNAME = PATH + str(i) + ".png"
    cv2.imwrite(imgNAME, IMG)
    print("Image -> " + str(imgNAME) + " saved.")

# ========================================================================================= #           
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
    print("Python script -> getsample_Gazebo.py")
    print("")

    # Initialise ROS2:
    rclpy.init(args=None)
    camTOPIC = "camera/image_raw"

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

    # DIRECTORY:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ros2_ObjectPoseEstimation', 'ros2_ope', 'opencv', 'calibration')
    PATH = DIR + "/" + CAMERA

    # DIRECTORY where samples will be saved:
    imgPATH = PATH + "/samples/"

    # RECORD IMAGE:
    IMG = toCV2_fromTOPIC(camTOPIC)
    saveIMG(NUMBER, imgPATH, IMG)

    rclpy.shutdown()
    print("")
    print("Closing... BYE!")
    exit()

if __name__ == '__main__':
    main()