#-------------------------------------------------
# FUTURE FEATURE
#
# Generates new image from GAN-trained package
# GAN, Import example created and packages trained by Kerras et. al/NVIDIA Research
# All rights to their respective owners
# More information: https://github.com/tkarras/progressive_growing_of_gans

#import tensorflow as tf
import numpy as np
#from PIL import Image
#import pickle
import config as cfg

#-------------------------------------------------

def proGanGen(genre):
    #tf.InteractiveSession()
    #with open(genre+".pkl", 'rb') as file:
    #    G, D, Gs = pickle.load(file)
    #latents = np.random.RandomState(1).randn(1000, *Gs.input_shapes[0][1:])
    print("proGan-called")
    #labels = np.zeros([latents.shape[0]] + Gs.input_shapes[1][1:])
    #images = Gs.run(latents, labels)
    #images = np.clip(np.rint((images + 1.0) / 2.0 * 255.0), 0.0, 255.0).astype(np.uint8) # [-1,1] => [0,255]
    #images = images.transpose(0, 2, 3, 1)
    #generatedImg = PIL.Image.fromarray(images, 'RGB')
    
    #generatedImg.save("demo_results/"+str(f"{datetime.datetime.now():%Y%m%d_%H-%M-%S}")
    #generatedImg.show()