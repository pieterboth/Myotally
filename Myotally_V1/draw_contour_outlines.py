import cv2

def green(open_filename, contours, save_filename, n):

    I = cv2.imread(open_filename)          
    cv2.drawContours(I, contours, -1, (0,255,0), n)
    cv2.imwrite(save_filename,I)

def blue(open_filename, contours, save_filename, x):
    
    I = cv2.imread(open_filename)          
    cv2.drawContours(I, contours, -1, (255,0,0), x)
    cv2.imwrite(save_filename,I)

def red(open_filename, contours, save_filename, n, thickness):

    I = cv2.imread(open_filename)

    if thickness == 'proportional':
        count = 0
        for k in range(len(contours)):
            if count <= len(contours)-1:
                this_area = cv2.contourArea(contours[count])
                cv2.drawContours(I, contours, count, (0,0,255), 2+(n*int(round(this_area/200))))
            count += 1
                

    elif thickness != 'proportional':
            I = cv2.imread(open_filename)          
            cv2.drawContours(I, contours, -1, (0,0,255), n)
            cv2.imwrite(save_filename,I)
            
    cv2.imwrite(save_filename,I)

def white(open_filename, contours, save_filename, n):
    I = cv2.imread(open_filename)          
    cv2.drawContours(I, contours, -1, (255,255,255), n)
    cv2.imwrite(save_filename,I)

def black(open_filename, contours, save_filename, n, thickness):


    I = cv2.imread(open_filename)

    if thickness == 'proportional':
        count = 0
        for k in range(len(contours)):
            if count <= len(contours)-1:
                this_area = cv2.contourArea(contours[count])
                cv2.drawContours(I, contours, count, (0,0,0), 2+(n*int(round(this_area/200)))) #2,200
            count += 1
                
    elif thickness != 'proportional':
        I = cv2.imread(open_filename)          
        cv2.drawContours(I, contours, -1, (0,0,0), n)
        cv2.imwrite(save_filename,I)
            
    cv2.imwrite(save_filename,I)

