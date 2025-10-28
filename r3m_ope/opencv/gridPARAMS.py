#!/usr/bin/python3

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

import sys
import cv2
import numpy as np
sys.dont_write_bytecode = True

class grid():
    
    def __init__(self, CELL):
        
        self.CELL = CELL
        
        if self.CELL == "irb120-cranfield":
            self.H = 750
            self.W = 1050
        elif self.CELL == "ur3-cranfield":
            self.H = 415
            self.W = 550
        elif self.CELL == "irb1200-amrc":
            self.H = 1100
            self.W = 950
        
        else:
            print("Cell name not valid. Please try again, bye!")
            exit()
          
    def applyCORRECTION(self, x,y, ENV):
        
        # CORRECTION ONLY:
        if self.CELL == "irb120-cranfield":
            
            xDIF = 0.70-x
            yDIF = 0.525-y

            if ENV == "gazebo":
            
                if xDIF >= 0:
                    x = x + abs(xDIF)*1.5/100  
                else:
                    x = x
                    
                if yDIF >= 0:
                    y = y + abs(yDIF)*1.5/100  
                else:
                    y = y - abs(yDIF)*1.5/100
            
            else:

                if xDIF >= 0:
                    x = x + abs(xDIF)*1.8/100  
                else:
                    x = x
                    
                if yDIF >= 0:
                    y = y + abs(yDIF)*3.0/100  
                else:
                    y = y - abs(yDIF)*5.5/100

            return(x,y)
        
        # TRANSFORM + CORRECTION:
        
        if self.CELL == "ur3-cranfield":

            xo = x
            yo = y
            
            # TRANSFORMATION -> From ORIGIN (0,0) to ArUco Grid ORIGIN (0.275,-0.035):
            x = -0.275 + yo
            y = 0.38 - xo

            # CORRECTION:
            Yc = y + y*0.002
            
            return(x,y)
        
        if self.CELL == "irb1200-amrc":
            
            # To calculate differences:
            xDIF = 1.1 - x
            yDIF = 0.475 - y
            
            # TRANSFORMATION -> From ORIGIN (0,0) to ArUco Grid ORIGIN (0.275,-0.375):
            x = 0.125 + x
            y = -0.375 + y

            if ENV == "gazebo":
            
                x = x + 0.003 + xDIF * 0.02
            
                if y >= 0.1:
                    y = y - abs(yDIF) * 0.025
                else:
                    y = y + abs(yDIF) * 0.025
            
            else:

                x = x + 0.004 + xDIF * 0.05
                y = y + 0.002
            
            return(x,y)
                
        else:
            
            return(x,y)
        
    def extraSTEP(self, IMAGE, OBJECT, BBx, BBy, env):

        if env == "gazebo":

            if OBJECT == "TopCylinder" or OBJECT == "BaseCylinder":

                GREY_THRESHOLD = 195

                IMG = IMAGE.copy()
                    
                totalPXL = IMG.size
                greyPXL = np.sum(IMG >= GREY_THRESHOLD)
                
                PERCENTAGE = (greyPXL/totalPXL) * 100
                
                print("PERCENTAGE: " + str(PERCENTAGE))
                
                if PERCENTAGE >= 10:
                    return(False)
                else:
                    return(True)
                
            if OBJECT == "FullAssembly" or OBJECT == "MidAssembly":

                if (BBy < 100 and BBx < 100) or (BBy < 100 and BBx > 950) or (BBy > 650 and BBx < 100) or (BBy > 650 and BBx > 950):
                    return(False)
                else:
                    return(True)
                
            else:
                return(True)
        
        else:
            return(True)
        
    def fixedZ(self, OBJECT):

        if self.CELL == "irb120-cranfield":

            if OBJECT == "TopCylinder":
                return(0.867)
            
            elif OBJECT == "BaseCylinder":
                return(0.897)
            
            elif OBJECT == "RedCube" or OBJECT == "WhiteCube" or OBJECT == "GreenCube" or OBJECT == "BlueCube":
                return(0.876)
            
            elif OBJECT == "TopCube":
                return(0.8735)
            
            elif OBJECT == "BottomCube":
                return(0.881)
            
            else:
                return(0.0)
            
        if self.CELL == "ur3-cranfield":

            if OBJECT == "TopCylinder":
                return(0.854)
            
            elif OBJECT == "BaseCylinder":
                return(0.884)
            
            elif OBJECT == "RedCube" or OBJECT == "WhiteCube" or OBJECT == "GreenCube" or OBJECT == "BlueCube":
                return(0.86)
            
            elif OBJECT == "TopCube":
                return(0.857)
            
            elif OBJECT == "BottomCube":
                return(0.864)
            
            else:
                return(0.0)
            
        if (self.CELL == "irb1200-amrc"):
            
            if OBJECT == "RedCube" or OBJECT == "WhiteCube" or OBJECT == "GreenCube" or OBJECT == "BlueCube":
                return(0.135)
            
            elif OBJECT == "TopCube":
                return(0.1325)
                
            elif OBJECT == "BottomCube":
                return(0.139)    
                
            elif OBJECT == "TopCylinder":
                return(0.13)
            
            elif OBJECT == "BaseCylinder":
                return(0.16)
            
            else:
                return(0.0)
            
        else:
            return(0.0)