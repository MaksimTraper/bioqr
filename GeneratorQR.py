import cv2
import dlib
import numpy as np
import qrcode

import PhotoManipulating
class GeneratorQRCodes:

    photo = None
    grPhoto = None
    scetch = None
    grScetch = None
    antro = np.array([])
    info = np.array([])
    pheno = np.array([])
    gr_Img_ANTRO_QR = None
    gr_Img_INFO_QR = None
    gr_Img_PHENO_QR = None
    r = np.array([],[])
    g = np.array([])
    b = np.array([],[])

    def __init__(self, photo, scetch, antroIn, infoIn, phenoIn):
        self.scetch = scetch
        self.grScetch = PhotoManipulating.cvt_to_gray(scetch)
        self.photo = photo
        self.grPhoto = PhotoManipulating.cvt_to_gray(photo)
        detector = dlib.get_frontal_face_detector()
        faces = detector(self.grPhoto)
        face = faces[0]
        self.r, self.g, self.b = PhotoManipulating.dividePhotoOnRGB(photo)
        xy, bright_coord = GeneratorQRCodes.getAntroPhenoMas(self, photo, face)
        self.antro = np.append(antroIn, xy)
        self.info = infoIn
        self.pheno = np.append(phenoIn, bright_coord)

    def getAntroPhenoMas(self, photo, face):
        gr_photo = PhotoManipulating.cvt_to_gray(photo)
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        landmarks = predictor(gr_photo, face)
        x = np.array([])
        y = np.array([])
        b_br = np.array([])
        g_br = np.array([])
        r_br = np.array([])
        for n in range(0, 68):
            x = np.append(x, landmarks.part(n).x)
            y = np.append(y, landmarks.part(n).y)
            b_br = np.append(b_br, self.b[int(y[n]), int(x[n])])
            g_br = np.append(g_br, self.g[int(y[n]), int(x[n])])
            r_br = np.append(r_br, self.r[int(y[n]), int(x[n])])
        xy = np.concatenate((x, y))
        bright_coord = np.concatenate((r_br, g_br, b_br))
        return xy, bright_coord

    def genQRCodes(self, photo, face, antroIn, infoIn, phenoIn):
        INFO_QR = qrcode.QRCode(box_size=3, border=7)
        ANTRO_QR = qrcode.QRCode(box_size=1)
        PHENO_QR = qrcode.QRCode(box_size=1)

        ANTRO_QR.add_data(self.antro)
        ANTRO_QR.make(fit=True)
        INFO_QR.add_data(self.info)
        INFO_QR.make(fit=True)
        PHENO_QR.add_data(self.pheno)
        PHENO_QR.make(fit=True)

        #Алгоритм увеличения разрешения каждого QR-кода >200 на 200
        #QRs = [INFO_QR, ANTRO_QR, PHENO_QR]
        #for i in range(0, 3, 1):
        #    resolution = (17 + 4*QRs[i].version + QRs[i].border*2)*QRs[i].box_size
        #    add = 0
        #    while(resolution<200):
        #        add += 1
        #        resolution = (17 + 4*QRs[i].version + QRs[i].border*2)*(QRs[i].box_size+add)
        #    QRs[i].box_size += add-1
        #    resolution = (17 + 4 * QRs[i].version + QRs[i].border*2) * QRs[i].box_size
        #    add = 0
        #    while(resolution<200):
        #        add += 1
        #        resolution = (17 + 4 * QRs[i].version + (QRs[i].border+add)*2) * QRs[i].box_size
        #    QRs[i].border += add

        Img_INFO_QR = INFO_QR.make_image()
        Img_INFO_QR.save('INFO_QR.jpg')
        Img_ANTRO_QR = ANTRO_QR.make_image()
        Img_ANTRO_QR.save('ANTRO_QR.jpg')
        Img_PHENO_QR = PHENO_QR.make_image()
        Img_PHENO_QR.save('PHENO_QR.jpg')
        return None

    def loadQRCodes(self):
        Img_ANTRO_QR = cv2.imread('ANTRO_QR.jpg')
        Img_INFO_QR = cv2.imread('INFO_QR.jpg')
        Img_PHENO_QR = cv2.imread('PHENO_QR.jpg')

        Img_ANTRO_QR = cv2.resize(Img_ANTRO_QR, (200, 200))
        Img_INFO_QR = cv2.resize(Img_INFO_QR, (200, 200))
        Img_PHENO_QR = cv2.resize(Img_PHENO_QR, (200, 200))

        #Алгоритм доведения разрешения каждого QR-кода до разрешения 200 на 200
        #Обрезаются белые поля
        #Img_ANTRO_QR = np.array(Img_ANTRO_QR)
        #Img_INFO_QR = np.array(Img_INFO_QR)
        #Img_PHENO_QR = np.array(Img_PHENO_QR)

        #QRs = [Img_INFO_QR, Img_ANTRO_QR, Img_PHENO_QR]
        #for i in range (0, 3, 1):
        #    rows, cols, layers = QRs[i].shape
        #    while(rows > 200):
        #        if (rows%2!= 0):
        #            QRs[i] = np.delete(QRs[i], 0, 0)
        #            QRs[i] = np.delete(QRs[i], 0, 1)
        #            rows, cols, layers = QRs[i].shape
        #Img_INFO_QR = QRs[0]
        #Img_ANTRO_QR = QRs[1]
        #Img_PHENO_QR = QRs[2]

        self.gr_Img_ANTRO_QR = cv2.cvtColor(Img_ANTRO_QR, cv2.COLOR_BGR2GRAY)
        self.gr_Img_INFO_QR = cv2.cvtColor(Img_INFO_QR, cv2.COLOR_BGR2GRAY)
        self.gr_Img_PHENO_QR = cv2.cvtColor(Img_PHENO_QR, cv2.COLOR_BGR2GRAY)
        return None

    def genBIOQRCodes(self, nameOnRed, nameOnGreen, nameOnBlue):
        namesVariables=['Antro', 'Info', 'Pheno', 'Photo', 'Scetch']
        namesParameters = [nameOnRed, nameOnGreen, nameOnBlue]
        #Заполняем массив фиктивными переменными. В последствии, часть из них будут заменены
        parameters = [self.grPhoto, self.grPhoto, self.grPhoto]
        for y in range(0,3,1):
            match namesParameters[y]:
                case 'Antro':
                    parameters[y] = self.gr_Img_ANTRO_QR
                case 'Info':
                    parameters[y] = self.gr_Img_INFO_QR
                case 'Pheno':
                    parameters[y] = self.gr_Img_PHENO_QR
                case 'Photo':
                    parameters[y] = self.grPhoto
                case 'Scetch':
                    parameters[y] = self.grScetch
        r = cv2.addWeighted(self.r, 0, parameters[0], 1, 0)
        g = cv2.addWeighted(self.g, 0, parameters[1], 1, 0)
        b = cv2.addWeighted(self.b, 0, parameters[2], 1, 0)
        BioQRCode = cv2.merge((b, g, r))
        return BioQRCode