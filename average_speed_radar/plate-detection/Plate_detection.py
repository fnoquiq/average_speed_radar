import os
from PIL import Image
import numpy as np
import tkinter
import pytesseract
import cv2



def desenhaContornos(contornos, imagem):
    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 150:
            # aproxima os contornos da forma correspondente
            approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            # verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
            if len(approx) == 4:
                # cv2.drawContours(imagem, [c], -1, (0, 255, 0), 1)
                (x, y, a, l) = cv2.boundingRect(c)
                cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)
                roi = imagem[y:y + l, x:x + a]

                cv2.imshow('RES', roi)
                cv2.waitKey(400)

    return imagem


def detect_plate(path_and_filename):
    frame = cv2.imread(path_and_filename)

    # limite horizontal
    # cv2.line(frame, (0, 350), (860, 350), (0, 0, 255), 1)
    # limite vertical 1
    # cv2.line(frame, (220, 0), (220, 480), (0, 0, 255), 1)
    # limite vertical 2
    # cv2.line(frame, (500, 0), (500, 480), (0, 0, 255), 1)

    cv2.imshow('SAIDA', frame)

    # região de busca
    #res = frame[350:, 220:500]

    # escala de cinza
    frame_modified = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # limiarização
    ret, frame_modified = cv2.threshold(frame_modified, 90, 255, cv2.THRESH_BINARY)

    # desfoque
    frame_modified = cv2.GaussianBlur(frame_modified, (25, 25), 0)

    # lista os contornos
    contornos, hier = cv2.findContours(frame_modified, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cv2.imshow('RES', frame)

    desenhaContornos(contornos, frame)

    cv2.destroyAllWindows()


path = './sample_images/positive/'

images_paths=[os.path.join(path,f) for f in os.listdir(path)]
for image_path in images_paths:
    detect_plate(image_path)
