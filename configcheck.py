#-------------------------------------------------
# Check config.py and initialize image source

import config as cfg
import sys
import os
import random
import gan_generate as gan

#-------------------------------------------------

# Define formatting for stylized CLI info
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

statusOk = str(bcolors.OKGREEN + bcolors.BOLD + "OK" + bcolors.ENDC)
statusOkBlue = str(bcolors.OKBLUE + bcolors.BOLD + "OK" + bcolors.ENDC)
statusWarning = str(bcolors.WARNING + bcolors.BOLD + "Warning" + bcolors.ENDC)
statusDanger = str(bcolors.FAIL + bcolors.BOLD + "Danger" + bcolors.ENDC)
statusFatal = str(bcolors.FAIL + bcolors.BOLD + "Fatal" + bcolors.ENDC)

#-------------------------------------------------

# Load or generate image according to config.py
def imgLoad():
    print(bcolors.BOLD + "The following image will be painted:" + bcolors.ENDC)
    global img
    if cfg.imgRandom:
        files = os.listdir(cfg.imgRandom)
        while True:
            index = random.randrange(0, len(files))
            if not files[index].startswith("."):
                break
        img = str(cfg.imgRandom+"/"+(files[index]))
        print(img)
    elif cfg.imgPath:
        img = cfg.imgPath     
        print(img)
    elif cfg.imgGenerate:
        if cfg.imgGenerate == "face":
            gan.proGanGen(cfg.imgGenerate)
        else:
            gan.styleGanGen(cfg.imgGenerate)
    else:
        sys.exit(statusFatal + " No image source specified in config.py")

#-------------------------------------------------

# Displays settings in human readable format and checks for dangerours settings
def securityCheck():
    if cfg.canvasWidth <= 0 or cfg.canvasHeight <= 0 or cfg.strokeLength <= 0 or cfg.brushSize <= 0:
        sys.exit(statusFatal + " One or more of the following values are 0 or negative: canvasWidth, canvasHeight, strokeLength, brushSize. Change them in config.py")
    else:
        statusStrokeLength = statusOk + " Stroke Length: " + str(cfg.strokeLength) + "mm"
        statusBrushSize = statusOk + " Brush Size: " + str(cfg.brushSize) + "mm"
    if cfg.canvasWidth > 1999:
        statusCanvasWidth = statusWarning + " Canvas Width: " + bcolors.WARNING + str(cfg.canvasWidth) + "mm" + bcolors.ENDC + " or " + str(round(cfg.canvasWidth/1000,2)) + "m or " + str(round(cfg.canvasWidth/24.5,2)) + " inches. The specified canvas size is considered very large. Proceed if this is intendet."
    else:
        statusCanvasWidth = statusOk + " Canvas Width: " + str(cfg.canvasWidth) + "mm"
    if cfg.canvasHeight > 1999:
        statusCanvasHeight = statusWarning + " Canvas Height: " + bcolors.WARNING + str(cfg.canvasHeight) + "mm" + bcolors.ENDC + " or " + str(round(cfg.canvasHeight/1000,2)) + "m or " + str(round(cfg.canvasHeight/24.5,2)) + " inches. The specified canvas size is considered very large. Proceed if this is intendet."
    else:
        statusCanvasHeight = statusOk + " Canvas Height: " + str(cfg.canvasHeight) + "mm"
    if cfg.toolDepth < 20 and cfg.toolDepth > 0:
        statusToolDepth = statusWarning + " Tool Depth: " + bcolors.WARNING + str(cfg.toolDepth) + "mm" + bcolors.ENDC + " or " + str(round(cfg.toolDepth/24.5,2)) + " inches. Your tool will push into the canvas. Proceed if the tool or canvas is flexible."
    elif cfg.toolDepth >= 20:
        statusToolDepth = statusDanger + " Tool Depth: " + bcolors.FAIL + str(cfg.toolDepth) + "mm" + bcolors.ENDC + " or " + str(round(cfg.toolDepth/24.5,2)) + " inches. The tool depth is considered very high and will push deeply into the canvas. Proceed with caution."
    else:
        statusToolDepth = statusOk + " Tool Depth: " + str(cfg.toolDepth) + "mm"

    if cfg.blur % 2 == 0 and cfg.blur != 0 or cfg.blur < 0:
        sys.exit(statusFatal + " cfg.Blur: " + bcolors.FAIL + str(cfg.blur)+ "px" + bcolors.ENDC + " Blur has to be an odd number and not negative.")
    if cfg.threshColor > 255:
        sys.exit(statusFatal + " Threshold: " + bcolors.FAIL + str(cfg.threshColor) + bcolors.ENDC + " threshColor has to be between 0 and 255 or negative for deactivation.")

    # Print CLI info
    print(str(bcolors.BOLD + "Security Check" + bcolors.ENDC))
    print(statusCanvasWidth)
    print(statusCanvasHeight)
    print(statusBrushSize)
    print(statusStrokeLength)
    print(statusToolDepth)
    print(str(bcolors.BOLD + "Fine Tuning" + bcolors.ENDC))
    if cfg.imgScale != 1:
        print(statusOkBlue + " Image Scale: " + str(cfg.imgScale))
    if cfg.denoise >= 0:
        print(statusOkBlue + " Denoise: " + str(cfg.denoise))
    if cfg.blur > 0:
        print(statusOkBlue + " Blur: " + str(cfg.blur))
    if cfg.threshColor > -1:
        print(statusOkBlue + " Threshold: " + str(cfg.threshColor) + "-255")
    print(bcolors.BOLD + "Summary" + bcolors.ENDC)
    print("The robot will paint a " + str(cfg.canvasWidth) + "x" + str(cfg.canvasHeight) + "mm painting with a stroke diameter of " + str(cfg.brushSize) + "mm, a maximum stroke length of " + str(cfg.strokeLength) + "mm and the tool will push " + str(cfg.toolDepth) + "mm into the canvas.")
    input("Press [Enter] to start.")