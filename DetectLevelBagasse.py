# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 23:25:23 2020

@author: Eduardo
@e-mail: eduardocarvalho-1992@hotmail.com
"""

import cv2

class DetectLevelBagasse():
    
    def __init__(self, calibration_image, resize_x, resize_y):
        self.calibration_image = calibration_image
        self.resize_x = resize_x
        self.resize_y = resize_y
        self.center = (0,0)
        
        pass
    
    def read_image(image_file):
        """
        Read an image    
        Parameters
        ----------
        image_file : String
            Image file path
            
        Returns
        -------
        image : Array of unit8 or None
            Returns a color image or return None (if there is an error).
        """
        try:
            image = cv2.imread(image_file)
            return image
        except:
            print('[ERROR]: could not read image')
            return None
        
    def bgr_gray(image):  
        """    
        Convert BGR to Gray using the OpenCV
        Parameters
        ----------
        image : Array of uint8
            A color image
        Returns
        -------
        image_gray : Array of uint8 or None
            Return the grayscale image or return None (if there is an error)
        """   
        try:
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        
            return image_gray
        except:
            print('[ERROR]: could not read image ')
            return None
    
    def detect_circles(image):
        """
        Detect cicle using the HoughCircles fuction from OpenCV
        Parameters
        ----------
        image : Array of uint8
            A grayscale image with a Gaussian Blur Filter
        Returns
        -------
        circles : Array of float32 or None
            Returns the detector circles with coordinates and radius 
            or returns None (if there is an error)
        """    
        try:
            if len(image.shape) > 2:
                print('[ERROR]: Dimension > 2. Is an image gray?')
                return None
            
            circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1, 
                                       image.shape[0]/8, param1=100,
                                       param2=50,minRadius=0,maxRadius=0)        
            if len(circles) == 0:
                print('[ERROR]: not possible to detect circles')
                return None            
            else:
                return circles
        except:
            print('[ERROR]: could not detect circles')
            return None
    
    
    

