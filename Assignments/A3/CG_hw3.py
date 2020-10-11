# Filename: CG_hw3.py
# Description: Postscript-like format file and Generate a PBM Image as Output
# Created: 09/24/2020
# Updated: 10/08/2020
# Bjb366
# CS430-001

import sys
import math

# Global Variables
inFile = 'hw3_split.ps'
scaleFact = 1.0
rotation = 0
xTrans = 0
yTrans = 0
xLower = 0
yLower = 0
xUpper = 250
yUpper = 250
xLowerView = 0
yLowerView = 0
xUpperView = 200
yUpperView = 200

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
    global xLowerView
    global yLowerView
    global xUpperView
    global yUpperView
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
        elif (argStr == '-c'):      #Upper Bound of X-Dimension World Window (Default: 250)
                xUpper = int(sys.argv[i+1])
        elif (argStr == '-d'):      #Upper Bound of Y-Dimension World Window (Default: 250)
                yUpper = int(sys.argv[i+1])
        elif (argStr == '-j'):      #Lower bound of X-Dimension Viewport Window (Default: 0)
                xLowerView = int(sys.argv[i+1])
        elif (argStr == '-k'):      #Lower bound of Y-Dimension Viewport Window (Default: 0)
                yLowerView = int(sys.argv[i+1])
        elif (argStr == '-o'):      #Upper bound of X-Dimension Viewport Window (Default: 200)
                xUpperView = int(sys.argv[i+1])
        elif (argStr == '-p'):      #Upper bound of Y-Dimension Viewport Window (Default: 200)
                yUpperView = int(sys.argv[i+1])

        i+=2
    
    return

""" 
Function: GetLine
Description: Read Line from "Postscript" File 
Arguments: none
Return: segments[]
"""
def getLine(inFile):
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
                line = (l.strip().split(" "))
                while "" in line:
                    line.remove("")
                segments.append(line)
    
    return(segments)

""" 
Function: Get Segments
Description: Get Line Segments for each polygon from "Postscript" File 
Arguments: none
Return: polygons[]
"""
def getSegment(rLines):
    startX = '0'
    startY = '0'
    endX = '0'
    endY = '0'
    segments = []
    polygons = []
    
    for l in range(len(rLines)):
        if rLines[l][0] == 'stroke':
            polygons.append(segments)
            segments = []
        elif rLines[l][2] == 'moveto':
            startX = rLines[l][0]
            startY = rLines[l][1]
        elif rLines[l][2] == 'lineto':
            endX = rLines[l][0]
            endY = rLines[l][1]
            segments.append([startX,startY,endX,endY,'Line'])
            startX = rLines[l][0]
            startY = rLines[l][1]
        else:
            print("ERROR: Unhandled Line Read")
            print(rLines[l])

    return polygons

""" 
Function: Apply Transforms
Description: Apply Transformations to them in World Coordinates
Arguments: polygon
Return: tSegments[]
"""
def applyTransforms(polygon):
    sSegments = [] #List of Scaled Segments
    rSegments = [] #List of Scaled and Rotated Segments
    tSegments = [] #List of Scaled, Rotated, and Translated Segments
 
    # Scale Image
    for s in polygon:
        sSegments.append([
            int(int(s[0])*scaleFact),
            int(int(s[1])*scaleFact),
            int(int(s[2])*scaleFact),
            int(int(s[3])*scaleFact)
        ])
    
    # Rotate Image
    radAngle = (math.radians(rotation))
    for r in sSegments:
        rSegments.append([
            int((r[0]*(math.cos(radAngle)))-(r[1]*math.sin(radAngle))),
            int((r[0]*(math.sin(radAngle)))+(r[1]*math.cos(radAngle))),
            int((r[2]*(math.cos(radAngle)))-(r[3]*math.sin(radAngle))),
            int((r[2]*(math.sin(radAngle)))+(r[3]*math.cos(radAngle)))
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
Description: Clip Tranformed Lines to World Window
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
            y0 = (((xUpper - x0)/(x1-x0))*(y1-y0)+y0)
            x0 = xUpper
        elif (x1 > xUpper):
            y1 = (((xUpper - x1)/(x0-x1))*(y0-y1)+y1)
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
Function: clipSuther
Description: Clip Transformed Polygon using Sutherland-Hodgman Algorithm
Arguments: tranformedSeg[]
Return: clipSeg[]
"""
def clipSuther(tranformedSeg):
    clipSeg = []
    polyCoors = []

    # Append Coordinates of Polygon
    polyCoors.append((tranformedSeg[0][0],tranformedSeg[0][1]))
    for s in tranformedSeg:
        polyCoors.append((s[2],s[3]))
    
    clipPoly = [(xLower,yLower),(xUpper,yLower),(xUpper,yUpper),(xLower,yUpper)]
    subPoly = polyCoors
    
    # Can Assume it is a closed polygon
    # Delete first point duplicate
    outputList = subPoly[1:]

    # Complete Clipping
    for c in range(len(clipPoly)):
        inputList = outputList
        outputList = []

        # Declare Clipping Edge
        clipV1 = clipPoly[c]
        clipV2 = clipPoly[c-1]

        for s in range(len(inputList)):
            subV1 = inputList[s]
            subV2 = inputList[s-1]

            if (((clipV2[1]-clipV1[1])*(subV1[0]-clipV1[0])) >= ((clipV2[0]-clipV1[0])*(subV1[1]-clipV1[1]))):
                # Case 1 - Both Inside
                if (((clipV2[1]-clipV1[1])*(subV2[0]-clipV1[0])) >= ((clipV2[0]-clipV1[0])*(subV2[1]-clipV1[1]))):
                    outputList.append(subV1)

                # Case 2 - Out to IN
                else:
                    deltaClipX = clipV1[0] - clipV2[0]
                    deltaClipY = clipV1[1] - clipV2[1]
                    deltaLineX = subV1[0] - subV2[0]
                    deltaLineY = subV1[1] - subV2[1]
                    
                    # Vertical Boundary
                    if deltaClipX == 0:
                        if deltaLineY == 0:
                            interX = clipV1[0]
                            interY = subV1[1]
                        else:
                            slopeLine = ((subV2[0]-subV1[0])/(subV2[1]-subV1[1]))
                            slopeClip = ((clipV2[0]-clipV1[0])/(clipV2[1]-clipV1[1]))

                            interY = ((((slopeLine*subV1[1])-subV1[0])-((slopeClip*clipV1[1])-clipV1[0]))/(slopeLine-slopeClip))
                            interX = (slopeLine*interY)-((slopeLine*subV1[1])-subV1[0])

                    # Horizontal Boundary
                    else:
                        if deltaLineX == 0:
                            interX = subV1[0]
                            interY = clipV1[1]
                        else:
                            slopeLine = ((subV2[1]-subV1[1])/(subV2[0]-subV1[0]))
                            slopeClip = ((clipV2[1]-clipV1[1])/(clipV2[0]-clipV1[0]))

                            interX = ((((slopeLine*subV2[0])-subV2[1])-((slopeClip*clipV1[0])-clipV1[1]))/(slopeLine-slopeClip))
                            interY = (slopeLine*interX)-((slopeLine*subV1[0])-subV1[1])

                    intersection=(int(interX),int(interY))
                    outputList.append(intersection)
                    outputList.append(subV1)
                    
            else:
                # Case 3 - v1 IN to OUT
                if (((clipV2[1]-clipV1[1])*(subV2[0]-clipV1[0])) >= ((clipV2[0]-clipV1[0])*(subV2[1]-clipV1[1]))):

                    # Find Intersection
                    deltaClipX = clipV1[0] - clipV2[0]
                    deltaClipY = clipV1[1] - clipV2[1]
                    deltaLineX = subV1[0] - subV2[0]
                    deltaLineY = subV1[1] - subV2[1]
                    
                    # Vertical Boundary
                    if deltaClipX == 0:
                        if deltaLineY == 0:
                            interX = clipV1[0]
                            interY = subV1[1]
                        else:
                            slopeLine = ((subV2[0]-subV1[0])/(subV2[1]-subV1[1]))
                            slopeClip = ((clipV2[0]-clipV1[0])/(clipV2[1]-clipV1[1]))

                            interY = ((((slopeLine*subV1[1])-subV1[0])-((slopeClip*clipV1[1])-clipV1[0]))/(slopeLine-slopeClip))
                            interX = (slopeLine*interY)-((slopeLine*subV1[1])-subV1[0])
                    
                    # Horizontal Boundary
                    else:
                        if deltaLineX == 0:
                            interX = subV1[0]
                            interY = clipV1[1]
                        else:
                            slopeLine = ((subV2[1]-subV1[1])/(subV2[0]-subV1[0]))
                            slopeClip = ((clipV2[1]-clipV1[1])/(clipV2[0]-clipV1[0]))

                            interX = ((((slopeLine*subV1[0])-subV1[1])-((slopeClip*clipV1[0])-clipV1[1]))/(slopeLine-slopeClip))
                            interY = (slopeLine*interX)-((slopeLine*subV1[0])-subV1[1])

                    intersection=(int(interX),int(interY))
                    outputList.append(intersection)

                # Case 4 - Both Outside
                else:
                    continue 

    # Convert To Line Format (StartX, StartY, End X, EndY)
    for l in range(len(outputList)):
        clipSeg.append([outputList[l-1][0],outputList[l-1][1],outputList[l][0],outputList[l][1]])

    return clipSeg

""" 
Function: WorldToViewport
Description: Map the World Window into the Viewport
Arguments: clippedSeg[]
Return: portSegs[]
"""
def worldToViewport(clippedSeg):
    worldOrigin = []
    worldScale = []
    portSegs = []

    #Translate World Window to Origin
    for c in clippedSeg:
        worldOrigin.append([
            int(c[0])-xLower,
            int(c[1])-yLower,
            int(c[2])-xLower,
            int(c[3])-yLower
        ])

    #Scale World Window to Size of Viewport
    for w in worldOrigin:
        worldScale.append([
            int(int(w[0])*((xUpperView-xLowerView)/(xUpper-xLower))),
            int(int(w[1])*((yUpperView-yLowerView)/(yUpper-yLower))),
            int(int(w[2])*((xUpperView-xLowerView)/(xUpper-xLower))),
            int(int(w[3])*((yUpperView-yLowerView)/(yUpper-yLower)))
        ])

    #Translate to final position of Viewport
    for s in worldScale:
        portSegs.append([
            int(s[0])+xLowerView,
            int(s[1])+yLowerView,
            int(s[2])+xLowerView,
            int(s[3])+yLowerView
        ])

    return portSegs

""" 
Function: Apply Translation
Description: Translate lines into Screen/Image Coordinates
Arguments: viewportSeg[]
Return: screenCoor[]
"""
def applyTranslation(viewportSeg):
    screenCoor = []

    if (xLower == 0 and yLower==0):
        screenCoor = viewportSeg
    else:
        for seg in viewportSeg:
            screenCoor.append([seg[0]-xLower,seg[1]-yLower,seg[2]-xLower,seg[3]-yLower])
        
    return screenCoor 

""" 
Function: Draw Lines
Description: Scan Convert (i.e. Draw) Clipped Lines into Software Frame Buffer
Arguments: screenCoor[]
Return: frameBuffer
"""
def drawLines(screenCoor, buffer):
    frameBuffer = buffer

    if frameBuffer == []:
        rows = 501
        cols = 501

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
        x0 = s[0]
        y0 = s[1]
        x1 = s[2]
        y1 = s[3]

        if abs(y1 - y0) < abs(x1 - x0):
            if x0 < x1:
                pixels.append(getBresenham(x0, y0, x1, y1, 'x'))
            else:
                pixels.append(getBresenham(x1, y1, x0, y0, 'x'))
        else:
            if y0 < y1:
                pixels.append(getBresenham(x0, y0, x1, y1, 'y'))
            else:
                pixels.append(getBresenham(x1, y1, x0, y0, 'y'))

    # Populate Buffer with Images using Bresenham Algorithm
    for line in pixels:
        for p in line:
            try:
                frameBuffer[-(p[1])][p[0]]=1
            except IndexError:
                continue
        
    return frameBuffer

"""
Function: getBresenham
Description: Use Bresenham Algortithm to scan-conversion of lines
Arguments:
Return: blackPixels
"""
def getBresenham(x0, y0, x1, y1, method):
    blackPixels = []

    if x1 == x0:
        slope = 2 #Slope Undefined, using 2 to represent steep slope
    else:
        slope = ((y1 - y0)/(x1 - x0))

    if (method == 'x'):
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
        dx = x1 - x0
        dy = y1 - y0
        D = (2 * dx) - dy
        y = y0
        x = x0
    
        if dx < 0:
            xi = -1
            dx = -dx
        else:
            xi = 1
    
        while (y <= y1):
            blackPixels.append((x,y))
            if D <= 0:
                D += (2*dx)
            else:
                x += xi
                D += (2*(dx-dy))
                
            y+=1
    
    return blackPixels

""" 
Function: ScanFill
Description: Fill the Polygon using Scan Filling
Arguments: polygons[]
Return: filledPolygons[]
"""
def scanfill(polygons, buffer):
    if polygons == []:
        return
    else:
        ymin = polygons[0][1]
        ymax = polygons[0][1]

    #find ymin and ymax
    for edge in polygons:
        if edge[1] < ymin:
            ymin = edge[1]
        elif edge[1] > ymax:
            ymax = edge[1]

    for edge in polygons:
        if edge[1] == edge[3]:
            continue
        
            #Mark each scan line that edge crosses by examining its ymin and ymax
            
            #if edge is horizontal
                #ignore
            #if ymax on scan line
                #ignore
            #if ymin <= y < ymax
                #Add edge to scan line y's edge list
            
        #For each scan line between polygons ymin and ymax
            #Caluculate intersections with edges on list
            #sort intersections in x
            #perform parity-bit scan-line filling
            #check for double intersection special case
        
        #Clear scan lines' edge list

    return

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
    readLines = getLine(inFile)
    buffer = []

    if len(readLines[0]) == 3:
        poly = True
        postLines = getSegment(readLines)
    else: 
        poly = False
        postLines = readLines

    for l in postLines:
        transLines = applyTransforms(l)

        if poly == True:
            clippedSegs = clipSuther(transLines)
        else:
            clippedSegs = applyClip(transLines)
    
        viewportSegs = worldToViewport(clippedSegs)

        buffer = drawLines(viewportSegs,buffer)

        # if poly == True:
        #     scanfilled = scanfill(viewportSegs,buffer)

    writePBM(buffer)
      
##########################################################################
main()
