import cv2
from PIL import Image
import numpy as np
import os
import draw_contour_outlines
import get_contours
import filter_contours
import cvt_to
import fill_contours

def fat_separate(ofn, i, MA, mia, p):
    
    c, h = get_contours.main(ofn)
    
    draw_contour_outlines.white('blank.tif', c, 'test1.tif', i+4)
    
    draw_contour_outlines.white('blank.tif', c, 'test2.tif', i)
    fill_contours.main('test2.tif', c, 'test2.tif', (255,255,255))
    I1 = cv2.imread('test1.tif')
    I2 = cv2.imread('test2.tif')
    I3 = I1 - I2
    cv2.imwrite('test3.tif', I3)
    
    cvt_to.dilated(ofn, (3,3), i)
    c, h = get_contours.main('test3.tif')
    fill_contours.main('dilated_'+ofn, c, 'test4.tif', (0,0,0))
    c, h = get_contours.external('test4.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, p)
    c, h = filter_contours.smallest_circle(c, h, 0.2)
    fill_contours.main('blank.tif', c, 'fs_'+ofn, (255,255,255))
       
def tif(open_filename, save_filename):
    I = cv2.imread(open_filename)
    cv2.imwrite(save_filename,I)

def invert_binary(image_name, x, save_filename):    

    I = cv2.imread(image_name)
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(I_gray,x,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite(save_filename, thresh)

def eroded(image_name, kernel_size, iterate, i):

    I = cv2.imread(image_name, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    erosion = cv2.erode(I, kernel, iterations = iterate)
    cv2.imwrite(str(i)+'eroded_'+image_name, erosion)

def dilated(image_name, kernel_size, iterate):

    I = cv2.imread(image_name, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    dilation = cv2.dilate(I, kernel, iterations = iterate)
    cv2.imwrite('dilated_'+image_name, dilation)

def eroded2(ofn, sfn, kernel_size, iterate):

    I = cv2.imread(ofn, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    erosion = cv2.erode(I, kernel, iterations = iterate)
    cv2.imwrite(sfn, erosion)

def dilated2(ofn, sfn, kernel_size, iterate):

    I = cv2.imread(ofn, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size) #kernel = np.ones(kernel_size, np.uint8)
    dilation = cv2.dilate(I, kernel, iterations = iterate)
    cv2.imwrite(sfn, dilation)

def closed(image_name, kernel_size):

    I = cv2.imread(image_name, 0)
    kernel = np.ones(kernel_size, np.uint8)
    closure = cv2.morphologyEx(I, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite('closed_'+image_name, closure)

def opened(image_name, kernel_size):

    I = cv2.imread(image_name, 0)
    kernel = np.ones(kernel_size, np.uint8)
    opening = cv2.morphologyEx(I, cv2.MORPH_OPEN, kernel)
    cv2.imwrite('opened_'+image_name, opening)

def closed_opened(ofn, sfn, kernel_size):

    I = cv2.imread(ofn, 0)
    kernel = np.ones(kernel_size, np.uint8)
    closure = cv2.morphologyEx(I, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closure, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(sfn, opening)

def grad(image_name, kernel_size):
    
    #open cv says this returns the difference between
    #the dilation and erosion of an object. According to
    #my trial and error this is the dilation and then
    #subsequent erosion of the dilated image.
    #gradient with kernel = 2,2 returns a line that is
    #one pixel wide.
    
    I = cv2.imread(image_name, 0)
    kernel = np.ones(kernel_size, np.uint8)
    gradient = cv2.morphologyEx(I, cv2.MORPH_GRADIENT, kernel)
    cv2.imwrite('gradient_'+image_name, gradient)

def dusted(ofn, sfn, MA, mia):
    c, h = get_contours.main(ofn)
    c, h, a = filter_contours.size_only(c, h, MA, mia)
    fill_contours.main('blank.tif', c, sfn, (255,255,255))
    

    
    
    
    


            
            
    
