import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *

import cv2
import dlib
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

import GeneratorQR
import PhotoManipulating


def openStartWindow():
     startwindow = tk.Tk()
     startwindow.geometry('300x250')
     startwindow.title("Стартовое окно")

     mes = tk.Label(startwindow, text = 'Выберите вариант работы программы:')
     btnManualCreateQR = tk.Button(startwindow, text="Ручное формирование QR-кода", command=openWinManualGenQR)
     btnAutoCreateQRs = tk.Button(startwindow, text="Подборка QR-кодов", command=openWinAutoGenQR)

     mes.pack(ipadx=20, ipady=20)
     btnManualCreateQR.pack(ipadx=10, ipady=10, padx=10, pady=10)
     btnAutoCreateQRs.pack(ipadx=10, ipady=10, padx=10, pady=10)

     startwindow.mainloop()
     return None

def openWinAutoGenQR():
     photo = PhotoManipulating.load_photo('cropped_image.jpg')
     photo = cv2.resize(photo, (177, 177))
     gr_photo = PhotoManipulating.cvt_to_gray(photo)

     scetch = PhotoManipulating.load_photo('cropped_scetch.jpg')
     scetch = cv2.resize(scetch, (177, 177))

     detector = dlib.get_frontal_face_detector()
     faces = detector(gr_photo)
     face = faces[0]

     antro = np.array(['4-May-2023', '/Facial Anthropometric Point', 'Base CUFS: Female f-008-01 /#', [250, 200]],
                      dtype=object)
     info = np.array(['Base CUFS', 'Female f-008-01', 'http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html'])
     pheno = np.array(['4-May-2023', '/Facial Anthropometric Point', 'Photo: 01 /#'])

     generator = GeneratorQR.GeneratorQRCodes(photo, scetch, antro, info, pheno)

     generator.getAntroPhenoMas(photo, face)
     generator.genQRCodes(photo, face, antro, info, pheno)
     generator.loadQRCodes()
     BioQRCode1 = generator.genBIOQRCodes('Photo', 'Info', 'Antro')
     BioQRCode2 = generator.genBIOQRCodes('Photo', 'Info', 'Photo')
     BioQRCode3 = generator.genBIOQRCodes('Photo', 'Info', 'Scetch')
     BioQRCode4 = generator.genBIOQRCodes('Photo', 'Antro', 'Pheno')
     BioQRCode5 = generator.genBIOQRCodes('Photo', 'Info', 'Pheno')
     BioQRCode6 = generator.genBIOQRCodes('Photo', 'Scetch', 'Pheno')
     QRCodes = [BioQRCode1, BioQRCode2, BioQRCode3, BioQRCode4, BioQRCode5, BioQRCode6]
     names = ['PIA (Photo/Info/Antro)', 'PIP (Photo/Info/Photo)', 'PIS (Photo/Info/Scetch)',
              'PAPh (Photo/Antro/Pheno)', 'PIPh (Photo/Info/Pheno)', 'PSPh (Photo/Scetch/Pheno)']

     pic_box=plt.figure(num="Автоматическая генерация BIO QR-codes", figsize=(8, 6), dpi=80)

     #Сохранение QR-кодов в директорию проекта
     #for i in range(1,7,1):
          #filename = 'BioQRCode' + str(i) + '.jpg'
          #cv2.imwrite(filename, QRCodes[i-1])

     for i in range(1, 7, 1):
          #filename = 'BioQRCode' + str(i) + '.jpg'
          #image = plt.imread(filename)
          plt.subplot(2, 3, i)
          plt.imshow(QRCodes[i-1])
          plt.title(names[i-1])
          plt.axis('off')

     plt.show()
     return None

def openWinManualGenQR():
     def selected1(event):
          val = str(combobox1.get())
          global select1
          select1 = val
          return None
     def selected2(event):
          val = str(combobox2.get())
          global select2
          select2 = val
          return None
     def selected3(event):
          val = str(combobox3.get())
          global select3
          select3 = val
          return None

     winManualGenQR = tk.Tk()
     winManualGenQR.geometry('300x250')
     winManualGenQR.title("Ручная генерация BIO QR-code")

     namesVariables = ['Antro', 'Info', 'Pheno', 'Photo', 'Scetch']

     mes = tk.Label(winManualGenQR, text='Соберите собственный BIO QR-код по частям:')
     combobox1 = ttk.Combobox(winManualGenQR, values=namesVariables, state='readonly')
     combobox2 = ttk.Combobox(winManualGenQR, values=namesVariables, state='readonly')
     combobox3 = ttk.Combobox(winManualGenQR, values=namesVariables, state='readonly')
     combobox1.current(3)
     combobox2.current(1)
     combobox3.current(4)
     label1 = tk.Label(winManualGenQR, text='Красный слой')
     label2 = tk.Label(winManualGenQR, text='Зелёный слой')
     label3 = tk.Label(winManualGenQR, text='Синий слой')
     global select1, select2, select3
     select1, select2, select3 = combobox1.get(), combobox2.get(), combobox3.get()
     btnManualCreateQR = tk.Button(winManualGenQR, text="Сформировать", command=genManualQR)

     mes.pack()
     label1.pack()
     combobox1.pack(padx=6, pady=6)
     label2.pack()
     combobox2.pack(padx=6, pady=6)
     label3.pack()
     combobox3.pack(padx=6, pady=6)
     btnManualCreateQR.pack()

     combobox1.bind("<<ComboboxSelected>>", selected1)
     combobox2.bind("<<ComboboxSelected>>", selected2)
     combobox3.bind("<<ComboboxSelected>>", selected3)
     winManualGenQR.mainloop()
     return None

def genManualQR():
     photo = PhotoManipulating.load_photo('cropped_image.jpg')
     photo = cv2.resize(photo, (177, 177))
     gr_photo = PhotoManipulating.cvt_to_gray(photo)

     scetch = PhotoManipulating.load_photo('cropped_scetch.jpg')
     scetch = cv2.resize(scetch, (177, 177))

     detector = dlib.get_frontal_face_detector()
     faces = detector(gr_photo)
     face = faces[0]

     antro = np.array(['4-May-2023', '/Facial Anthropometric Point', 'Base CUFS: Female f-008-01 /#', [250, 200]],
                      dtype=object)
     info = np.array(['Base CUFS', 'Female f-008-01', 'http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html'])
     pheno = np.array(['4-May-2023', '/Facial Anthropometric Point', 'Photo: 01 /#'])

     generator = GeneratorQR.GeneratorQRCodes(photo, scetch, antro, info, pheno)

     generator.getAntroPhenoMas(photo, face)
     generator.genQRCodes(photo, face, antro, info, pheno)
     generator.loadQRCodes()
     BioQRCode = generator.genBIOQRCodes(select1, select2, select3)

     name = select1[0]+select2[0]+select3[0]+': '+select1+'/'+select2+'/'+select3
     plt.subplots(1, 1, figsize=(7, 7), num='Сгенерированный BIO QR-code')
     plt.imshow(BioQRCode)
     plt.title(name)
     plt.axis('off')

     plt.show()