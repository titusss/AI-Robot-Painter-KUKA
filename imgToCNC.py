import numpy as np
from numpy import linalg as LA
import cv2
import sys
import math
import socket
import time


### CLI Arguments

genreType = sys.argv[1]
inputFile = sys.argv[2]
outputFile = sys.argv[3]
a = []
b = []
c = []

### Variables

colorAmount = 12
colorDifferenceMax = 500

## Define the color values of the paint here. You can change them to whatever you think represents the choosen images in 12 colors the best, or which paint you are using.

# Portrait Color Palette. Read numbers from left to right, top to bottom. Values are in BGR. Naming is very roughly oriented at this https://en.wikipedia.org/wiki/List_of_colors:_A-F

deepChestnut_1 = [40, 75, 185]
bronze_2 = [74, 146, 216]
dutchWhite_3 = [135, 200, 231]
bone_4 = [205, 223, 222]
battleshipGrey_5 = [118, 133, 135]
ashGray_6 = [154, 171, 174]
frenchBeige_7 = [77, 113, 149]
babyPowder_8 = [250, 252, 252]
darkBrown_9 = [32, 43, 63]
blueSapphire_10 = [105, 100, 25]
coyoteBrown_11 = [61, 80, 101]
blackChocolate_12 = [10, 12, 20]

# Abstract Color Palette. Read numbers from left to right, top to bottom. Values are in BGR. Naming is very roughly oriented at this https://en.wikipedia.org/wiki/List_of_colors:_A-F

cultured_1 = [249, 250, 251]
almond_2 = [221, 217, 210]
cadmiumRed_3 = [13, 38, 228]
citrine_4 = [28, 200, 240]
bdazzledBlue_5 = [148, 83, 11]
blueGray_6 = [140, 125, 80]
copperRed_7 = [82, 121, 209]
burlywood_8 = [152, 192, 220]
blackShadows_9 = [147, 160, 175]
burnishedBrown_10 = [103, 113, 131]
darkLiverHorses_11 = [54, 61, 77]
black_12 = [19, 18, 19]

if genreType == 'portrait':
	colorPaint = np.array([deepChestnut_1, bronze_2, dutchWhite_3, bone_4, battleshipGrey_5, ashGray_6, frenchBeige_7, babyPowder_8, darkBrown_9, blueSapphire_10, coyoteBrown_11, blackChocolate_12])
elif genreType == 'abstract':

	colorPaint = np.array([cultured_1, almond_2, cadmiumRed_3, citrine_4, bdazzledBlue_5, blueGray_6, copperRed_7, burlywood_8, blackShadows_9, burnishedBrown_10, darkLiverHorses_11, black_12])
else:
	sys.exit("Error, please specify Genre Type. Choose \"portrait\" or \"abstract\"")

### CLI info

print("Converting", genreType, "image to", np.shape(colorPaint)[0], "colors.")

### K-means Algorithm to reduce color amount to K

## Read Image file

img = cv2.imread(inputFile)

Y = img.reshape((-1, 3))
Y = np.float32(Y)

## Apply k-means

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = np.shape(colorPaint)[0] # nClusters, equivalent to the amount of paint colors used
ret,label,center=cv2.kmeans(Y,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

## Check image for closest color from the predefined palette
print(center)

for i in range(K):
	for j in range(K):
		#d = math.sqrt((((center[i][2])-(colorPaint[j][2])))**2 + (((center[i][1])-(colorPaint[j][1])))**2 + (((center[i][0])-(colorPaint[j][0])))**2) # Calculate euclidean distance
		d = math.sqrt((((center[i][2])-(colorPaint[j][2]))*0.3)**2 + (((center[i][1])-(colorPaint[j][1]))*0.59)**2 + (((center[i][0])-(colorPaint[j][0]))*0.11)**2) # Calculate euclidean distance with weights. May improve color matching. Eyes perceive some colors better then others. Uncomment this line and comment out the above one, to apply.
		a.insert(j, int(d))
	print(a)
	if a[np.argmin(a)] < colorDifferenceMax:
		b.insert(i, np.argmin(a))
		a.clear()
		c.clear()
	else:
		b.insert(i, "null")
		a.clear()

print("Index of closest colors", b)


## Match color from k-means reduced input image with color palette
for i in range(K):
	print("center:", center[i])
	print("colorPaint", colorPaint[b][i])
	res2[np.where((res2== [center[i]]).all(axis=2))] = [colorPaint[b][i]]
	
### Convert to CNC path

## Brush variables
brushRadius = 10 # Brush radius in mm
canvasSize = [400, 400] # Canvas width and height in mm
resizeFactor = img.shape[0]/canvasSize[0]
brushPixel = brushRadius*resizeFactor

## Remove noise form mask with erosion followed by dilation (optional)

#kernel = np.ones((3,3),np.uint8) # Fine tune kernel for less or more denoising
#mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

## Mask colors

kernelBrush = np.ones((int(brushPixel)-3,int(brushPixel)-3),np.uint8) # This is the erosion kernel. Increase the weights that are subtracted from the values, to reduce missed spots
size = np.size(img)
done = False
strokeLength = 1000 # Maximum brush stroke length in mm
strokeLengthPixel = int(strokeLength*resizeFactor)

contourPath = []
contourParent = []
colorPath = []
path = []
nextPoint = ''
changeColor = True

contourExists = False
connectionOpen = True


### Configure socket here

host = "172.31.1.100"
port = 59152

## Bind with client

mySocket = socket.socket()
mySocket.bind((host,port))
mySocket.listen(1)
conn, addr = mySocket.accept()
print ("Connection from: " + str(addr))

## Define communication

def sendActions(message):
	message = message.encode()
	conn.send(message)
	print("Message sent to Client:", message)
	answer = conn.recv(33)
	answer = answer.decode()
	print("Client answered with:", answer)

### Loop through colors to find color clusters, create contours for them and erode them for innermore contours

while True:
	for i in range(K):
		mask = cv2.inRange(res2, colorPaint[i], colorPaint[i]) # Apply mask
		colorSelected = colorPaint[i]
		while(not done):
			mask = cv2.GaussianBlur(mask,(9,9),0) # Blur mask to reduce edges and therefore CNC points. Must be an odd number and positive.
			ret, thresh = cv2.threshold(mask, 127, 255, 0)
			im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			cv2.drawContours(res2, contours, -1, (0,255,0), 1)
			mask = cv2.erode(mask,kernelBrush,iterations = 1) # Shrink mask 
			zeros = size - cv2.countNonZero(mask)
			if len(contours) > 0:
				sendActions('<Ext><Status>2</Status><Color>'+str(i+1)+'</Color></Ext>')
				currentStrokeLength = 0
			for l in range(len(contours)):
				newPath = False
				for m in range(len(contours[l])-1):
					contourExists = True
					currentX = contours[l][m][0][0]
					currentY = contours[l][m][0][1]

					if m < len(contours[l]):
						dist = np.linalg.norm(contours[l][m][0]-contours[l][m+1][0]) # Calculate stroke length
						currentStrokeLength = currentStrokeLength+dist

					if currentStrokeLength > strokeLength:
						sendActions('<Ext><Status>2</Status><Color>'+str(i+1)+'</Color></Ext>')
						currentStrokeLength = 0

					if currentX <= canvasSize[0] and currentY <= canvasSize[1]:
						sendActions('<Ext><Status>1</Status><Points><xyzabc X="'+str(currentX)+'" Y="'+str(currentY)+'" Z="0" A="0" B="0" C="0"/></Points></Ext>')
					else:
						sys.exit("Fatal: Points are being generated, that are larger than the given canvas size. Proceeding may cause serious damage and injury to the manipulator and it's sourroundings.")
				print("newPath")
				sendActions('<Ext><Status>3</Status><Points><xyzabc X="'+str(currentX)+'" Y="'+str(currentY)+'" Z="0" A="0" B="0" C="0" /></Points></Ext>')
				newPath = True

			if zeros==size:
				done = True
				contourExists == False
		
		done = False
	pcDone = True 
conn.close()
cv2.imshow("res2", res2)
cv2.imshow("mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()