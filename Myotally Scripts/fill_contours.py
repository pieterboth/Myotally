import cv2
import draw_contour_outlines
import filter_contours
import fill_contours
import get_contours

#draws passed contours onto a passed image_name and saves under passed image_name
def main(open_filename, contours, save_filename, color):

    I = cv2.imread(open_filename)          
    cv2.drawContours(I, contours, -1, color, -1)
    cv2.imwrite(save_filename,I)

def asis(open_filename, contours, save_filename, color):

    I = cv2.imread(open_filename,-1)          
    cv2.drawContours(I, contours, -1, color, -1)
    cv2.imwrite(save_filename,I)

def heat_map(open_filename, contours, save_filename):

    I = cv2.imread(open_filename)

    for n, c in enumerate(list(contours)):       
        cv2.drawContours(I, contours, n, (0+40*(2500/cv2.contourArea(contours[n])), 0, 255-40*(2500/cv2.contourArea(contours[n]))) , -1)
    cv2.imwrite(save_filename,I)

def fs(ofn, contours, MA, mia, perm, sfn):
    
    c, h = get_contours.main(ofn)
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('blank.tif', c, '4.tif', (255,255,255))
    fill_contours.main(ofn, c, '5.5.tif', (0,0,0))
    draw_contour_outlines.black('5.5.tif', contours, '6.tif', 2, '')
    c, h = get_contours.main('6.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    C = c
    fill_contours.main('blank.tif', C, '7.tif', (255,255,255))
    fill_contours.main('blank.tif', C, '9.tif', (255,255,255))

    for i in range(6,1,-1):
        
        draw_contour_outlines.white('7.tif', C, '8.tif', i)
        c, h = get_contours.main('8.tif')
        fill_contours.main('4.tif', c, '1.tif', (255,255,255))
        c, h = get_contours.main('1.tif')
        c, h, a = filter_contours.size_shape(c, h, MA, mia+35*i/2, perm*0.95) #35 is the perimeter of a 100µm fiber
        fill_contours.main('blank.tif', c, '2.tif', (255,255,255))
        c, h = get_contours.main('4.tif')
        fill_contours.main('2.tif', c, '3.tif', (0,0,0))
        c, h = get_contours.main('3.tif')
        fill_contours.main('9.tif', c, '9.tif', (255,255,255))

    c, h = get_contours.main('7.tif')
    fill_contours.main('4.tif', c, '1.tif', (255,255,255))
    c, h = get_contours.main('1.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm*0.95) 
    fill_contours.main('blank.tif', c, '2.tif', (255,255,255))
    c, h = get_contours.main('4.tif')
    fill_contours.main('2.tif', c, '3.tif', (0,0,0))
    c, h = get_contours.main('3.tif')
    fill_contours.main('9.tif', c, '9.tif', (255,255,255))
        
    I1 = cv2.imread('4.tif')
    I2 = cv2.imread('9.tif')
    I3 = I1 + I2
    cv2.imwrite(sfn, I3)



def combine(ofn1, ofn2, sfn, MA, mia, perm):

    c1, h1 = get_contours.main(ofn1)
    fill_contours.main(ofn2, c1, '2.tif', (255,255,255))
    c, h = get_contours.main('2.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('blank.tif', c, '3.tif', (255,255,255)) 
    fill_contours.main('2.tif', c, '4.tif', (0,0,0))
    draw_contour_outlines.black('4.tif', c1, '5.tif', 1, '')
    c, h = get_contours.main('5.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia-35, perm)
    fill_contours.main('3.tif', c, '6.tif', (255,255,255))
    fill_contours.main('5.tif', c, '7.tif', (0,0,0))
    draw_contour_outlines.black('7.tif', c1, '8.tif', 2, '')
    c, h = get_contours.main('8.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('6.tif', c, '9.0.tif', (255,255,255))
    C = c
    c, h = get_contours.main('9.0.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('blank.tif', c, '9.05.tif', (255,255,255)) 
    
    draw_contour_outlines.white('9.05.tif', C, '9.1.tif', 2)
    c, h = get_contours.main('9.1.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('9.05.tif', c, '9.15.tif', (255,255,255))

    draw_contour_outlines.white('9.05.tif', C, '9.2.tif', 3)
    c, h = get_contours.main('9.2.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)

    fill_contours.main('9.15.tif', c, '9.25.tif', (255,255,255))
    c, h = get_contours.main('9.25.tif')
    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
    fill_contours.main('blank.tif', c, sfn, (255,255,255))


  



