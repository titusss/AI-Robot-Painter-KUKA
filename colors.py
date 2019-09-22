#-------------------------------------------------
# Define the color values of the paint here. 
# You can create multiple color palettes or just one.
# If you want to paint in only 1 color, you still need a second color for the background.

import config as cfg
import numpy as np

#-------------------------------------------------

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

#-------------------------------------------------

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

#-------------------------------------------------

if cfg.genreType == 'portrait':
	colorPaint = np.array([deepChestnut_1, bronze_2, dutchWhite_3, bone_4, battleshipGrey_5, ashGray_6, frenchBeige_7, babyPowder_8, darkBrown_9, blueSapphire_10, coyoteBrown_11, blackChocolate_12])
elif cfg.genreType == 'abstract':
	colorPaint = np.array([cultured_1, almond_2, cadmiumRed_3, citrine_4, bdazzledBlue_5, blueGray_6, copperRed_7, burlywood_8, blackShadows_9, burnishedBrown_10, darkLiverHorses_11, black_12])