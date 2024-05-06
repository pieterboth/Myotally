from PIL import Image
import os
import cv2
import math
import numpy as np
import get_contours
import filter_contours
import draw_contour_outlines
import fill_contours
import cvt_to
from PIL import ImageDraw
import datetime
import mfis
from scipy import stats as st

def main(folder, DAPI_channel, Lam_channel, mfi_channels, IQ, mia, MA, PMR):
    #PMR = pixels/µm^2
    
    start_time = str(datetime.datetime.now()).replace(':','-')
    print('Started: ', start_time)
    
    keep_files = []
    
    DAPI_channel = DAPI_channel.strip(' ')
    Lam_channel = Lam_channel.strip(' ')
    keep_files.append(DAPI_channel)
    keep_files.append(Lam_channel)
    
    
    a = mfi_channels.strip(' ')
    a = a.strip(',')
    a = a.split(',')
    mfi_channels = []
    for b in a:
        mfi_channels.append(b.strip(' '))
        
    while '' in mfi_channels:
        mfi_channels.remove('')

    start_DAPI = DAPI_channel
    start_Lam = Lam_channel
    start_mfi = mfi_channels
    perm = 2.9
    brights_SD = 2
    
    os.chdir(folder)
    os.makedirs('Results', exist_ok = True)
    os.chdir(folder+'/Results')
    os.makedirs('CSA_CSVs', exist_ok = True)
    os.makedirs('MFI_CSVs', exist_ok = True)
    os.chdir(folder)
    results = open(folder+'/Results/all_results_'+str(start_time)+'.txt', 'w')
    results.write(folder + '\n' + str(start_time))
    results.write('\nFiber Size Range (µm^2): ' + str(mia) + ' - ' + str(MA))
    results.write('\n' +'Image'.rjust(50) + '\t' + 'Number of Fibers'.rjust(20) + '\t' + 'Average CSA (µm^2)'.rjust(20))
    for i in mfi_channels:
        keep_files.append(i)
        results.write('\t' + (str(i) + ' Mean FI').rjust(20))
    results.write('\n')
    results.close()

    mia = mia*PMR
    MA = MA*PMR

    image_quality = 'low'
    if IQ == 2:
        image_quality = 'high'

    okf = []
    for i in keep_files:
        okf.append(i)

    for path, direcs, files in os.walk(folder):
        if path == folder:
            direcs.sort()
            for d in direcs:
                keep_files = []
                for i in okf:
                    keep_files.append(i)
                if d != '.DS_Store' and len(set(keep_files)&set(os.listdir(folder+'/'+d))) == len(set(keep_files)):
                    os.chdir(folder+'/'+d)
                    print(os.getcwd())
                    I = cv2.imread(DAPI_channel,-1)
                    depth = str(I.dtype)
                    a = I.flatten()
                    a.sort()
                    if depth == 'uint16':
                        
                        I1 = I*(65535/a[int(len(a)*(1-.0001))])
                        z = np.where(I>65535)
                        for x,y in enumerate(z[0]):
                            I1[z[0][x],z[1][x]] = 65535
                        I1 = np.uint16(I1)
                    else:
                        I1 = I*(255/a[int(len(a)*(1-.0001))])
                        z = np.where(I>65535)
                        for x,y in enumerate(z[0]):
                            I1[z[0][x],z[1][x]] = 255
                        I1 = np.uint8(I1)

                        
                    cv2.imwrite('bright_'+DAPI_channel,I1)
                    I_nuc = Image.open('bright_'+DAPI_channel)
                    W, H = I_nuc.size
                    I_nuc.close()
                    I_nuc = cv2.imread('bright_'+DAPI_channel, -1)

                    
                    L = []
                    for i in keep_files:
                        I = cv2.imread(i, -1)
                        depth = I.dtype
                        a = I.flatten()
                        a.sort()
                        if depth == 'uint16':
                            I1 = I*(65535/a[int(len(a)*(1-.0001))])
                            z = np.where(I>65535)
                            for x,y in enumerate(z[0]):
                                I1[z[0][x],z[1][x]] = 65535
                            I1 = np.uint16(I1)
                            
                        else:
                            I1 = I*(255/a[int(len(a)*(1-.0001))])
                            z = np.where(I>65535)
                            for x,y in enumerate(z[0]):
                                I1[z[0][x],z[1][x]] = 255
                            I1 = np.uint8(I1)
                            
                        cv2.imwrite('bright_'+i,I1)
                        I = cv2.imread('bright_'+i, -1)
                        I1 = cv2.addWeighted(I_nuc,0.5,I,0.5,0)
                        cv2.imwrite(str(i) + ' overlay.tif', I1)
                        L.append('bright_'+i)
                        
                    DAPI_channel = 'bright_'+DAPI_channel
                    Lam_channel = 'bright_'+Lam_channel
                        
                    I = Image.new('RGB', (W,H))
                    I.save('blank.tif')
                    I.save('fibers.tif')
                    I1 = cv2.imread(Lam_channel,0)
                    mode = int(st.mode(I1.flatten())[0][0])
                    z = np.where(I1 <= mode+2)
                    for x,y in enumerate(z[0]):
                        I1[z[0][x],z[1][x]] = mode
                        ILam = np.uint8(I1)
                    cv2.imwrite('ILam.tif', ILam)
                    ILam = cv2.imread('ILam.tif', -1)

                    I = cv2.imread('blank.tif')
                    _, I1 = cv2.threshold(I,255,255,cv2.THRESH_BINARY_INV)
                    cv2.imwrite('white.tif', I1)
                    cdic = {}
                    Is = []
                    
                    for i in range(-4,5):                                    
                        I = cv2.adaptiveThreshold(ILam,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 501, i)
                        cv2.imwrite('temp.tif', I)
                        cvt_to.closed_opened('temp.tif', 'temp.tif', (3,3))
                        c, h = get_contours.main('temp.tif')
                        c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
                        if len(c) not in list(cdic):
                            cdic[len(c)] = i
                    cs = list(cdic)
                    cs.sort()
                    Lam_thresh1 = cdic[cs[-1]]
                    Lam_thresh2 = cdic[cs[-2]]
                

                    I1 = cv2.imread('blank.tif')
                    for i in range(101, 2201, 200):
                        I = cv2.adaptiveThreshold(ILam,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, i, Lam_thresh1)
                        cv2.imwrite('temp.tif', I)
                        I = cv2.imread('temp.tif')
                        I1 = I1 + I
                        cv2.imwrite('AT_Lam1.tif', I1)
                    
                    I1 = cv2.imread('blank.tif')
                    for i in range(101, 2201, 200):
                        I = cv2.adaptiveThreshold(ILam,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, i, Lam_thresh2)
                        cv2.imwrite('temp.tif', I)
                        I = cv2.imread('temp.tif')
                        I1 = I1 + I                                   
                    cv2.imwrite('AT_Lam2.tif', I1)

                    I = Image.open('AT_Lam1.tif')
                    I.save('OGLam1.tif')
                    I = Image.open('AT_Lam2.tif')
                    I.save('OGLam2.tif')
                    I1 = cv2.imread('OGLam1.tif')
                    I2 = cv2.imread('OGLam2.tif')
                    I = I1 + I2
                    cv2.imwrite('OGLam3.tif', I)
                    I = Image.open('OGLam3.tif')
                    c = []
                    BG = []
                    if image_quality == 'low':
                        get_contours.thresh_square(ILam, 'fibers0.tif', MA, mia, perm, BG, fill = c, dusted = False) #dusted = false ->True 16-14-21
                        I = cv2.imread('fibers0.tif')
                        cv2.imwrite('fibers.tif', I)

                    fill_contours.main('OGLam1.tif', c, 'AT_Lam1.tif', (0,0,0))
                    fill_contours.main('OGLam2.tif', c, 'AT_Lam2.tif', (0,0,0))
                        
                    contours = get_contours.eroded('AT_Lam1.tif', MA, mia, perm, 'temp.tif', [], False, 5, -1)
                    fill_contours.fs('temp.tif', contours, MA, mia, perm, 'fibers1.tif')
                    contours = get_contours.eroded('AT_Lam2.tif', MA, mia, perm, 'temp.tif', [], False, 5, -1)
                    fill_contours.fs('temp.tif', contours, MA, mia, perm, 'fibers2.tif')

                    I = Image.open('AT_Lam1.tif')
                    I.save('AT_Lam1.1.tif')
                    I = Image.open('AT_Lam2.tif')
                    I.save('AT_Lam2.1.tif')

                    contours = get_contours.eroded('AT_Lam1.1.tif', MA, mia, perm, 'temp.tif', c, True, 5, -1)
                    fill_contours.fs('temp.tif', contours, MA, mia, perm, 'fibers3.tif')
                    contours = get_contours.eroded('AT_Lam2.1.tif', MA, mia, perm, 'temp.tif', c, True, 5, -1)
                    fill_contours.fs('temp.tif', contours, MA, mia, perm, 'fibers4.tif')
          
                    L = []
                    for i in range(1,5):
                        L.append('fibers'+str(i)+'.tif')
                    for i in L:
                        fill_contours.combine(i, 'fibers.tif', 'fibers.tif', MA, mia, perm)

                    c, h = get_contours.external('fibers.tif') 
                    fill_contours.main('fibers.tif', c, 'fibers.tif', (255,255,255))
                    cvt_to.dilated2('fibers.tif', 'temporary1.tif', (11,11), 8)
                    cvt_to.eroded2('temporary1.tif', 'temporary2.tif', (11,11), 8)
                    c, h = get_contours.main('temporary2.tif')
                    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
                    fill_contours.main('fibers.tif', c, 'fibers.tif', (0,0,0))
                    
                    I = Image.open('fibers.tif')
                    for x in range(W):
                        for y in range(H):
                            if x == 0 or y == 0  or x >= W-1 or y >= H-1:
                                I.putpixel((x,y), (255,255,255))
                    
                    I.save('prefibers.tif')
                    I = cv2.imread('fibers.tif', -1)
                    cv2.imwrite('first fibers.tif', I)
                    
                    c, h = get_contours.main('prefibers.tif')
                    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
                    c, h = filter_contours.smallest_circle(c, h, 0.2)
                    fill_contours.main('blank.tif', c, '1.tif', (255,255,255))

                    c, h = get_contours.external('1.tif')
                    fill_contours.main('1.tif', c, '1.tif', (255,255,255))
                    
                    c, h = get_contours.main('1.tif')
                    draw_contour_outlines.black('1.tif', c, '2.tif', 6, '')
                    c, h = get_contours.main('2.tif')
                    
                    c, h, a = filter_contours.size_only(c, h, MA, 2)
                    c = filter_contours.remove_brights_object(c,Lam_channel,[Lam_channel],False)
                    fill_contours.main('2.tif', c, '2.tif', (0,0,0))
                    c, h = get_contours.main('2.tif')
                    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
                    draw_contour_outlines.black('1.tif', c, '3.tif', 1, '')
                    c, h = get_contours.main('3.tif')
                    c, h = filter_contours.parents_only(c, h)
                    fill_contours.main('1.tif', c, '4.tif', (0,0,0)) 
                    c, h = get_contours.external('4.tif')
                    c, h, a = filter_contours.size_shape(c, h, MA, mia, perm)
                    c, h = filter_contours.smallest_circle(c, h, 0.2)
                    fill_contours.main('blank.tif', c, 'fibers.tif', (255,255,255))
                    
                    draw_contour_outlines.green(start_Lam+' overlay.tif', c, 'fiber outlines.tif', 1)
                    fill_contours.main(start_Lam+' overlay.tif', c, 'white fibers.tif', (255,255,255))
                    #keep_files.append('white fibers.tif')
                    contours, heirarchy = c, h
                    
                    I = cv2.imread(DAPI_channel,0)
                    I = cv2.adaptiveThreshold(I,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,301, -2)#was 31,-4 #301, -2 for grey
                    cv2.imwrite('AT_DAPI.tif', I)
                    DAPI_c, DAPI_h = get_contours.main('AT_DAPI.tif')
                    DAPI_c, DAPI_h, DAPI_a = filter_contours.size_only(DAPI_c, DAPI_h, W*W*W, 5)
                    
                    fill_contours.main('blank.tif', DAPI_c, 'AT_DAPI.tif', (255, 255, 255))
                    draw_contour_outlines.black('AT_DAPI.tif', contours, 'black_fibers_inward.tif', 1, thickness = 'proportional')#9 was 7
                    draw_contour_outlines.red('AT_DAPI.tif', contours, 'red_fibers_inward.tif', 1, thickness = 'proportional') #1->1.5 10-22-20
  
                    I1 = cv2.imread('fibers.tif')
                    I2 = cv2.imread('black_fibers_inward.tif')
                    I3 = I1 - I2
                    cv2.imwrite('fibers_minus_centralized_nuclei.tif', I3)
                    c, h = get_contours.main('fibers_minus_centralized_nuclei.tif')
                    filter_contours.children_only(c,h)
                    fill_contours.main('blank.tif', c, 'centralized_nuclei.tif', (255,255,255))
                    c, h = get_contours.main('fibers_minus_centralized_nuclei.tif')
                    c, h = filter_contours.parents_only(c, h)
                    fill_contours.main('blank.tif', c, 'regenerating_fibers.tif', (255,255,255))
                    c, h = get_contours.external('regenerating_fibers.tif')
                    fill_contours.main('regenerating_fibers.tif', c, 'regenerating_fibers.tif', (255,255,255))
                    draw_contour_outlines.green('centralized_nuclei.tif',c,'central_nucleated_fibers.tif', 1)
                    
                    contours, heirarchy = get_contours.external('regenerating_fibers.tif')
                    contours, heirarchy, areas = filter_contours.size_shape(contours, heirarchy, MA, mia, perm)
                    
                    draw_contour_outlines.white('fiber outlines.tif', contours,\
                                                'final_blank.tif', 1) 
                    #keep_files.append('final_blank.tif')
                    fill_contours.main(start_Lam + ' overlay.tif', contours, \
                                       'white regenerating fibers.tif', (255,255,255))
                    #keep_files.append('white regenerating fibers.tif')

                    fibers_i = mfis.object(contours, mfi_channels, False)
                    for f in fibers_i:
                        f.CNF = 1
                    
                    I1 = cv2.imread('fibers.tif')
                    I2 = cv2.imread('regenerating_fibers.tif')
                    I = I1-I2
                    cv2.imwrite('uninjured_fibers.tif', I)
                    u_contours, u_heirarchy = get_contours.external('uninjured_fibers.tif')

                    fibers_u = mfis.object(u_contours, mfi_channels, False)
                    for f in fibers_u:
                        f.CNF = 0

                    fibers = fibers_i + fibers_u
                    for n, f in enumerate(fibers):
                        f.number = n

                    I = Image.open('final_blank.tif')
                    write = ImageDraw.Draw(I)
                    CSAs = []
                    for f in fibers:
                        write.text((f.centroid), str(f.number), color = 'white', size = 15)
                        CSAs.append(f.area)
                    I.save('final.tif')
                    keep_files.append('final.tif')
                    del write

                    results = open(folder+'/Results/all_results_'+str(start_time)+'.txt', 'a')
                    results.write(str(d).rjust(50) + '\t' + str(len(fibers)).rjust(20) + '\t' + str(format(np.mean(CSAs)/PMR,'.1f')).rjust(20))

                    L = []
                    for i,b in enumerate(mfi_channels):
                        L.append([])
                        for f in fibers:
                            L[-1].append(f.mean_fis[i])
                        results.write('\t' + str(format(np.mean(L[-1]),'.1f')).rjust(20))
                    results.write('\n')
                    results.close()

                    current = open(folder+'/Results/'+str(d)+'_'+str(start_time)+'.txt', 'w')
                    current.write('\n' + 'Fiber Number'.rjust(20) + '\t' + 'CSA'.rjust(20) + '\t'+ 'CNF (y/n = 1/0)'.rjust(20))
                    for i in mfi_channels:
                        current.write('\t'+(str(i)+ ' MFI').rjust(20))
                    for f in fibers:
                        current.write('\n'+str(f.number).rjust(20)+'\t'+str(format(f.area/PMR,'.1f')).rjust(20)+'\t'+str(f.CNF).rjust(20))
                        for i,b in enumerate(mfi_channels):
                            current.write('\t'+str(f.mean_fis[i]).rjust(20))
                    current.close()

                    for i,b in enumerate(mfi_channels):
                        MFI_CSV = open(folder+'/Results/MFI_CSVs/'+str(d)+'_'+str(i)+' MFIs_'+str(start_time)+'.txt', 'w')
                        for f in fibers:
                            MFI_CSV.write(str(f.mean_fis[i]) + ', ')
                        MFI_CSV.close()

                    CSA_CSV = open(folder+'/Results/CSA_CSVs/'+str(d)+'_CSAs_'+str(start_time)+'.txt', 'w')
                    for f in fibers:
                        CSA_CSV.write(str(format(f.area/PMR, '.1f')) + ', ')
                    CSA_CSV.close()

                    DAPI_channel = start_DAPI
                    Lam_channel = start_Lam
                    mfi_channel = start_mfi
                    
                    x = os.getcwd()
                    for p, c, f in os.walk(os.getcwd()):
                        for this_f in f:
                            if this_f not in keep_files and os.path.exists(os.getcwd()+'/'+this_f):
                                os.remove(this_f)

    print('Finished: ', datetime.datetime.now())

                                    
                                
                            











    



    
    
    
    
    
    
    
    







