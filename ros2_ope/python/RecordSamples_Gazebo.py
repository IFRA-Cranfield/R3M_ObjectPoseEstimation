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
# IFRA-Cranfield (2024). Object Detection and Pose Estimation within a Robot Cell. URL: https://github.com/IFRA-Cranfield/ros2_ObjectPoseEstimation

# RecordSamples_Gazebo.py
# This script records pictures of the desired objects within the Robot Cell (in GAZEBO) and stores them for future labelling.

# ===== IMPORT REQUIRED COMPONENTS ===== #
import os, sys, yaml, ast, time, cv2
# Required to include ROS2 and its components:
import rclpy
from rclpy.node import Node
# Import /SpawnEntity Gazebo ROS2 Service:
from gazebo_msgs.srv import SpawnEntity
# Import /DeleteEntity Gazebo ROS2 Service:
from gazebo_msgs.srv import DeleteEntity
# Import ROS2 Messages:
from geometry_msgs.msg import Pose
# Required to load urdf file:
from ament_index_python.packages import get_package_share_directory
import xacro
# Required to spawn cube at a random pose:
import random
# Required for image conversion:
from imgROS2 import toCV2_fromTOPIC, saveIMG

# =============================================================================== #
# CLASS -> EntityGz (Gazebo):
class EntityGz(Node):

    def __init__(self):

        super().__init__('ros2_ope_EntityClient')
        
        self.cli_SPAWN = self.create_client(SpawnEntity, "/spawn_entity")
        self.req_SPAWN = SpawnEntity.Request()

        self.cli_DELETE = self.create_client(DeleteEntity, "/delete_entity")
        self.req_DELETE = DeleteEntity.Request()

    def SPAWN(self, PACKAGE, URDFName, NAME, POSE):

        # Load URDF:
        urdf_file = URDFName + ".urdf"
        urdf_file_path = os.path.join(get_package_share_directory(PACKAGE), 'urdf', 'objects', urdf_file)
        xacro_file = xacro.process_file(urdf_file_path, mappings={"name": NAME})

        # Arguments:
        self.req_SPAWN.name = NAME
        self.req_SPAWN.xml = xacro_file.toxml()

        # POSE:
        self.req_SPAWN.initial_pose.position.x = POSE.position.x
        self.req_SPAWN.initial_pose.position.y = POSE.position.y
        self.req_SPAWN.initial_pose.position.z = POSE.position.z
        self.req_SPAWN.initial_pose.orientation.x = POSE.orientation.x
        self.req_SPAWN.initial_pose.orientation.y = POSE.orientation.y
        self.req_SPAWN.initial_pose.orientation.z = POSE.orientation.z
        self.req_SPAWN.initial_pose.orientation.w = POSE.orientation.w

        # Assign result value:
        self.future_SPAWN = self.cli_SPAWN.call_async(self.req_SPAWN)

    def DELETE(self, NAME):
        
        # Arguments:
        self.req_DELETE.name = NAME
        
        # Assign result value:
        self.future_DELETE = self.cli_DELETE.call_async(self.req_DELETE)

    def GetObjectSpawnPose(self, INPUT):

        POSE = Pose()
        POSEdict = {}

        for key, value in INPUT.items():

            if isinstance(value, str):
                LIM = ast.literal_eval(value)
                VAL = round(random.uniform(LIM["min"],LIM["max"]), 2)
                
                POSEdict[key] = VAL
                
            else: 
                POSEdict[key] = INPUT[key]

        POSE.position.x = POSEdict["x"]
        POSE.position.y = POSEdict["y"]
        POSE.position.z = POSEdict["z"]
        POSE.orientation.x = POSEdict["qx"]
        POSE.orientation.y = POSEdict["qy"]
        POSE.orientation.z = POSEdict["qz"]
        POSE.orientation.w = POSEdict["qw"]

        return(POSE)

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
    print("Python script -> RecordSamples_Gazebo.py")
    print("")

    # Initialise ROS2:
    rclpy.init(args=None)
    ENTITYClient = EntityGz()
    camTOPIC = "camera/image_raw"

    # === INITIAL CONDITIONS === #
    # Get USE-CASE Parameter value:
    USECASE = AssignArgument("usecase")
    if USECASE != None:
        print("Use-case selected -> "+ USECASE)
    else:
        print("")
        print("ERROR: usecase INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
    # Get ITERATIONS Parameter value:
    ITERATIONS = AssignArgument("iterations")
    N = 0
    if ITERATIONS.isdigit():
        print("Number of iterations defined -> "+ ITERATIONS)
        print("")
        N = int(ITERATIONS)
    else:
        print("")
        print("ERROR: iteration INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()

    # DIRECTORY:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ros2_ObjectPoseEstimation', 'yolov8', 'samples')
    PATH = DIR + "/" + USECASE + ".yaml"

    # DIRECTORY where samples will be saved:
    imgPATH = os.path.join(os.path.expanduser('~')) + "/" + USECASE 

    if not os.path.exists(PATH):
        print("Sample/Data collection config file does not exist for the specified use-case. Please double check and try again.")
        print("Closing... BYE!")
        exit()

    # READ config.yaml file:
    with open(PATH, 'r') as YAML:
        configYAML = yaml.safe_load(YAML)

    iVAR = 0
    # EXECUTE SAMPLE COLLECTION:
    for VARIANT in configYAML["VARIANTS"]:

        iVAR = iVAR + 1

        print("====================")
        print("Executing VARIANT N" + str(iVAR) + "...")
        print("")

        j = 0
        while j<20:

            j = j + 1

            # 1. SPAWN OBJECTS:
            for OBJECT in VARIANT["Objects"]:
                POSE = ENTITYClient.GetObjectSpawnPose(OBJECT["pose"])
                ENTITYClient.SPAWN(OBJECT["pkg"], OBJECT["urdf"], OBJECT["name"], POSE)
                time.sleep(1.0)

            # 2. RECORD IMAGE:
            IMG = toCV2_fromTOPIC(camTOPIC)
            saveIMG(iVAR, j, imgPATH, IMG)

            time.sleep(1.0)

            # 3. DELETE OBJECTS:
            for OBJECT in VARIANT["Objects"]:
                ENTITYClient.DELETE(OBJECT["name"])
                time.sleep(1.0)

        print("")
        print("Samples recorded for VARIANT N" + str(iVAR) + ".")
        print("")

    print("Sample/Data collection successfully finished.")
    print("Closing... BYE!")
    exit()

if __name__ == '__main__':
    main()