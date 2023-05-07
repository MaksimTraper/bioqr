import numpy as np
import cv2
from PIL import Image
import dlib

def load_photo_2variants(name):
    photo = cv2.imread(name)
    photoPIL = Image.open(name)
    return photo, photoPIL

def load_photo(name):
    photo = cv2.imread(name)
    return photo

def cvt_to_gray(photo):
    gr_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    return gr_photo

def crop_image(photo, photoPIL):
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
    return cropped_image

def dividePhotoOnRGB(photo):
    b, g, r = np.array_split(photo, 3, axis=2)
    return r, g, b