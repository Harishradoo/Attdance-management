# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:29:01 2019

@author: Internship007
"""
# importing necessary packages
from os import listdir, mkdir, getcwd
from os.path import isdir, exists
import sys
import pickle
import shutil  # for removing dir with contents
from PIL import Image, ImageEnhance
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC


def extract_face(filename, required_size=(160, 160)):
    """Extract a single face from a given photograph."""
    # load image from FILE
    image = Image.open(filename)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.8)
    pixels = asarray(image)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    # bug fix for list index out of range
    try:
        x_1, y_1, width, height = results[0]['box']
    except IndexError:


def load_faces(directory):
    """Load images and extract faces for all images in a directory."""
    faces = list()
    # enumerate FILEs
    for filename in listdir(directory):
        # path
        path = directory + filename
        # data generator for augmentation
        datagen = ImageDataGenerator(rotation_range=10, width_shift_range=0.1,
                                     height_shift_range=0.1, shear_range=0.15,
                                     zoom_range=0.1, channel_shift_range=10,
                                     horizontal_flip=True)
        image = Image.open(path)
        image = img_to_array(image)
        image = expand_dims(image, 0)
        # create new directory for augmentations in current working dir(cwd)
        dest = getcwd() + '/aug'
        mkdir(dest)
        datagen.fit(image)
        # to set default value of number of augmentations if not specified
        if len(sys.argv) < 3:
            augs_num = 30
        else:
            augs_num = int(sys.argv[2])
        i = 0
        # loop variable for augmentation
        for _ in datagen.flow(image, batch_size=1, save_to_dir=dest,
                              save_prefix='aug', save_format='jpg'):
            i += 1
            # second argument in cmd line will be number of iterations
            if i == augs_num:
                break
        dest = dest + '/'