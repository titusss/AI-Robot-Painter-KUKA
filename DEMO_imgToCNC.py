#-------------------------------------------------
# Copyright (c) 2019, Titus Ebbecke. All rights reserved.
#-------------------------------------------------

import numpy as np
from numpy import linalg as LA
import cv2
import sys
import math
import socket
import time
import datetime
import pathlib
import config as cfg
import configcheck as check
import colors
from copy import deepcopy

#-------------------------------------------------
# Initialize image loading/generation and check config

check.imgLoad()
check.securityCheck()

#-------------------------------------------------
# Image preparation and color quantization

img = cv2.imread(check.img)

height, width, depth = img.shape
img = cv2.resize(img,(int(width*cfg.imgScale), int(height*cfg.imgScale))) # Scales image, when defined in config.py

# Apply fine tuning, when specified in config.py
if cfg.blur > 0:
    img = cv2.GaussianBlur(img,(cfg.blur,cfg.blur),0)
if cfg.denoise > 0:
    img = cv2.fastNlMeansDenoisingColored(img,None,cfg.denoise,cfg.denoise,7,21)
if cfg.threshColor >= 0:
    img = cv2.threshold(img,cfg.threshColor,255,cv2.THRESH_BINARY)[1]

Y = img.reshape((-1, 3))
Y = np.float32(Y)

# K-means Algorithm to reduce color amount to K
K = colors.colorPaint.shape[0] # Amount of colors
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret,label,center=cv2.kmeans(Y,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

#-------------------------------------------------
# Change reduced colors to the colors defined in colors.py

colorDifferenceMax = 500
a = []
b = []
c = []

for i in range(K):
    for j in range(K):
        #d = math.sqrt((((center[i][2])-(colors.colorPaint[j][2])))**2 + (((center[i][1])-(colors.colorPaint[j][1])))**2 + (((center[i][0])-(colors.colorPaint[j][0])))**2) # Calculate euclidean distance between source colors and palette colors
        d = math.sqrt((((center[i][2])-(colors.colorPaint[j][2]))*0.3)**2 + (((center[i][1])-(colors.colorPaint[j][1]))*0.59)**2 + (((center[i][0])-(colors.colorPaint[j][0]))*0.11)**2) # Calculate euclidean distance with weights. May improve color matching. Eyes perceive some colors better then others. Uncomment this line and comment out the above one, to apply
        a.insert(j, int(d))
    if a[np.argmin(a)] < colorDifferenceMax: # Fallback when color distance is too large
        b.insert(i, np.argmin(a))
        a.clear()
        c.clear()
    else:
        b.insert(i, "null")
        a.clear()

# Match colors from k-means reduced input image with color palette from colors.py
for i in range(K):
   res2[np.where((res2== [center[i]]).all(axis=2))] = [colors.colorPaint[b][i]]
imgReduced = deepcopy(res2)

#-------------------------------------------------
# Setup parameters for CNC translation

# Calculate pixel-to-mm ratio
canvasSize = [cfg.canvasWidth, cfg.canvasHeight]
if img.shape[0] > img.shape[1]:
    resizeFactor = canvasSize[0]/img.shape[0]
else:
    resizeFactor = canvasSize[0]/img.shape[1]

# Setup variables
size = np.size(img)
done = False
brushPixel = (cfg.brushSize/resizeFactor)*2
tolerance = 5 # Shrinks the brush size to force overlapping strokes. Increase for less missed spots. Value in mm.
initialPath = True
contourExists = False
singlePathJump = False
directionDegrees = 90
kernelBrush = np.ones((int(brushPixel)-int((tolerance/resizeFactor)*2),int(brushPixel)-int((tolerance/resizeFactor)*2)),np.uint8) # Erosion kernel. Reduces brush size. Increase negative values, to reduce missed painting spots
messageCount = 0

#-------------------------------------------------
# Communication disabled in demo mode
#
# Network - Socket

#Binds the Client with the Server
#mySocket = socket.socket()
#mySocket.bind((cfg.host,cfg.port))
 
#mySocket.listen(1)
#conn, addr = mySocket.accept()
#print ("Connection from: " + str(addr))

#-------------------------------------------------
# Define communication function

def sendActions(message):
    global messageCount
    #message = message.encode()
    #conn.send(message)
    print("Message sent to client:", message)
    print("\n")
    messageCount += 1
    #answer = conn.recv(33)
    #answer = answer.decode()
    #print("Client answer:", answer)

#-------------------------------------------------
# Near-Real-Time communication with robot
#
# DOCUMENTATION
#
# <Status 1> = Normal frame of coordinates.
# <Status 2> = Take paint with tool. May be removed, when your tool supports continous paint delivery and needs no paint refresh.
# <Status 3> = Path jump. A contour has been finished and the robot jumps to the beginning of the next contour.

# Loop through all colors K
for i in range(K):
    mask = cv2.inRange(res2, colors.colorPaint[i], colors.colorPaint[i]) # Define parameters of the color mask
    ## Remove noise form mask with erosion followed by dilation (Opening)
    #kernel = np.ones((2,2),np.uint8) # Fine tune kernel for less or more denoising
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    colorSelected = colors.colorPaint[i]

    while(not done):
        ret, thresh = cv2.threshold(mask, 127, 255, 0) # Mask color K
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find contours in color mask
        cv2.drawContours(res2, contours, -1, (0,255,0), 1) # Draw contours
        zeros = size - cv2.countNonZero(mask)
        mask = cv2.erode(mask,kernelBrush,iterations = 1) # Shrink mask for innermore contour

        # Take paint for the very first time, when currently selected color exists
        if len(contours) > 0 and initialPath == True:
            sendActions('<Ext><Status>2</Status><Color>99</Color></Ext>')
            print("Start with color:", colors.colorPaint[i])
            currentStrokeLength = 0
            initialPath = False

        # Loop through all contours of the current color
        for l in range(len(contours)):
            newPath = False
            if len(contours[l])>1:
                for m in range(len(contours[l])):
                    contourExists = True
                    # Calculate distance to next coordinate, if there is a next coordinate in the array
                    if m < (len(contours[l])-1):
                        dist = round((np.linalg.norm(contours[l][m][0]-contours[l][m+1][0]))*resizeFactor,1) # Calculate euclidean distance from current to next point
                        
                        # Calculate more distant coordinates
                        if m < (len(contours[l])-5):
                            longDist = round((np.linalg.norm(contours[l][m][0]-contours[l][m+5][0]))*resizeFactor,1) # Calculate euclidean distance from current to fifth next point
                            longX = round(contours[l][m+5][0][0]*resizeFactor)
                            longY = round(contours[l][m+5][0][1]*resizeFactor)
                        # Fallback, when the coordinate array approached it's end
                        else:                               
                            longX = round(contours[l][m][0][0]*resizeFactor)
                            longY = round(contours[l][m][0][1]*resizeFactor)
                            longDist = 0

                    # Calculate final coordinates (new and old ones)
                    # A coordinate is one xy-point in pixel of the contour-array
                    # It's then multiplied by the resize factor, to convert it into mm
                    currentX = round((contours[l][m][0][0])*resizeFactor)
                    currentY = round((contours[l][m][0][1])*resizeFactor)
                    lastX = round((contours[l][m-1][0][0])*resizeFactor)
                    lastY = round((contours[l][m-1][0][1])*resizeFactor)

                    # Calculate the direction to the next point
                    directionRadians = math.atan2(currentY-lastY, currentX-lastX)
                    directionDegrees = (round(math.degrees(directionRadians)/10))*10
                    # If the distance to the next point is too short and therefore irrelevant, take fifth next point
                    # This prevents the tool from changing it's direction unnecessarily much, when points have wildly different directions, because they're very close to each other
                    if longDist < 40:
                        directionRadians = math.atan2(longY-lastY, longX-lastX)
                        directionDegrees = (round(math.degrees(directionRadians)/10))*10

                    # CLI info
                    print("Angle to next point:", directionDegrees)
                    print("Distance to next point:", dist)
                    print("Stroke length:", currentStrokeLength)
                    
                    #-------------------------------------------------
                    # Sending status and coordinate frames
                    
                    # Check if coordinates are far enough away from the canvas border
                    # Not painting these coordinates prevents the robot from painting 'framing contours'
                    # These are created when the edge-contour of a (empty) background are found
                    # You may change this, if you also want these to be painted, e.g. in a full color painting
                    if currentX <= canvasSize[0]-10 and currentY <= canvasSize[1]-10 and currentX > 10 and currentY > 10:                       
                        sendActions('<Ext><Status>1</Status><Points><xyzabc X="'+str(currentX)+'" Y="'+str(currentY)+'" Z="'+str(cfg.toolDepth)+'" A="-0" B="-15" C="0"/></Points></Ext>')
                    
                    # When coordinates are too close to the edge (framing coordinates), move the robot to X=350, Y=350, Z=-300
                    # The robot will stay there and do nothing, until the current coordinates are not framing coordinates
                    elif currentX <= canvasSize[0] and currentY <= canvasSize[1]:
                        print("Coordinates too close to the edge. Wait for innermore coordinates.")
                        sendActions('<Ext><Status>1</Status><Points><xyzabc X="350" Y="350" Z="-300" A="-0" B="-15" C="0"/></Points></Ext>')
                    
                    else:
                    # Exit with fatal, when coordinates outside of the canvas are being generated
                    # This prevents the robot from leaving the canvas during the painting process
                        print("currentX, currentY", currentX, currentY)
                        sys.exit("Fatal: Points are being generated, that are larger than the given canvas size. Proceeding may cause serious damage and injury to the manipulator and it's sourroundings.")
                    
                    # Refresh paint, if the robot has painted a path longer than "strokeLength"
                    if currentStrokeLength > cfg.strokeLength:
                        print("Maximum stroke length reached. Refresh paint")
                        sendActions('<Ext><Status>2</Status><Color>99</Color></Ext>')                           
                        currentStrokeLength = 0 # Reset length of the stroke after color refresh

                    currentStrokeLength = currentStrokeLength+dist # Calculate the length of the path painted
                    singlePathJump = True

            print("Contour finished. Jump to new contour.")
            if singlePathJump == True:
                # Jump to new contour
                sendActions('<Ext><Status>3</Status><Points><xyzabc X="'+str(lastX)+'" Y="'+str(lastY)+'" Z="'+str(cfg.toolDepth)+'" A="-0" B="-15" C="0"/></Points></Ext>')
                newPath = True
                singlePathJump = False
        
        if zeros==size:
            done = True
            contourExists == False
    done = False

if done == True:
    #conn.close()
    print("Color finished.")

#-------------------------------------------------
# Save and show prepared source image and paths.

pathlib.Path("demo_results").mkdir(exist_ok=True) # Create /demo_results folder, if it doesn't exist
filename = "demo_results/"+str(f"{datetime.datetime.now():%Y%m%d_%H-%M-%S}") # Randomize filename
cv2.imwrite(filename+"_source.png", img) # Save image
cv2.imwrite(filename+"_reduced.png", imgReduced) # Save image
cv2.imwrite(filename +"_vectors.png", res2) # Save image
print("Painting finished.")
print("Total amount of messages sent:", messageCount)
print("Results saved as: "+filename)
cv2.imshow("Path Preview", res2)
cv2.waitKey(0)
cv2.destroyAllWindows()