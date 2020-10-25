# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 17:42:28 2020

@author: Eduardo
e-mail: eduardocarvnunes@gmail.com
"""

import cv2
import DetectLevelBagasse as detector

def detect_volume():
    _, _, _, i_bin_calibrate = detector.get_ROI(image="", path_image_calibrate="images/image_calibrate.png", 
                              calibrate=True)
    
    number_white_pixels_calibrate = detector.count_white_pixels(i_bin_calibrate)   
    
    cap = cv2.VideoCapture("videos/video_level_bagasse.mp4")
    count = 0
    
    while(True):
        
        ret, frame = cap.read()
        
        frame_show = cv2.resize(frame, (680,382))  
        
        cv2.imshow('Frames RGB', frame_show)
        
        count = count + 1
    
        if(count == 15):
            count = 0
            
            i_r, i_g, i_n, i_b = detector.get_ROI(image=frame, calibrate=False)
            
            number_white_pixels_input = detector.count_white_pixels(i_b)
            
            nivel = detector.calculate_volume(number_white_pixels_input, 
                                     number_white_pixels_calibrate)
            
            print ('Level of bagasse: ' + str(nivel) + '%')
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            nivel_show = 'Nivel: ' + str(nivel) + '%'
            cv2.putText(i_b, str(nivel_show),(10,350), font, 2, (255,255,255), 2,
                        cv2.LINE_AA)
            
            #cv2.imshow('Frames RGB', i_r)
            cv2.imshow('Frames Gray', i_g)
            cv2.imshow('Frames Blur', i_n)
            cv2.imshow('Frames Bin', i_b)
        
           
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    
    detect_volume()