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
          
    def applyCORRECTION(self, x,y):
        
        if self.CELL == "irb120-cranfield":
            
            xDIF = 0.70-x
            yDIF = 0.525-y
            
            if xDIF >= 0:
                x = x + abs(xDIF)*1.5/100  
            else:
                x = x
                
            if yDIF >= 0:
                y = y + abs(yDIF)*1.5/100  
            else:
                y = y - abs(yDIF)*1.5/100

            return(x,y)
                
        else:
            
            return(x,y)
        
    def extraSTEP(self, IMAGE, OBJECT, BBx, BBy):

        if OBJECT == "TopCylinder" or OBJECT == "BaseCylinder":

            IMG = IMAGE.copy()
                
            gray = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (9, 9), 2)
            circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=80, param2=35, minRadius=10, maxRadius=100)

            if circles is not None:
                return(True)
            else:
                return(False)
            
        if OBJECT == "FullAssembly" or OBJECT == "MidAssembly":

            if (BBy < 100 and BBx < 100) or (BBy < 100 and BBx > 950) or (BBy > 650 and BBx < 100) or (BBy > 650 and BBx > 950):
                return(False)
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
            
            else:
                return(0.0)
            
        else:
            return(0.0)