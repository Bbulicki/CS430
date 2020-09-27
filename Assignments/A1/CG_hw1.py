# Filename: CG_hw1.py
# Description: Accept Simplified Postscript-like format file and Generate a PBM Image as Output
# Created: 09/24/2020
# Updated: 09/24/2020
# CS430-001

import sys
import math

# Global Variables
inFile = 'hw1.ps'
scaleFact = 1.0
rotation = 0
xTrans = 0
yTrans = 0
xLower = 0
yLower = 0
xUpper = 499
yUpper = 499

""" 
Function: Set Globals
Description: Set Global Variables 
Arguments: None
Return: None
"""
def setGlobal():
    global inFile
    global scaleFact
    global rotation
    global xTrans
    global yTrans
    global xLower
    global yLower
    global xUpper
    global yUpper
    i = 1

    # Read Arguments and Adjust Defaults
    while (i < len(sys.argv)):
        argStr = str(sys.argv[i])
        if (argStr == '-f'):        #"Postscript" Input File (Default: hw1.ps)
                inFile = str(sys.argv[i+1])
        elif (argStr == '-s'):      #Scaling Factor (Default: 1.0) 
                scaleFact = float(sys.argv[i+1])
        elif (argStr == '-r'):      #Counter-Clockwise Rotation in Degrees (Default: 0)
                rotation = int(sys.argv[i+1])
        elif (argStr == '-m'):      #X-axis Translation (Default: 0)
                xTrans = int(sys.argv[i+1])
        elif (argStr == '-n'):      #Y-axis Translation (Default: 0)
                yTrans = int(sys.argv[i+1])
        elif (argStr == '-a'):      #Lower Bound of X-Dimension World Window (Default: 0)
                xLower = int(sys.argv[i+1])
        elif (argStr == '-b'):      #Lower Bound of Y-Dimension World Window (Default: 0)
                yLower = int(sys.argv[i+1])
        elif (argStr == '-c'):      #Upper Bound of X-Dimension World Window (Default: 499)
                xUpper = int(sys.argv[i+1])
        elif (argStr == '-d'):      #Upper Bound of Y-Dimension World Window (Default: 499)
                yUpper = int(sys.argv[i+1])
        i+=2
    
    return

""" 
Function: Get Segments
Description: Get Line Segments from "Postscript" File 
Arguments: none
Return: segments[]
"""
def getSegments(inFile):
    postFile = open(inFile, 'r')
    readlines = postFile.readlines()
    segments= []
    
    # Read lines in file and save coordinates
    reader = False
    for l in readlines:
        if (l.strip() == "%%%BEGIN"):
            reader = True
        elif (l.strip() == "%%%END"):
            reader = False
        else:
            if ((reader == True) and (len(l.strip()) != 0)):
                segments.append(l.strip().split(" "))
    
    return(segments)

""" 
Function: Apply Transforms
Description: Apply Transformations to them in World Coordinates
Arguments: segments
Return: tSegments[]
"""
def applyTransforms(segments):
    sSegments = [] #List of Scaled Segments
    rSegments = [] #List of Scaled and Rotated Segments
    tSegments = [] #List of Scaled, Rotated, and Translated Segments
 
    # Scale Image
    for s in segments:
        sSegments.append([
            int(int(s[0])*scaleFact),
            int(int(s[1])*scaleFact),
            int(int(s[2])*scaleFact),
            int(int(s[3])*scaleFact)
        ])
    
    # Rotate Image
    radAngle = math.radians(rotation)
    for r in sSegments:
        rSegments.append([
            int((r[0]*(math.cos(radAngle)))-r[1]*math.sin(radAngle)),
            int((r[0]*(math.sin(radAngle)))+r[1]*math.cos(radAngle)),
            int((r[2]*(math.cos(radAngle)))-r[3]*math.sin(radAngle)),
            int((r[2]*(math.sin(radAngle)))+r[3]*math.cos(radAngle))
        ])
    
    # Translate Image
    for t in rSegments:
        tSegments.append([
            int(t[0])+xTrans,
            int(t[1])+yTrans,
            int(t[2])+xTrans,
            int(t[3])+yTrans
        ])

    return(tSegments)

""" 
Function: Apply Clipping
Description: Clip Tranformed Lines to Window
Arguments: tranformedSeg[]
Return: clipSeg[]
"""
def applyClip(tranformedSeg):
    clipSeg = []
    cropLine = []

    for line in tranformedSeg:
        x0 = line[0]
        y0 = line[1]
        x1 = line[2]
        y1 = line[3]
        
        # Check if line is entirely out
        if ((x0 < xLower and x1 < xLower) or (y0 < yLower and y1 < yLower) or (x0 > xUpper and x1 > xUpper) or (y0 > yUpper and y1 > yUpper)):
            continue
        # Check if Line is entirely in
        elif ((x0 >= xLower and x1 >= xLower) and (y0 >= yLower and y1 >= yLower) and (x0 <= xUpper and x1 <= xUpper) and (y0 <= yUpper and y1 <= yUpper)):
            clipSeg.append(line)
        else:
            cropLine.append(line)
            
    for c in cropLine:
        x0 = c[0]
        y0 = c[1]
        x1 = c[2]
        y1 = c[3]
        # Check X Lower Bound
        if (x0 < xLower):
            y0 = ((xLower - x0)/(x1-x0))*(y1-y0)+y0
            x0 = xLower
        elif (x1 < xLower):
            y1 = ((xLower - x1)/(x0-x1))*(y0-y1)+y1
            x1 = xLower
        # Check Y Lower Bound
        if (y0 < yLower):
            x0 = ((yLower - y0)/(y1-y0))*(x1-x0)+x0
            y0 = yLower
        elif (y1 < yLower):
            x1 = ((yLower - y1)/(y0-y1))*(x0-x1)+x1
            y1 = yLower
        # Check X Upper Bound
        if (x0 > xUpper):
            y0 = ((xUpper - x0)/(x1-x0))*(y1-y0)+y0
            x0 = xUpper
        elif (x1 > xUpper):
            y1 = ((xUpper - x1)/(x0-x1))*(y0-y1)+y1
            x1 = xUpper
        # Check Y Upper Bound
        if (y0 > yUpper):
            x0 = ((yUpper - y0)/(y1-y0))*(x1-x0)+x0
            y0 = yUpper
        elif (y1 > yUpper):
            x1 = ((yUpper - y1)/(y0-y1))*(x0-x1)+x1
            y1 = yUpper
        
        clipSeg.append([int(x0),int(y0),int(x1),int(y1)])

    return clipSeg

""" 
Function: Apply Translation
Description: Translate lines into Screen/Image Coordinates
Arguments: clippedSeg[]
Return: screenCoor[]
"""
def applyTranslation(clippedSeg):
    screenCoor = []

    if (xLower == 0 and yLower==0):
        screenCoor = clippedSeg
    else:
        for seg in clippedSeg:
            screenCoor.append([seg[0]+xLower,seg[1]+ylower,seg[2]+xLower,seg[3]+yLower])

    return(screenCoor)

""" 
Function: Draw Lines
Description: Scan Convert (i.e. Draw) Clipped Lines into Software Frame Buffer
Arguments: screenCoor[]
Return: frameBuffer
"""
def drawLines(screenCoor):
    frameBuffer = []

    rows = yUpper - yLower + 1
    cols = xUpper - xLower + 1

    # Create "Empty" Buffer of Correct Size
    frameBuffer.append(["P1"])
    frameBuffer.append([str(cols) + " " + str(rows)])
    
    r = 0
    c = 0
    while (r < rows):
        tmpRow = []
        while(c < cols):
            tmpRow.append(0)
            c+=1
        frameBuffer.append(tmpRow)
        r+=1
        c=0

    # Get Pixels
    pixels = []
    for s in screenCoor:
        pixels.append(getBresenham(int(s[0]),int(s[1]),int(s[2]),int(s[3])))
    print(pixels[-1])
    print(screenCoor[-1])
    
    #print(pixels)
    # Populate Buffer with Images using Bresenham Algorithm
    for line in pixels:
        for p in line:
            frameBuffer[-1-(p[1])][p[0]]=1
        
    return frameBuffer

"""
Function: getBresenham
Description: Use Bresenham Algortithm to scan-conversion of lines
Arguments:
Return: blackPixels
"""
def getBresenham(x0, y0, x1, y1):
    blackPixels = []
    
    if x1 == x0:
        slope = 2 #Slope Undefined, using 2 to represent steep slope
    else:
        slope = ((y1 - y0)/(x1 - x0))

    if (-1 <= slope <= 1):
        if (x0 < x1):
            dx = x1 - x0
            dy = y1 - y0
            D = 2 * dy - dx
            y = y0
            x = x0
        
            if dy < 0:
                yi = -1
                dy = -dy
            else:
                yi = 1
        
            while (x <= x1):
                blackPixels.append((x,y))
                if D <= 0:
                    D += (2*dy)
                else:
                    D += (2*(dy-dx))
                    y+=yi
                x+=1
        else:
            dx = x0 - x1
            dy = y0 - y1
            D = 2 * dy - dx
            y = y1
            x = x1
        
            if dy < 0:
                yi = -1
                dy = -dy
            else:
                yi = 1
        
            while (x <= x0):
                blackPixels.append((x,y))
                if D <= 0:
                    D += (2*dy)
                else:
                    D += (2*(dy-dx))
                    y+=yi
                x+=1
    else:
        if (y0 < y1):
            dx = x1 - x0
            dy = y1 - y0
            D = 2 * dx - dy
            y = y0
            x = x0
        
            if dy < 0:
                xi = -1
                dx = -dx
            else:
                xi = 1
        
            while (y <= y1):
                blackPixels.append((x,y))
                if D <= 0:
                    D += (2*dx)
                else:
                    D += (2*(dx-dy))
                    x+=xi
                y+=1
        else:
            dx = x0 - x1
            dy = y0 - y1
            D = 2 * dx - dy
            y = y1
            x = x1
        
            if dy < 0:
                xi = -1
                dx = -dx
            else:
                xi = 1
        
            while (y <= y0):
                blackPixels.append((x,y))
                if D <= 0:
                    D += (2*dx)
                else:
                    D += (2*(dx-dy))
                    x+=xi
                y+=1
    # elif (x0 == x1) and (y0 > y1):
    #     y = y0
    #     x = x0
        
    #     while (y <= y1):
    #         blackPixels.append((x,y))
    #         y+=1
    # else:
        # y = y1
        # x = x0
        
        # while (y <= y0):
        #     blackPixels.append((x,y))
        #     y+=1
    
    return blackPixels

""" 
Function: writePBM
Description: Write Frame Buffer to Standard out in PBM Format
Arguments: screenBuffer
Return: 
"""
def writePBM(screenBuffer):
    for l in screenBuffer:
        line = ' '.join([str(elem) for elem in l])
        print(line)
    
    return

""" 
Function: Main
Description: Main Function
Arguments: None
Return: None
"""
def main():
    setGlobal()
    postLines = getSegments(inFile)
    transLines = applyTransforms(postLines)
    clippedSegs = applyClip(transLines)
    translatedCoor = applyTranslation(clippedSegs)
    buffer = drawLines(translatedCoor)
    #writePBM(buffer)
      
##########################################################################
main()
