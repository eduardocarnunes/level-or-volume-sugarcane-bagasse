# Autor: Eduardo Carvalho Nunes
# email: eduardocarvalho-1992@hotmail.com
# Material level of sugarcane bagasse
# create feb 2018

from datetime import datetime
import numpy as np
import cv2


# I used this frame to get 0% of the bagasse level
frame = cv2.imread("calibrar.png")
# resize image
frame = cv2.resize(frame, (680,382))
# BGR to GRAY
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# hough transform for circle detection
circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, frame.shape[0]/8, 
                           param1=100, param2=50, minRadius=0, maxRadius=0)
# circles detect
circles = np.uint16(np.around(circles))
# center of visor circle
center = (circles[0][0][0],circles[0][0][1])
# radius of visor circle
raio = circles[0][0][2]
size = 382, 680
# black image 382x680 
mask = np.zeros(size, dtype=np.uint8)
# white circle with radius 80
cv2.circle(mask,center, 80, (255,255,255), -1,8,0)
# operation bit the bit for add black image in visor
nova_imagem = cv2.bitwise_and(frame, mask)
# medianBlur filter for remove the noises in the circle
nova_imagem = cv2.medianBlur(nova_imagem, 15)
# segmentation of image with threshold
ret, img_bin = cv2.threshold(nova_imagem, 180, 255, cv2.THRESH_BINARY)


# amount white pixels in the img_bin. I used tha amount white pixels for measure the percentage of the bagasse
# e.g. If there are 1000 white pixels in the circle then 1000 white pixels represent 0% level of bagasse
# 500 white pixels represent 50% level of bagasse

#cont_white represent o number of white pixels
cont_white = cv2.countNonZero(img_bin)

# load the video for test
cap = cv2.VideoCapture("video_level_bagasse.mp4")
contador = 0;

while(True):
    # Captura frame por frame
    ret, frame2 = cap.read()
    contador = contador + 1

    frame2 = cv2.resize(frame2, (680,382))
    cv2.imshow('Frames RGB', frame2)

    if(contador == 15):
        contador = 0;
        # I did here the same thing in the lines 11 - 38
        size2 = 382, 680
        mask2 = np.zeros(size2, dtype=np.uint8) 
        cv2.circle(mask2,center, 80, (255,255,255), -1,8,0) 
        frame_e = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) 
        cv2.imshow('RGB para escala de Cinza', frame_e)
        nova_imagem2 = cv2.bitwise_and(frame_e, mask2) 
        cv2.imshow('Circulo', nova_imagem2)
        frame_e = cv2.medianBlur(frame_e, 15) 
        #cv2.imshow('Filtro Mediana', frame_e)        
        ret2, img_bin2 = cv2.threshold(nova_imagem2, 180, 255, cv2.THRESH_BINARY) 
        cont_white2 = cv2.countNonZero(img_bin2) 
        
        resu2 = (cont_white2 / cont_white) * 100

        if resu2 > 100 or resu2 < 0:
            nivel2 =0
            print ('Level of bagasse: ' + str(nivel2) + '%')
            
        else:
            nivel2 = 100 - resu2
            nivel2 = round(nivel2)
            print ('Level of bagasse: '  +  str(nivel2) + '%')
        """
        # OPTIONAL - Save the leve in a file
        now = datetime.now()
        arquivo = open('nivel.txt', 'r') # open file
        conteudo = arquivo.readlines()
        texto = str(now.day) + '/' + str(now.month) + ': ' + str(now.hour) + 'hour = ' + str(nivel2) + '\n'
        conteudo.append(texto)   # 
        arquivo = open('nivel.txt', 'w') # Abre novamente o arquivo (escrita)
        arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
        arquivo.close()
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        nivel_show = 'Nivel: ' + str(nivel2) + '%'
        cv2.putText(img_bin2, str(nivel_show),(10,350), font, 2,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('Segmentacao Imagem', img_bin2)
       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

   

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()