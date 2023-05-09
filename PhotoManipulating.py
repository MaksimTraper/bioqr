import inspect
import os
import pathlib

import numpy as np
import cv2
from PIL import Image
import dlib
from tkinter import filedialog as fd
from os.path import dirname as up

def loadPhotoPath():
    global photoPath
    photoPath = fd.askopenfilename()
    root_proj = os.getcwd()
    rel_path = os.path.relpath(photoPath, root_proj+'/photos')
    global scetchPath
    scetchPath = up(up(photoPath)) + '/sketches/' + rel_path[0].upper() + '2' + rel_path[1:8:1] + '-sz1.jpg'
    return photoPath, scetchPath
    f = '4'
def load_photo_2variants(name):
    root_proj = os.getcwd()
    rel_path = os.path.relpath(name, root_proj)
    photo = cv2.imread(rel_path)
    photoPIL = Image.open(pathlib.Path(name))
    return photo, photoPIL

def load_photo(name):
    photo = cv2.imread(name)
    return photo

def cvt_to_gray(photo):
    gr_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    return gr_photo

def crop_image(photo, photoPIL, name):
    # Загрузка компонентов, обнаруживающих АПТ и из запись
    detector = dlib.get_frontal_face_detector()
    gr_photo = cvt_to_gray(photo)
    faces = detector(gr_photo)
    face = faces[0]
    width = face.right() - face.left()
    height = face.bottom() - face.top()
    differ = 200 - width
    right = face.right() + differ / 2
    top = face.top() - differ
    left = face.left() - differ / 2
    bottom = face.bottom()
    while ((right - left) != 200 or (bottom - top) != 200):
        if ((right - left) != 200):
            if (right - left) > 200:
                right -= 1
            else:
                right += 1
        if ((bottom - top) != 200):
            if (bottom - top) > 200:
                top += 1
            else:
                top -= 1
    cropped_image = photoPIL.crop((left, top, right, bottom))
    if(name == 'photo'):
        cropped_image.save('cropped_photo.jpg')
    else:
        cropped_image.save('cropped_scetch.jpg')
    return cropped_image

def dividePhotoOnRGB(photo):
    b, g, r = np.array_split(photo, 3, axis=2)
    return r, g, b