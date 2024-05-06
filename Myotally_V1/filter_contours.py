import cv2
import numpy as np
import math
import cvt_to
from PIL import Image
import fill_contours
import draw_contour_outlines
import get_contours
import filter_contours
import get_contours
import mfis


def remove_brights_object(c, i, channels, background_correction):

    cells = mfis.object(c, channels,background_correction)
    L = []
    for cell in cells:
        L.append(cell.mean_fis[channels.index(i)])

    av = np.mean(L)
    SD = np.std(L)

    remove_cells = []

    for cell in cells:
        if cell.mean_fis[channels.index(i)] >= av + SD*2 or cell.mean_fis[channels.index(i)] <= av - SD*2:
            remove_cells.append(cell)
            
    while len(remove_cells) > 0:
        for rc in remove_cells:
            cells.remove(rc)
            remove_cells.remove(rc)

    L = []
    for cell in cells:
        L.append(cell.contour)

    return L
                
def cvs(I, max_area, min_area, perimeter):
    c,h = get_contours.external(I)
    fill_contours.main('blank.tif', c, 'cvs1_'+I, (255,255,255))
    c,h = get_contours.main(I)
    c,h = filter_contours.remove_parents(c,h)
    fill_contours.main('cvs1_'+I, c, 'cvs2_'+I, (0,0,0))
    c,h = get_contours.main('cvs2_'+I)
    c,h = filter_contours.parents_only(c,h)
    draw_contour_outlines.black(I, c, 'cvs3_'+I, 1, 'dis')
    c,h = get_contours.main('cvs3_'+I)
    c,h,a = filter_contours.size_shape(c,h, max_area, min_area, perimeter)
    c,h = filter_contours.children_only(c,h)

    return c, h


def remove_parents(contours, heirarchy):
    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if heirarchy[0][count][2] != -1:
                heirarchy = np.delete(heirarchy, count, 1)
                del contours[count]
            else:
                count+=1                
    return contours, heirarchy

def parents_only(contours, heirarchy):
    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if heirarchy[0][count][2] == -1:
                heirarchy = np.delete(heirarchy, count, 1)
                del contours[count]
            else:
                count+=1                
    return contours, heirarchy

def remove_nonparents_without_parents(contours, heirarchy):
    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if heirarchy[0][count][2] == -1 and heirarchy[0][count][3] == -1 :
                heirarchy = np.delete(heirarchy, count, 1)
                del contours[count]
            else:
                count+=1                

    return contours, heirarchy

def remove_children(contours, heirarchy):
    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if heirarchy[0][count][3] != -1:
                heirarchy = np.delete(heirarchy, count, 1)
                del contours[count]
            else:
                count+=1

    return contours, heirarchy

def children_only(c,h):
    count = 0
    for k in range(len(c)):
        if count <= len(c)-1:
            if h[0][count][3] == -1:
                h = np.delete(h, count, 1)
                del c[count]
            else:
                count+=1
    return c, h

def no_parents_of_one(c,h):

    L1 = [] 
    L2 = [] 
    L3 = [] 
    
    D = {}

    for k in range(len(c)):
        parent = h[0][k][3]
        if parent != -1:
            L1.append(parent)
            if parent not in L2:
                L2.append(parent) 
    for a in L2: 
        D[a] = L1.count(a) 
    for d in list(D):
        if D[d] > 1:
            L3.append(c[d])

    return L3 
                        

def remove_orphans(contours, heirarchy):
    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if heirarchy[0][count][3] == -1:
                heirarchy = np.delete(heirarchy, count, 1)
                del contours[count]
            else:
                count+=1

    return contours, heirarchy

def remove_parent_orphans(contours, heirarchy):
    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if heirarchy[0][count][2] != -1 and heirarchy[0][count][3] == -1:
                heirarchy = np.delete(heirarchy, count, 1)
                del contours[count]
            else:
                count+=1

    return contours, heirarchy

    



def size_shape(contours, heirarchy, max_area, min_area, perimeter):

    areas = np.zeros((1,len(contours)))
    perimeters = np.zeros((1,len(contours)))
    over_4000 = np.arange(0) 

    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if cv2.contourArea(contours[count]) >= min_area and cv2.contourArea(contours[count]) <= max_area and cv2.arcLength(contours[count],True) <  perimeter*math.sqrt(math.pi*cv2.contourArea(contours[count])):
                areas[0,count] = cv2.contourArea(contours[count])
                count+=1
            elif cv2.contourArea(contours[count]) > max_area:
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)
            elif cv2.contourArea(contours[count]) < min_area:
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)
            elif cv2.arcLength(contours[count],True) >=  perimeter*math.sqrt(math.pi*cv2.contourArea(contours[count])):
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)         
            else:
                count+=1

    return contours, heirarchy, areas

def size_only(contours, heirarchy, max_area, min_area):

    areas = np.zeros((1,len(contours)))
    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if cv2.contourArea(contours[count]) >= min_area and cv2.contourArea(contours[count]) <= max_area:
                areas[0,count] = cv2.contourArea(contours[count])
                count+=1
            elif cv2.contourArea(contours[count]) > max_area:
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)
            elif cv2.contourArea(contours[count]) < min_area:
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)        
            else:
                count+=1

    return contours, heirarchy, areas

def dynamic_ss(contours, heirarchy, max_area, min_area, perimeter):
    areas = np.zeros((1,len(contours)))
    perimeters = np.zeros((1,len(contours)))

    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            if cv2.contourArea(contours[count]) >= min_area and cv2.contourArea(contours[count]) <= max_area and cv2.arcLength(contours[count],True) <  perimeter*math.sqrt(math.pi*cv2.contourArea(contours[count])):
                keep_going = True
                for i in range(8):
                    if i == list(range(8))[-1]:
                        areas[0,count] = cv2.contourArea(contours[count])
                        count+=1
                        keep_going = False
                    
                    if keep_going == True:
                        if cv2.contourArea(contours[count]) < min_area+i*50 and cv2.arcLength(contours[count],True) >  (perimeter-1+(i*.14))*math.sqrt(math.pi*cv2.contourArea(contours[count])):
                            del contours[count]
                            heirarchy = np.delete(heirarchy, count, 1)
                            keep_going = False
                        
                    
            elif cv2.contourArea(contours[count]) > max_area:
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)
            elif cv2.contourArea(contours[count]) < min_area:
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)
            elif cv2.arcLength(contours[count],True) >=  perimeter*math.sqrt(math.pi*cv2.contourArea(contours[count])):
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)         
            else:
                count+=1   

    return contours, heirarchy, areas

def pix_to_micron(contours, areas):

    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            areas[0,count] = np.round(math.sqrt(areas[0,count]),2)
            count+=1
    return areas

def get_big(contours):

    areas = np.zeros((1,len(contours)))

    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            areas[0,count] = cv2.contourArea(contours[count])
            count+=1
    return areas

def smallest_circle(contours, heirarchy,x):

    count = 0
    for k in range(len(contours)):
        if count <= len(contours)-1:
            _, radius = cv2.minEnclosingCircle(contours[count])
            area = cv2.contourArea(contours[count])
            if area < x*(math.pi)*(radius**2):
                del contours[count]
                heirarchy = np.delete(heirarchy, count, 1)
            
            else:
                count+=1
    return contours, heirarchy

def remove_perimeter(w, h, contours, delete_from):
    import fill_contours
    D = {}

    count = 0
    for contour in contours:
        D[count] = []
        for c in contour:
            D[count].append((c[0][0],c[0][1]))
        count += 1
        
    delete_contours = []
    for contour in D:
        for (x,y) in D[contour]:
            if x == 2 or x == w-2:
                if contour not in delete_contours:
                    delete_contours.append(contour)

            elif y == 2 or y == h-2:
                if contour not in delete_contours:
                    delete_contours.append(contour)
    
    c2del = []
    for dc in delete_contours:
        c2del.append(contours[dc])

    return contours, c2del



