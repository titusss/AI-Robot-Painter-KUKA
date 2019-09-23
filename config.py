#-------------------------------------------------
# Configure everything here
#
# Information about usage and recommended settings can be found here:
# https://github.com/chinapwn/AI-Robot-Painter-KUKA

# Network
host = "172.31.1.100" # Define the Server IP
port = 59152 # Define the Port

# Image source
imgPath = "source/example.jpeg" # Path to specific image. Leave empty when choosing other option.
imgRandom = "" # Choose random image from specified folder. Leave empty when choosing other option.
imgGenerate = "" # Generate new image with GAN. Options: face, abstract, portrait. Leave empty when choosing other option.

# Color palette
genreType = "abstract" # Define your colors in colors.py and specify the palette here

# Setup
canvasWidth = 800 # Canvas Width in mm.
canvasHeight = 800 # Height in mm.
brushSize = 15 # Diameter of the brush in mm. Defines the size of the gap between each brush stroke.
strokeLength = 150 # Maximum length of a stroke in mm, before the robot refreshes paint.
toolDepth = 0 # How deep the tool pushes into the canvas. Necessary for flexible tool or canvas, but dangerous if both are rigid.

# Fine-Tuning (Optional)
imgScale = 0.3 # Scale your image up or down for less complexity and painting time. Value Multiplies width and height.
denoise = 10 # Denoises image. This greatly reduces complexity and painting time. Default: 10. No denoise: 0.
blur = 3 # Blurs image to reduce complexity. Value in pixels. Requires odd value.
threshColor = -1 # Choose value between 0-254 (125 recommended). Negative value deactivates threshold color quantization (Default).