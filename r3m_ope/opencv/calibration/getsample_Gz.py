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
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'R3M_ObjectPoseEstimation', 'r3m_ope', 'opencv', 'calibration')
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