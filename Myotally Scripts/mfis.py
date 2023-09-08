from PIL import Image
import numpy as np
import cv2
import fill_contours

def object(contours, channels, background_correction):

    class cell():
        pass
    
    cells = []
    if background_correction == True:
        background = []
        for i in channels:
            fill_contours.asis(i, contours, 'mfistemp.tif', (65535,65535,65535))
            I = cv2.imread('mfistemp.tif',-1)
            I = I[I!=0]
            background.append(float(format(np.mean(I[I<65535]), '.2f')))

    for b, c in enumerate(contours):
        this_c = cell()
        cells.append(this_c)
        this_c.number = b
        this_c.contour = c
        this_c.area = cv2.contourArea(c)
        this_c.perimeter = cv2.arcLength(c,True)
        M = cv2.moments(c)
        this_c.centroid = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
        this_c.mean_fis = []
        this_c.total_fis = []
        fill_contours.main('blank.tif', [contours[b]], 'mfistemp1.tif', (255,255,255))
        I = cv2.imread('mfistemp1.tif',0)
        z = np.where(I == 255)
        
        for a, i in enumerate(channels):
            
            I = cv2.imread(i,-1)
            L = []
                
            for x,y in enumerate(z[0]):
                L.append(I[z[0][x],z[1][x]])

            if background_correction == True:
                this_c.mean_fis.append(float(format(np.mean(L)-background[a], '.1f')))
                this_c.total_fis.append(float(format(np.sum(L)-(background[a]*len(L)), '.1f')))

            elif background_correction == False:
                this_c.mean_fis.append(float(format(np.mean(L), '.1f')))
                this_c.total_fis.append(float(format(np.sum(L), '.1f')))

    return cells
        



        
