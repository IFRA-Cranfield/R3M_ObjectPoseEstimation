#!/usr/bin/python3
import sys
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