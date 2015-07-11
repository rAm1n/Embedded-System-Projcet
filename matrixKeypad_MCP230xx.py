# #####################################################
# Python Library for 3x4 matrix keypad using
# the MCP23008 chip via I2C from the Raspberry Pi.
# 
# This could easily be expanded to handle a 4x4 but I 
# don't have one for testing. The KEYPAD constant 
# would need to be updated. Also the setting/checking
# of the colVal part would need to be expanded to 
# handle the extra column.
# 
# Written by Chris Crumpacker
# May 2013
#
# main structure is adapted from Bandono's
# matrixQPI which is wiringPi based.
# https://github.com/bandono/matrixQPi?source=cc
# #####################################################

from Adafruit_MCP230xx import Adafruit_MCP230XX

class keypad(Adafruit_MCP230XX):
    # Constants
    INPUT       = 0
    OUTPUT      = 1
    HIGH        = 1
    LOW         = 0
    
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
    
    ROW         = [6,5,4,3]
    COLUMN      = [2,1,0]
    
    def __init__(self, address=0x21, num_gpios=8):
        
        self.mcp2 = Adafruit_MCP230XX(address, num_gpios)
        
    def getKey(self):
        
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            self.mcp2.config(self.COLUMN[j], self.mcp2.OUTPUT)
            self.mcp2.output(self.COLUMN[j], self.LOW)
        
        # Set all rows as input
        for i in range(len(self.ROW)):
            self.mcp2.config(self.ROW[i], self.mcp2.INPUT)
            self.mcp2.pullup(self.ROW[i], True)
        
        # Scan rows for pushed key/button
        # valid rowVal" should be between 0 and 3 when a key is pressed. Pre-setting it to -1
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = self.mcp2.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                
        # if rowVal is still "return" then no button was pressed and we can exit
        if rowVal == -1:
            self.exit()
            return
        
        # Convert columns to input
        for j in range(len(self.COLUMN)):
            self.mcp2.config(self.COLUMN[j], self.mcp2.INPUT)
        
        # Switch the i-th row found from scan to output
        self.mcp2.config(self.ROW[rowVal], self.mcp2.OUTPUT)
        self.mcp2.output(self.ROW[rowVal], self.HIGH)
        
        # Scan columns for still-pushed key/button
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = self.mcp2.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
        
        if colVal == -1:
            self.exit()
            return
              
        # Return the value of the key pressed
        self.exit()   
        return self.KEYPAD[rowVal][colVal]
            
    def exit(self):
        # Reinitialize all rows and columns as input before exiting
        for i in range(len(self.ROW)):
                self.mcp2.config(self.ROW[i], self.INPUT) 
        for j in range(len(self.COLUMN)):
                self.mcp2.config(self.COLUMN[j], self.INPUT)
        
if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()
    
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
        
    # Print the result
    print r  