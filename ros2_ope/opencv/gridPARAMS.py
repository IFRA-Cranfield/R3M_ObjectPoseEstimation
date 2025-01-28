#!/usr/bin/python3
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
        if self.CELL == "irb1200-amrc":
            
            # To calculate differences:
            xDIF = 1.1 - x
            yDIF = 0.55 - y
            
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

                x = x + 0.007 + xDIF * 0.025

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