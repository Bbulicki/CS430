# Filename: CG_hw4.py
# Description: Postscript-like format file and Generate a PBM Image as Output
# Created: 09/24/2020
# Updated: 11/01/2020
# Bjb366
# CS430-001

import sys
import math
import numpy as np

#Global Variables
inFile = ''
xLowerView = 0      # [-j]
yLowerView = 0      # [-k]
xUpperView = 500    # [-o]
yUpperView = 500    # [-p]

#3D View Volume
xProjection = 0.0   # [-x]
yProjection = 0.0   # [-y]
zProjection = 1.0   # [-z]
xReference = 0.0    # [-X]
yReference = 0.0    # [-Y]
zReference = 0.0    # [-Z]
xViewPlane = 0.0    # [-q]
yViewPlane = 0.0    # [-r]
zViewPlane = -1.0   # [-w]
xViewUp = 0.0       # [-Q]
yViewUp = 0.0       # [-R]
zViewUp = 0.0       # [-W]
uMin = -0.7         # [-u]
vMin = -0.7         # [-v]
uMax = 0.7          # [-U]
vMax = 0.7          # [-V]
# [-P]


""" 
Function: Set Globals
Description: Set Global Variables 
Arguments: None
Return: None
"""
def setGlobal():
    global inFile
    global xLowerView
    global yLowerView
    global xUpperView
    global yUpperView
    global xProjection 
    global yProjection 
    global zProjection 
    global xReference 
    global yReference 
    global zReference 
    global xViewPlane 
    global yViewPlane 
    global zViewPlane 
    global xViewUp 
    global yViewUp 
    global zViewUp 
    global uMin 
    global vMin 
    global uMax 
    global vMax 
    
    i = 1

    # Read Arguments and Adjust Defaults
    while (i < len(sys.argv)):
        argStr = str(sys.argv[i])
        if (argStr == '-f'):        #"Postscript" Input File (Default: hw1.ps)
            inFile = str(sys.argv[i+1])
        elif (argStr == '-j'):      #Lower bound of X-Dimension Viewport Window (Default: 0)
            xLowerView = int(sys.argv[i+1])
        elif (argStr == '-k'):      #Lower bound of Y-Dimension Viewport Window (Default: 0)
            yLowerView = int(sys.argv[i+1])
        elif (argStr == '-o'):      #Upper bound of X-Dimension Viewport Window (Default: 500)
            xUpperView = int(sys.argv[i+1])
        elif (argStr == '-p'):      #Upper bound of Y-Dimension Viewport Window (Default: 500)
            yUpperView = int(sys.argv[i+1])
        elif (argStr == '-x'):      #X of Projection Reference Point (Default: 0.0)
            xProjection = float(sys.argv[i+1])
        elif (argStr == '-y'):      #Y of Projection Reference Point (Default: 0.0)
            yProjection = float(sys.argv[i+1])   
        elif (argStr == '-z'):      #Z of Projection Reference Point (Default: 1.0)
            zProjection = float(sys.argv[i+1])   
        elif (argStr == '-X'):      #X of View Reference Point (Default: 0.0)
            xReference = float(sys.argv[i+1]) 
        elif (argStr == '-Y'):      #Y of View Reference Point (Default: 0.0)
            yReference = float(sys.argv[i+1]) 
        elif (argStr == '-Z'):      #Z of View Reference Point (Default: 0.0)
            zReference = float(sys.argv[i+1]) 
        elif (argStr == '-q'):      #X of View Plane Normal vector (Default: 0.0)
            xViewPlane = float(sys.argv[i+1]) 
        elif (argStr == '-r'):      #Y of View Plane Normal vector (Default: 0.0)
            yViewPlane = float(sys.argv[i+1])   
        elif (argStr == '-w'):      #Z of View Plane Normal vector (Default: -1.0)
            zViewPlane = float(sys.argv[i+1])  
        elif (argStr == '-Q'):      #X of View Up Vector (Default: 0.0)
            xViewUp = float(sys.argv[i+1]) 
        elif (argStr == '-R'):      #Y of View Up Vector (Default: 0.0)
            yViewUp = float(sys.argv[i+1])  
        elif (argStr == '-W'):      #Z of View Up Vector (Default: 0.0)
            zViewUp = float(sys.argv[i+1])    
        elif (argStr == '-u'):      #U Min of the VRC (Default: -0.7)
            uMin = float(sys.argv[i+1])   
        elif (argStr == '-v'):      #V Min of the VRC (Default: -0.7)
            vMin = float(sys.argv[i+1])   
        elif (argStr == '-U'):      #U Max of the VRC (Default: 0.7)
            uMax = float(sys.argv[i+1])         
        elif (argStr == '-V'):      #V Max of the VRC (Default: 0.7)
            vMax = float(sys.argv[i+1])          

        i+=2
    
    return



def main():
    setGlobal()



##########################################################################
main()