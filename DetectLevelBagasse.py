# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 23:25:23 2020

@author: Eduardo
@e-mail: eduardocarvalho-1992@hotmail.com
"""

import cv2
import numpy as np
import yaml

    
# load parameter.yaml
def yaml_load():
    with open("parameter.yaml") as stream:
        param = yaml.safe_load(stream)
    return param
   

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
    
def blur_image(image_gray, kernel):
    """
    Smoothing Images using median Blur from the OpenCV library

    Parameters
    ----------
    image_gray : Array of uint8
        Grayscale image

    Returns
    -------
    image_blur : Array of uint8 or None
        Returns a grayscale image with a Gaussian Blur Filter 
        or returns None (if there is an error)
    """
    try:               
        image_blur = cv2.medianBlur(image_gray, kernel)
                    
        if len(image_blur.shape) > 2:
            print('[ERROR]: Dimension > 2. Is an image gray?')
            return None
        else:
            return image_blur
    except:
        print('[ERROR]: could not convert image')
        return None
    
def threshold(image, th):
    """
    Segments the image using the threshold function of the OpenCV library
    Parameters
    ----------
    image_gray : Array of uint8
        Grayscale image
        
    th : int
        Threshold for segmentation
    Returns
    -------
    image_bin : Array of uint8
        Returns a segmented image with a value of 0 (black pixels) and 
        255 (white pixels) or returns None (if there is an error)
    """
    
    try:
        if len(image.shape) > 2:
            print('[ERROR]: Dimension > 2. Is an image gray?')
            return None 
          
        ret, image_bin = cv2.threshold(image, th, 255, cv2.THRESH_BINARY)
    
        return image_bin
    except:
        print('[ERROR]: could not segmentation image')
        return None
    

def get_ROI(image=None, path_image_calibrate=None, calibrate=True):
    """
    Here we take the area of interest(ROI) so we can calculate the volume

    Parameters
    ----------
    image : Array of uint8 (image) 
        DESCRIPTION. If not calibrate         
    path_image_calibrate : String
        DESCRIPTION. Image path of calibration
    calibrate : Boolean
        DESCRIPTION. The default is True.

    Returns
    -------
    image_resize : Array of uint8 (image)
        DESCRIPTION. Image resize (382x680)
    image_gray : Array of uint8 (image)
        DESCRIPTION. Image gray
    new_image : Array of uint8 (image)
        DESCRIPTION. Image that show the volume of the area of interest 
    image_bin : Array of uint8 (image)
        DESCRIPTION. Image segmentation (binary)

    """
    
    try:
        if calibrate:            
            image = read_image(path_image_calibrate)        

        image_resize = cv2.resize(image, (680,382))
        image_gray = bgr_gray(image_resize)
        circle = detect_circles(image_gray)
        circle = np.uint16(np.around(circle))
        # get center of visor circle
        center = (circle[0][0][0],circle[0][0][1])
        # get radius of visor circle
        #radius = circle[0][0][2]
        size = 382, 680
        # black image 382x680 
        mask = np.zeros(size, dtype=np.uint8)
        # white circle with radius 80
        cv2.circle(mask,center, 80, (255,255,255), -1,8,0)
        # operation bit the bit for add black image in visor
        new_image = cv2.bitwise_and(image_gray, mask)
        # medianBlur filter for remove the noises in the circle
        new_image = blur_image(new_image, 15)
        # segmentation of image with threshold
        image_bin = threshold(new_image, 180)

        return image_resize, image_gray, new_image, image_bin      
        
    except:
        print('[ERROR]: some error')
        return None

def count_white_pixels(image):
    """
    Amount white pixels in the image. I used tha amount white pixels for 
    measure the percentage of the bagasse # e.g. If there are 1000 white pixels
    in the circle then 1000 white pixels represent 0% level of bagasse 
    500 white pixels represent 50% level of bagasse

    Parameters
    ----------
    image : Array of uint8 (image)
        DESCRIPTION.

    Returns
    -------
    n_white : TYPE
        DESCRIPTION.

    """
    
    
    try:
        n_white = cv2.countNonZero(image)
        return n_white
    except:
        print('[ERROR]: some error ')
        return None

def calculate_volume(white_pixels_input, white_pixels_calibrate):
    """
    

    Parameters
    ----------
    white_pixels_input : TYPE
        DESCRIPTION.
    white_pixels_calibrate : TYPE
        DESCRIPTION.

    Returns
    -------
    nivel : TYPE
        DESCRIPTION.

    """
        
    result = (white_pixels_input / white_pixels_calibrate) * 100    
    
    if result > 100 or result < 0:
        nivel = 0
        
    else:
        nivel = 100 - result
        nivel = round(nivel)
        
    return nivel
    
    

 
      

    
    
        




  
    

