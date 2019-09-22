<h1 align="center">
        <img
                alt="KUKA Robot and Canvas"
                src="https://titusebbecke.com/images/pba-img04.jpg">
</h1>
<h3 align="center">
        🤖 🎨 Load any image or let an AI generate one and paint it on canvas with a KUKA industrial robot
</h3>

<p align="center">
        <a href="https://titusebbecke.com/"><img
                alt="website"
                src="https://img.shields.io/badge/website-pending-blue"</a>
        <a href="https://vimeo.com/354081387"><img
                alt="demo video"
                src="https://img.shields.io/badge/demo-pending-blue?logo=Vimeo"</a>
</p>

# Overview
 - **Paints or draws anything.** Paint any kind of single-, or multi-colored picture with your KUKA robot. 
 - **Multicolor.** Choose as many colors as you want. Supports acrylic, oil, pencil and many more.
 - **Flexible setup.** Setup in 10 minutes. Only needs to calibrate canvas base and teach color refilling or tool switching paths.
 - **Pretty safe.** Only generates 2D-coordinates that fit the canvas size, set by the user.
 - **Easy to configure.** Use the intuitive python CLI-tool or just modify the reasonably messy python code.

# Table of contents

<!--ts-->
   * [What you need](#what-you-need)
   * [Installation](#installation)
	   * [Server](#server)
	   * [KRC](#krc)
	   * [Physical setup](#physical-setup)
	   * [robot](#robot)
   * [Starting the painting process](#starting-the-painting-process)
   * [Configuration](#configuration)
      * [Network](#network)
      * [Image source](#image-source)
      * [Color palette](#color-palette)
      * [Setup](#setup)
      * [Fine-tuning](#fine-tuning-optional)
   * [Example](#example)
   * [Recommendations](#recommendations)
   * [Safety](#safety)
<!--te-->

# What you need

- **KUKA robot.** This project was tested with a KR 10 R1420, but should work with any 6-axis KUKA robot.
- **KRC w. Ethernet-KRL.** This KUKA package is needed for communication between server and KRC.*
- **Server.** A laptop or similar, that is connected to the KRC via Ethernet and communicates over KLI. ⚠️ A NVIDIA graphics card is needed, when you want to generate pictures with the AI, instead of using pre-generated ones.
- **Python 3.** Install python on the server. I recommend an <a href="https://www.anaconda.com/distribution/">anaconda install</a>.
- **Utilities.** Any kind of painting tool attached to the robot, a canvas/paper to draw on, paint and water *(Optional)*.
  
*This project focuses on generating XYZ-coordinates (as Frames, E6POS or Integers) from an input image in near real-time. ℹ️ In theory any kind of interface could be used here. Generating a complete batch of coordinates and transfering them to the robot control afterwards (via USB-Stick e.g.) is possible with a few modifications.

# Installation

### Server

> Some libraries and modules such as OpenCV need to be installed in the correct version in order for the script to work. Make sure to install them exactly as specified in `requirements.txt`

1. Pull this repository.
2. Install python packages with `pip install -r requirements.txt`.
3. *(Optional)* Check if your system works by executing the demo script with `python DEMO_imgToCNC.py`. A connected robot is not required.
4. If everything goes well, you should be able to see the path the robot would follow when painting `source/example.jpeg`. Configure `config.py` and check the results with the demo script, until you understand all settings.

### KRC

> I strongly recommend to refer to the *KUKA.Ethernet KRL 3.0* manual
> for more details on these steps. If you already have an Ethernet
> connection established, you don't need most of the following.

1. Install Ethernet-KRL via WorkVisual on the KRC.
2. Connect Server and KRC with an Ethernet cable. Use KLI-ready interfaces, such as X69 or X66.
3. Assign your Server an IP (e.g. 172.31.1.100) and do the same with your KRC (e.g. 172.31.1.147).
4. Modify Host IP and Port in `config.py` according to step 3.
5. Modify IP and Port in the XML config `xmlPaintImage.xml` according to step 3.
6. Copy `xmlPaintImage.xml` to *C:\KRC\ROBOTER\Config\User\Common\EthernetKRL* on the robot control.
7. Copy `paintImage.src` and `paintImage.dat` in your projects folder on the KRC.
8. *(Optional)* Use WorkVisual or the KUKA Testserver program, to ensure an Ethernet KRL connection is established.

### Physical setup
1. Calibrate your tool. Select *Tool[2]:pinselC* or create a new one and modify `paintImage.src`  according to your tool number and -name.
2. Place your canvas. This can be anything from a wall to a car component. Placing the canvas horizontal is recommended, when using water- or oil-based paints to prevent paint from flowing down.
3. Calibrate the canvas with your tool selected. Select *Base[3]:canvas1* or create a new base and modify `paintImage.src`  according to your base number and -name.
4. *(Optional)* Place containers with paint, water and paper for drying beside the robot. This is only required, if you want the robot to pick up paint and wash the brush. A gripper and a bunch of brushes sunken into paint would be preferable, but needs modifications in the code.

### Robot

> Although the .src and .dat files are useful for a quick setup, it's still recommended to heavily modify them or better create your KRL program from scratch for maximum safety and compatibility with your physical setup. See `xmlPaintImage.xml` for what kind of data is send to the robot.

1. Reteach some safety points used in `paintImage.src`. If you encounter errors at PTP-points that have been teached, instead of loaded from XML, it's likely a safety checkpoint used to switch between bases, without the arm moving. Reteach them with your new tool and base or delete them entirely.
2. *(Optional)* Teach colorHome(). A sub-program needed to place the arm above the paint containers. ⚠️ Delete any instances from `paintImage.src`, if not needed.
3. *(Optional)* Teach water() and drying(). These are sub-programs needed for removing paint from the brush and drying it. ⚠️ Delete any instance from `paintImage.src`, if not needed.
4. *(Optional)* Teach l1c1() to l4c3(). Also sub-programs needed for dipping the brush in new paint from a container. Create as many of these, as you have colors to choose from. ⚠️ Delete any instance from `paintImage.src`, if not needed.

# Starting the painting process
Choose your settings in `config.py` (see below) and check it's outcome with `python DEMO_imgToCNC.py` until you're happy with the configuration. Start the tool with `python imgToCNC.py` on the server and play `paintImage.src` on your robot in T2 or Automatic to start the painting process.

![image](https://user-images.githubusercontent.com/26855197/65393101-e342cd80-dd7c-11e9-96b4-d4c32dade990.png)

ℹ️ The python tool will do a security check, after which it prints an easy-to-read summary of your configuration and asks for final confirmation. Should any values exceed the expected range, it will print a "Warning" or a "Danger". This eliminates the accidental input of dangerously high or low values.

> The time to finish greatly varies and can take up to a whole day. A stroke-only painting with only one color and few paths will need 2 hours to finish, but can be accelerated with modifications. Due to redundant edge paths, most stroke-only paintings will be 'done' after 30 minutes or so, before the robot only paints over existing strokes.

# Configuration
This explains the parameters found in `config.py`, as well as how to choose a safe setup that creates good results.

#### Network
 - `host` IP of your server.
 - `port` Port of your server.
#### Image source
 - `imgPath` `<path to file>` Paint a specific image.
 - `imgRandom` `<path to folder>` Choose a random image in a folder.
 - ***Future feature*** `imgGenerate` `<face>` `<abstract>` `<portrait>` Generate new image with GAN. Generates realistic faces, abstract art or portrait art.
#### Color palette
 - `genreType` `<palette name>` Choose the name of the color palette defined in `colors.py`.
#### Setup
 - `canvasWidth` `<mm>` Width of your canvas. ⚠️ This acts as a security feature, as the program will exit, when coordinates are generated, that lay outside of the designated painting space.
 - `canvasHeight` `<mm>` Height of your canvas.
 - `brushSize` `<mm>` Diameter of the paint tool. May be an approximate value. ℹ️ Lower it's value, if there is too much empty space between brush strokes. ℹ️ Increase this value to something extremely high (e.g. 800) to achieve a contour only painting.
 - `strokeLength` `<mm>` Distance in mm painted, after the brush will stop and refresh the paint, to prevent a dried out stroke. Lower this value if the brush looses too much paint, before refreshing it.
 - `toolDepth` `<mm>` Defines how deep the tool will push into the canvas (Z-axis). This is needed, when the tool requires pressure to properly paint. ⚠️ Warning: This will cause high pressure and may cause serious damage if neither tool, nor canvas are flexible. ℹ️ Slowly increase this value for a thicker and stronger stroke.
#### Fine-tuning *(Optional)*
ℹ️ The quality of the output can be changed drastically with these parameters. Try them out with the demo tool.
 - `imgScale` `<multiplier>` Scale your image up or down. ℹ️ A smaller image will be painted significantly faster. Aim for around 400x400 pixels.
 - `denoise` `<value>` Reduce noise and complexity in the source image. 10 or higher is recommended. Check denoised images of `DEMO_imgToCNC.py` in `/source`.
 - `blur` `<odd value>` Blur the image to reduce noise and complexity.
 - `threshColor` `<0-254>` [Reduce colors with thresholding](https://en.wikipedia.org/wiki/Thresholding_%28image_processing%29) instead of color palette matching. May create better color fields. Deactivate with negative value. Recommended 125. Default -1.

# Example
 
![image](https://user-images.githubusercontent.com/26855197/65393210-35d0b980-dd7e-11e9-91fa-6115039eb832.png)
**Example output:** Face generated with [StyleGAN](https://github.com/NVlabs/stylegan). 1. Denoised and blurred image. 2. Color reduced and matched image. 3. Final paths in green.
```python
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
brushSize = 5 # Diameter of the brush in mm. Defines the size of the gap between
each brush stroke.
strokeLength = 150 # Maximum length of a stroke in mm, before the robot refreshes paint.
toolDepth = 0 # How deep the tool pushes into the canvas. Necessary for flexible tool or canvas, but dangerous if both are rigid.

# Fine-Tuning (Optional)
imgScale = 0.3 # Scale your image up or down for less complexity and painting time. Value Multiplies width and height.
denoise = 10 # Denoises image. This greatly reduces complexity and painting time. Default: 10. No denoise: 0.
blur = 3 # Blurs image to reduce complexity. Value in pixels. Requires odd value.
threshColor = -1 # Choose value between 0-254 (125 recommended). Negative value deactivates threshold color quantization (Default).
```
**Above:** The `config.py` used for the output.
# Recommendations
I recommend to paint on a horizontal laying strong paper with black paint only. Multi-colored full-area paintings are only usable after lots of fine tuning with good tools. Use a specific image with `imgPath` that proves suitable, instead of random ones and use very high `brushSize` values, to force a contour only painting. Try high `blur` and/or `denoise` values (e.g. 33), to simplify the source image. I highly recommend to work with pre-generated faces from the StyleGAN (Kerras et al.). Downscale larger images to ~400x400 px with `imgScale`. Full color paintings barely work with acrylic and need lot's of paint-layers. By far the easiest approach would be to use a professional painting effector and an edited source image with very few colors or one that only consists of contours (edited with e.g. Photoshop). Play with your config and test it with `DEMO_imgToCNC.py`. Results are visible in `/demo_results`. Speed and movements can be adjusted in the `paintImage.src` KRL file, which should be modified anyways.

# Safety

Regardless of the seemingly high complexity, this process has a limited area of action. However, all personell-teached movements (Start-Up, Taking Paint, Washing, Drying, etc.) happen in a larger area and therefore need careful programming and testing. The auto-generated coordinates on the other side, only act in 2 dimensions and shouldn't exceed the value of the `canvasWidth` or `canvasHeight` parameter. If your canvas base is measured correctly and the canvas size is configured properly, the program should stop itself from leaving the canvas during the painting process. Make sure to leave enough space above the canvas, as the arm will rise 300mm above it, when jumping to new paths. Be careful with the `toolDepth` value, as it will push your tool into the canvas. A process needed for flexible tools or canvas, but very dangerous when both of those are rigid.

#### ⚠️ The author of this repository takes absolutely no responsibility for any kind of damage done with this project. This is not a tool tested for any kind of safety and can/will cause serious harm, injuries and death when used improperly. This code is not safe and should never be used in production.
