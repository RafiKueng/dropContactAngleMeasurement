# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 15:17:16 2012

@author: rafik
"""

import helper as h

import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize 
import cv2
import random as rnd
#import time


class wrkEdgeFit(h.AbstractPlugin):

    def __init__(self):
        
        inp0 = h.createDataDescriptor(
            name="Frame",
            describtion="The unprocceded frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.img_Gray)
            
        self.inputinfo = [inp0]
        
        
        
        out0 = h.createDataDescriptor(
            name="Contact angle",
            describtion="The procceded frame, with applied filters",
            datatype=h.Float)        
            
        self.outputinfo = [out0]
    
    def config(self):
        pass
    
    def __call__(self, data):

        #gray = cv2.cvtColor(data[self.inp_ch[0]], cv2.COLOR_BGR2GRAY) # convert to grayscale
        gray = data[self.inp_ch[0]]

        edges = np.zeros(np.shape(gray), dtype=np.uint8)
        thres = np.zeros(np.shape(gray), dtype=np.uint8)
        
        #edges = cv2.cvtColor(data[self.inp_ch[0]], cv2.COLOR_BGR2GRAY)
        cont = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cont2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cont3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        lineimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

#    /---- get more contrast ----
        #gray = np.uint8(np.clip(np.uint32(gray) * 1.5, 0, 255))
        th = histogram(gray)[1]        
        #print th
        thres = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)[1]
#    \------end contrast



#    /---- canny edge filtering ----
        low_threshold = 50
        edges = cv2.Canny(gray,low_threshold,low_threshold*7, edges, 3, L2gradient=True) # low_threshold*3 for high_treshold is recommended by canny

        mix1 = cv2.add(gray, edges) #construct red channel
        mix2 = cv2.subtract(gray, edges) # constuct blue, green channel
        color = cv2.merge([mix2, mix2, mix1])
#    \------finished canny
        
        
        
#    /---- getting contours ----
        contours, hir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i, c in enumerate(contours):
            
            linecolor  = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
            cv2.drawContours(cont, contours, i, linecolor, 3)
#    \------finished with contours
        
        #print np.shape(contours)
        contours.sort(key=len, reverse=True)
        #print contours
#        for i, c in enumerate(contours):
#            print i, len(c), np.shape(c), type(c)
#            print i, len(c[0]), np.shape(c[0]), type(c[0])
#            print i, len(c[0][0]), np.shape(c[0][0]), type(c[0][0])
            #print c
#        longestcontours = contours[0:2] #get the 2 longest contours
#        for i, c in enumerate(longestcontours):
#            print i, len(c)
        
        """
#    /--------get the pipette using regular hough transform
        lines = cv2.HoughLines(edges, 1, np.pi/2., 50)[0]
        print lines
        print "min:", min(lines, key=lambda _: _[0]), "max:", max(lines, key=lambda _: _[0])
        
        #draw the lines        
        for i, l in enumerate(lines):
            print i, l
            (rho, theta) = l
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho 
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(lineimg, pt1, pt2, (255, 0, 0), 1, 8)
#    \--------end getting the pipette
"""
# TODO: compare speed between the regular and the probabilistic hough transform

#    /--------get the pipette using probabalistic hough transform
        lines = cv2.HoughLinesP(edges, 50, np.pi, threshold=30, minLineLength=30, maxLineGap=20)[0]
        #print lines
        #print "min:", min(lines, key=lambda _: _[0]), "max:", max(lines, key=lambda _: _[0])
        
        pipette_x_min = min(lines, key=lambda _: _[0])[0] - 5 #substract 5 pix for safty
        pipette_x_max = max(lines, key=lambda _: _[0])[0] + 5 #add saftey margin
        pic_mid = (pipette_x_min+pipette_x_max)//2
        
        if len(lines)>4:
            print " !! Attention: pipette detection encountered error"
        #draw the lines        
        for i, l in enumerate(lines):
            #print i, l
            x0, y0, x1, y1 = l
            cv2.line(lineimg, (x0, y0), (x1, y1), (0, 0, 255), 2, 8)
#    \--------end getting the pipette        
        

#    /------- distribute the found countour pixels to 2 sets of interessting points, left and right side

        set_l = []
        set_r = [] 
        for contour in contours:
            for points in contour:
                for point in points:
                    #print np.shape(point), len(point), type(point)
                    if point[0]<pipette_x_min:
                        set_l.append(np.array([point]))
                    elif point[0]>pipette_x_max:
                        set_r.append(np.array([point]))
        
        set_l.sort(key=lambda _: _[0][1])
        set_r.sort(key=lambda _: _[0][1])
        sets = np.array([np.array(set_l), np.array(set_r)])
        #set_r=np.array(set_r)

#        print "set l"
#        print set_r
#        print len(set_l), np.shape(set_l), type(set_l)
#        print len(set_l[0]), np.shape(set_l[0]), type(set_l[0])
#        print len(set_l[0][0]), np.shape(set_l[0][0]), type(set_l[0][0])
#        print set_l
        cv2.drawContours(cont2, sets, 0, (0,0,255), 0)
        cv2.drawContours(cont2, sets, 1, (0,255,0), 0)

#    \--------end distribute points 

#    /------- get the mirror plane by taking the furthest pixels

#        set_l_xmin = min(set_l, key=lambda _: _[0][0])
#        set_r_xmax = max(set_l, key=lambda _: _[0][0])
        
#        max_val = 0
#        max_indices = []
#        max_y = []
#        for i, val in enumerate(set_r):
#            if val[0][0] < max_val: continue
#            if val[0][0] == max_val:
#                max_indices.append(i)
#                max_y.append(val[0][1])
#            else:
#                max_val = val[0][0]
#                max_indices = [i]   
#                max_y = [val[0][1]]
#                
#        print max_val, max_indices, max_y
        
        
        
        max_x = 0
        max_indices = []
        y_at_max_x = []
        for i, val in enumerate(set_r):
            if val[0][0] < max_x: continue
            if val[0][0] == max_x:
                max_indices.append(i)
                y_at_max_x.append(val[0][1])
            else:
                max_x = val[0][0]
                max_indices = [i] 
                y_at_max_x = [val[0][1]]
                
        #y_at_max_x_mean = np.int(sum(y_at_max_x)/len(y_at_max_x))
        
        #print max_x, y_at_max_x, y_at_max_x_mean
        #print max_indices


        min_x = 100000
        min_indices = []
        y_at_min_x = []
        for i, val in enumerate(set_l):
            if val[0][0] > min_x: continue
            if val[0][0] == min_x:
                min_indices.append(i)
                y_at_min_x.append(val[0][1])
            else:
                min_x = val[0][0]
                min_indices = [i] 
                y_at_min_x = [val[0][1]]
                
        #y_at_min_x_mean = np.int(sum(y_at_min_x)/len(y_at_min_x))

        #print min_x, y_at_min_x, y_at_min_x_mean
        #print min_indices

        #check if this point is a corner (then its index isnt the first one)
        #otherwise it isn't reliable
        if len(min_indices) < 1 and len(max_indices) < 1:       
            print "!! critical error in baseline finding..."
        elif len(min_indices) == 1 and min_indices[0] == 0 and len(max_indices) == 1 and max_indices[0] == 0:
            print "!! error: no baseline found at all, using previous"
        elif len(min_indices) == 1 and min_indices[0] == 0 and max_indices[0] > 0:
            baseline_pos = np.int(sum(y_at_max_x)/len(y_at_max_x))
        elif len(max_indices) == 1 and max_indices[0] == 0 and min_indices[0] > 0:
            baseline_pos = np.int(sum(y_at_min_x)/len(y_at_min_x))
        else:
            baseline_pos = np.int((sum(y_at_max_x)+sum(y_at_min_x))/(len(y_at_max_x)+len(y_at_min_x)))


        cv2.line(cont3, (1, baseline_pos), (1279, baseline_pos), (0,255,255), 1)


#    \--------end mirror plane 


#    /------- get the mirror plane by approximating a poly at the edge

#        cords_x = []
#        cords_y = []
#        #print set_l
#        set_l_bound = set_l[0][0][0]
#        #print set_l_bound
#        #print set_l[0][0]
#        selset_l = filter(lambda _: _[0][0]<=set_l_bound,set_l)
#        #print selset_l
#        if len(selset_l) >0:
#            set_l_xmin = min(selset_l, key=lambda _: _[0][0])
##            for i in selset_l:
##                cords_x.append(i[0][1])
##                cords_y.append(i[0][0])                
#        
#        set_r_bound = set_r[0][0][0]
#        selset_r = filter(lambda _: _[0][0]>=set_r_bound,set_r)
#        if len(selset_r) >0:
#            set_r_xmax = max(selset_r, key=lambda _: _[0][0])
#            for i in selset_r:
#                print i[0][0], i[0][1]
#                cords_x.append(i[0][1])
#                cords_y.append(i[0][0])       
#                
#                
#        cv2.drawContours(cont3, np.array([np.array(selset_l)]), 0, (0,0,255), 0)
#        cv2.drawContours(cont3, np.array([np.array(selset_r)]), 0, (0,255,0), 0)
#
#        #print selset_r
#
#        #fit the curves
#        
#        fitfunc = lambda p, x: np.abs(p[0]*(x - p[1])) + p[2] # Target function
#        errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
#        beta0 = [0.1, 1100., 380.] # Initial guess for the parameters
#        
#        res = optimize.leastsq(errfunc, beta0[:], args=(np.array(cords_x), np.array(cords_y)))   
#        print res
        
#    \--------end mirror plane 
        
        
#    /------- fitting a poly to the contour
        def flip(x):
            if x < baseline_pos:
                return 2*baseline_pos - x
            else:
                return x

        angle = [0.0,0.0]
        for i in [0,1]:
            if len(sets[i]) != 0:
                x = sets[i][:,0,0]
                y = [flip(y) for y in sets[i][:,0,1]]
                z = np.polyfit(x, y, 13)
                #print z
                poly = np.poly1d(z)
                z2 = z.copy()
                z2[-1] -= baseline_pos          
                #print z2
                shift = np.poly1d(z2)
                roots = np.roots(shift)
                
                print roots

                if i==0: #left side
                    x_max = max(np.real(x))
                    roots = filter(lambda _x: np.isreal(_x) and _x>0 and _x<x_max, roots)
                    root = np.int(np.real(max(roots)))
                else: #right side
                    x_min = min(np.real(x))
                    roots = filter(lambda _x: np.isreal(_x) and _x>x_min and _x<1280, roots)
                    root = np.int(np.real(min(roots)))
                
                deriv = poly.deriv()
                slope = deriv(root)
                angle[i] = abs(np.arctan(slope))*180/np.pi
                fitline = np.poly1d([slope, poly(root)-slope*root])
                
                print fitline
                print roots
                print 'root:', root, 'slope:', slope, 'angle:', angle[i]
                
                xp = range(1,1279)
                yp = np.int32(np.clip(poly(xp),0,1023))
                pnts = np.array([np.column_stack((xp, yp))])

                plt.plot(x,y,'.', xp, poly(xp),'-', xp, shift(xp),'b--', xp, fitline(xp), 'r-')
                plt.ylim(0,1024)
                plt.show()
                
                cv2.polylines(cont3, pnts, False, (255,255*i,0), 1)
                
                dx = 200
                cv2.line(cont3, (root-dx, int(fitline(root-dx))), (root+dx, int(fitline(root+dx))), (0,0,255), 1)
        

#    \--------end fit

        
        
        #return [color] #return pictre with colored boundaries from canny edge detection 
        #return [cont] #return the pic with found contours colored
        #return [lineimg] # return the pictre with the pipette markers from hough line detetction
        #return [cont2] # the connected contours, split in left and right side of pipette
        return [cont3]


def histogram(picture, channels=[0]):
    # get and display histogram
    hist = cv2.calcHist( [picture], channels, None, [256], [0, 255] )
    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX);
    #print hist
    bin_count = hist.shape[0]
    bin_w = 2
    bin_max_h = 200
    img = np.ones((int(bin_max_h*1.1), bin_count*bin_w, 3), np.uint8)*[70,255,255]*255 #last list is background color

    #print hist
    for i in xrange(bin_count):
        val = hist[i]
        if val==1: hist_max = i #find the size and the pos of the max
        h = int(val*bin_max_h)
        #print h
        cv2.rectangle(img, (i*bin_w+2, int(bin_max_h*1.1)), ((i+1)*bin_w-2, int(bin_max_h*1.1)-h), [int(255*255.0*i/bin_count)]*3, -1)
    #img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    cv2.imshow('hist', img)       

    for i in xrange(hist_max, bin_count):
        if hist[i]<0.2:
            thres = i
            break
    #print hist_max, thres
    return hist_max, thres



def maxelements(seq): # @John Machin
    ''' Return list of position(s) of largest element
    source: http://stackoverflow.com/questions/3989016/how-to-find-positions-of-the-list-maximum'''
    if not seq: return []
    max_val = seq[0] if seq[0] >= seq[-1] else seq[-1]
    max_indices = []
    for i, val in enumerate(seq):
        if val < max_val: continue
        if val == max_val:
            max_indices.append(i)
        else:
            max_val = val
            max_indices = [i]
    return max_val, max_indices



if __name__ == '__main__':
    #getData()
    pass


'''

some old stuff...




    def overlayEdges(self, img, edges):
        for row in range(len(img)):
#            if max(edges[row]) == 0:
#                continue
            
            for col in range(len(img[row])):
                #newimg[row].append()
                #print edges[row][col]
                if edges[row][col] == 255:
                    img[row][col] = [0, 0, 255] #set pixelcolor to red (bgr)
                else:
                    img[row][col] = img[row][col] // 3 +170
        return img











        #print edges
        #print edges[1][1]      
        #print data[1][1][1]
        

        color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        mixed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
  
        #print x,y,d
        edge = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        x,y,d = shape(color) 
        mixx = zeros([x,y,d])
                
        
#        color = self.overlayEdges(color, edges)

        

        #cv2.mixChannels([color, edges], [mixed], [0,0 , 1,1 , 3,2 , 2,2])  
#        cv2.mixChannels(edge, rededges, [0,2])  
        
#        mixed = cv2.addWeighted(color, 1.0, edge, 1.0, 0.0 )
        
        #mixed = cv2.addWeighted(color, 0.50, edge, 1.0, 0.0 )
        #cv2.mixChannels(mixed, color, [2,2])  
        
'''