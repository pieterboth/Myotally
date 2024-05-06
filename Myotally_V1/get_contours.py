import cv2
import numpy as np
from PIL import Image
import get_contours
import filter_contours
import cvt_to
import fill_contours
import draw_contour_outlines
import datetime

def approx():
    I = cv2.imread(image_name)
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    contours, heirarchy = cv2.findContours(I_gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_TC89_KCOS)

    return list(contours), heirarchy
    
def main(image_name):

    I = cv2.imread(image_name)
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    contours, heirarchy = cv2.findContours(I_gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    return list(contours), heirarchy

def external(image_name):

    I = cv2.imread(image_name)
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    contours, heirarchy = cv2.findContours(I_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return list(contours), heirarchy

def threshold(image_name, x):
    
    I = cv2.imread(image_name)
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(I_gray,x,255,0)
    contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    return list(contours), heirarchy

def eroded(ofn, MA, mia, perm, sfn, fill, dusted, l, m):
    I = Image.open('blank.tif')
    W, H = I.size
    I.save(sfn)

    contours = []
    if dusted == True:
        c, h = get_contours.main(ofn)
        c, h, a = filter_contours.size_only(c, h, W*H*2, 50)
        fill_contours.main(ofn, c, ofn, (255,255,255))
    
    c = fill        
    for i in range (l, m, -1):
        if len(fill) > 0:
            fill_contours.main(ofn, c, ofn, (0,0,0))
            
        cvt_to.eroded(ofn,(3,3), i, '')
        c, h = get_contours.main('eroded_' + ofn)
        c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
        c, h = filter_contours.smallest_circle(c, h, 0.2)
        remove_c = []
        I = Image.open('eroded_' + ofn)
        for k in c:
            M = cv2.moments(k)
            centroid = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))
            p = I.getpixel(centroid)
            if p == 0:
                remove_c.append(k)                                                                                       
        fill_contours.main('blank.tif', c, '4.tif', (255,255,255))
        fill_contours.main('4.tif', remove_c, '4.tif', (0,0,0))
        cvt_to.fat_separate('4.tif', i, MA, mia, perm)
        c, h = get_contours.main('fs_4.tif')
        contours += c
        fill_contours.main(sfn, c, sfn, (255,255,255))

    return contours

def thresh_square(ILam, sfn, MA, mia, perm, BG, fill,  dusted):
    c = []
    contours = []
    contours2 = []
    I = Image.open('blank.tif')
    W, H = I.size
    I = cv2.imread('blank.tif')
    cv2.imwrite('2.tif', I)

    
    for l in range(101,1001,200):
        for i in range(-4,5):
            I = cv2.adaptiveThreshold(ILam,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, l, i)
            cv2.imwrite('1.tif', I)
            cvt_to.closed_opened('1.tif', '1.tif', (3,3))
            fill_contours.main('1.tif', BG, '1.tif', (0,0,0))
            I = cv2.adaptiveThreshold(ILam,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, l, i)
            cv2.imwrite('1.1.tif', I)
            if len(fill) > 0:
                fill_contours.main('1.tif', fill, '1.tif', (255,255,255))

            if dusted == True:
                c, h = get_contours.main('1.tif')
                c, h, a = filter_contours.size_only(c, h, W*H*2, 50)
                fill_contours.main('1.tif', c, '1.tif', (255,255,255))
                                                   
            c, h = get_contours.main('1.tif')
            c, h, a = filter_contours.size_shape(c, h, MA, mia, perm) 
            c, h = filter_contours.smallest_circle(c, h, 0.2)
            
            if len(c) > 0:
                remove_c = []
                I = Image.open('1.tif')
                I1 = Image.open('1.1.tif')
                for k in c:
                    M = cv2.moments(k)
                    centroid = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))
                    p = I.getpixel(centroid)
                    p1 = I1.getpixel(centroid)
                    
                    if p == 0 or p1 > 0:
                        remove_c.append(k)

                fill_contours.main('blank.tif', c, '4.tif', (255,255,255))
                fill_contours.main('4.tif', remove_c, '4.tif', (0,0,0))
                c, h = get_contours.main('4.tif')                
                contours += c
                fill_contours.main('2.tif', c, '2.tif', (255,255,255))

    c, h = get_contours.main('2.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('blank.tif', c, '4.tif', (255,255,255)) 
    fill_contours.main('2.tif', c, '5.tif', (0,0,0))
    draw_contour_outlines.black('5.tif', contours, '6.tif', 2, '')
    c, h = get_contours.main('6.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('blank.tif', c, '7.tif', (255,255,255))
    draw_contour_outlines.white('7.tif', c, '8.tif', 2)
    
    c, h = get_contours.main('8.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('7.tif', c, '9.tif', (255,255,255))
    I1 = cv2.imread('4.tif')
    I2 = cv2.imread('9.tif')
    I3 = I1 + I2
    cv2.imwrite('10.tif', I3)
    c, h = get_contours.main('10.tif')
    fill_contours.main('blank.tif', c, sfn, (255,255,255))
