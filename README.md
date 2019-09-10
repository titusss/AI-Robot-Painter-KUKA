<h1 align="center">
	<img
		alt="KUKA Robot and Canvas"
		src="https://titusebbecke.com/images/pba-img04.jpg">
</h1>

<h3 align="center">
	Load any image or let an AI generate one and paint it on canvas with a KUKA industrial robot
</h3>

<p align="center">
	<a href="https://titusebbecke.com/"><img
		alt="website"
		src="https://img.shields.io/badge/website-pending-blue"</a>
	<a href="https://vimeo.com/354081387"><img
		alt="demo video"
		src="https://img.shields.io/badge/demo-pending-blue?logo=Vimeo"</a>
</p>

## Overview

- **Paints or draws anything.** Paint any kind of single-, or multi-colored picture with your KUKA robot.
- **Multicolor.** Choose as many colors as you want. Supports acrylic, oil, pencil and many more.
- **Flexible setup.** Setup in 10 minutes. Only needs to calibrate canvas base and teach color refilling or tool switching paths.
- **Pretty safe.** Only generates 2D-coordinates that fit the canvas size, set by the user.
- **Easy to configure.** Use the intuitive python CLI-tool or change the reasonably messy python code.

## What you need

- **KUKA robot.** This project was tested with a KR 10 R1420, but should work with any 3D-CNC device.
- **KRC w. Ethernet-KRL*.** Use this KUKA package to communicate with your server via Ethernet.
- **Server.** A laptop or similar, that is connected to the KRC via Ethernet and communicates over KLI.
- **Python 3.** Install python on the server. I recommend an <a href="https://www.anaconda.com/distribution/">anaconda install</a>.
- **Utilities.** Any kind of painting device attached to the robot, a canvas to draw on, paint and water (Optional).

*Please note, that this project focuses on generating XYZ-coordinates from an input image in near real-time. In theory any kind of interface could be used here. Generating a complete array of coordinates and transfering the batch to the robot control afterwards (via USB-Stick e.g.) is possible with a few modifications.
