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


def median(y):
    z = len(y)
    if not z%2:
        return (y[(z/2)-1] + y[z/2]) / 2.
    return y[z/2]


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
        
        self.nTrained = 0;
    
    def config(self):
        
        
        self.contrast_adj = 1.1 #simple factor for getting more contrast in picture

        self.canny_low_threshold = 50
        self.canny_hi_threshold = 50*7
        
        self.hough_threshold=30
        self.hough_minLineLength=50
        self.hough_maxLineGap=20



        self.baseline = 377


    def train(self, imgs):
        
        print "training with", len(imgs), "images"
        
        pipette_x_min=[]
        pipette_x_max=[]
        baseline_pos=[]
        
        
        for img in imgs:
            gray = np.uint8(np.clip(np.uint32(img) * 1.1, 0, 255))
            edges = np.zeros(np.shape(gray), dtype=np.uint8)
            edges = cv2.Canny(gray,self.canny_low_threshold,self.canny_hi_threshold, edges, 3, L2gradient=True)
            contours, hir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            lines = cv2.HoughLinesP(edges,
                                    50,
                                    np.pi,
                                    threshold=self.hough_threshold,
                                    minLineLength=self.hough_minLineLength,                                
                                    maxLineGap=self.hough_maxLineGap
                                    )[0]
            #print lines
            #print "min:", min(lines, key=lambda _: _[0]), "max:", max(lines, key=lambda _: _[0])
            
            pipette_x_min.append(min(lines, key=lambda _: _[0])[0])
            pipette_x_max.append(max(lines, key=lambda _: _[0])[0])
        
        
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
#    \--------end distribute points 

#    /------- get the mirror plane by taking the furthest pixels
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

            #check if this point is a corner (then its index isnt the first one)
            #otherwise it isn't reliable
            # TODO: make this more efficient...
            
            if len(min_indices) < 1 and len(max_indices) < 1:
                # didn't found an extremum on either side
                pass
    
                
            elif len(min_indices) > 0 and min_indices[0] <= 5 and len(max_indices) > 0 and max_indices[0] <= 5:
                # if extremal ponts are found, but they are from the first few points
                # of the contour, then they are not really edges:
                # use the previous baseline
                pass
            
            elif len(min_indices) > 0 and min_indices[0] <= 5 and len(max_indices) > 0 and max_indices[0] > 5:
                # left side (min) is not reliable, only use right side
                print '! use only right side for baseline'
                baseline_pos.append(np.int(sum(y_at_max_x)/len(y_at_max_x)))
    
            elif len(max_indices) > 0 and max_indices[0] <= 5 and len(min_indices) > 0 and min_indices[0] > 5:
                # right side (max) is not reliable, only use left side
                print '! use only left side for baseline'
                baseline_pos.append(np.int(sum(y_at_min_x)/len(y_at_min_x)))
    
            else:
                baseline_pos.append(np.int((sum(y_at_max_x)+sum(y_at_min_x))/(len(y_at_max_x)+len(y_at_min_x))))
    
            
            
            
        self.pipette_x_min=median(pipette_x_min)
        self.pipette_x_max=median(pipette_x_max)
        self.baseline_pos=median(baseline_pos)
            
        print "training finished:"
        print " pipette_x_min:", self.pipette_x_min, "of", len(pipette_x_min)
        print " pipette_x_max:", self.pipette_x_max, "of", len(pipette_x_max)
        print " baseline_pos:", self.baseline_pos, "of", len(baseline_pos)


    
    

    
    def __call__(self, data, paintPic=True):

        #gray = cv2.cvtColor(data[self.inp_ch[0]], cv2.COLOR_BGR2GRAY) # convert to grayscale
        gray = data[self.inp_ch[0]]

        edges = np.zeros(np.shape(gray), dtype=np.uint8)
#        thres = np.zeros(np.shape(gray), dtype=np.uint8)
        
        #edges = cv2.cvtColor(data[self.inp_ch[0]], cv2.COLOR_BGR2GRAY)
        #cont = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
#        cont2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        #cont3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
#        lineimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

#    /---- get more contrast ----
        gray = np.uint8(np.clip(np.uint32(gray) * 1.1, 0, 255))
#        th = histogram(gray)[1]        
        #print th
#        thres = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)[1]
#    \------end contrast



#    /---- canny edge filtering ----
        edges = cv2.Canny(gray,self.canny_low_threshold,self.canny_hi_threshold, edges, 3, L2gradient=True) # low_threshold*3 for high_treshold is recommended by canny

        #mix1 = cv2.add(gray, edges) #construct red channel
        #mix2 = cv2.subtract(gray, edges) # constuct blue, green channel
        #cont3 = cv2.merge([mix2, mix2, mix1])
#    \------finished canny
        
        
        
#    /---- getting contours ----
        contours, hir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#    \------finished with contours
        
        #print np.shape(contours)
        #contours.sort(key=len, reverse=True)
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
        lines = cv2.HoughLinesP(edges,
                                50,
                                np.pi,
                                threshold=self.hough_threshold,
                                minLineLength=self.hough_minLineLength,                                
                                maxLineGap=self.hough_maxLineGap
                                )[0]
        #print lines
        #print "min:", min(lines, key=lambda _: _[0]), "max:", max(lines, key=lambda _: _[0])
        
        pipette_x_min = min(lines, key=lambda _: _[0])[0] - 2 #substract 5 pix for safty
        pipette_x_max = max(lines, key=lambda _: _[0])[0] + 2 #add saftey margin
        
        
        if len(lines)>5:
            print " !! Attention: pipette detection encountered error"
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
        #cv2.drawContours(cont2, sets, 0, (0,0,255), 0)
        #cv2.drawContours(cont2, sets, 1, (0,255,0), 0)

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
        
        print max_x, y_at_max_x
        print max_indices


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

        print min_x, y_at_min_x
        print min_indices

        #check if this point is a corner (then its index isnt the first one)
        #otherwise it isn't reliable
        # TODO: make this more efficient...
        
        if len(min_indices) < 1 and len(max_indices) < 1:
            # didn't found an extremum on either side
            print "!! critical error in baseline finding..."
#            raise RuntimeError #TODO: add better errorhandling...
            baseline_pos = self.baseline

            
        elif len(min_indices) > 0 and min_indices[0] <= 5 and len(max_indices) > 0 and max_indices[0] <= 5:
            # if extremal ponts are found, but they are from the first few points
            # of the contour, then they are not really edges:
            # use the previous baseline
            print "!! error: no baseline found at all, using previous"
            baseline_pos = self.baseline
        
        elif len(min_indices) > 0 and min_indices[0] <= 5 and len(max_indices) > 0 and max_indices[0] > 5:
            # left side (min) is not reliable, only use right side
            print '! use only right side for baseline'
            baseline_pos = np.int(sum(y_at_max_x)/len(y_at_max_x))

        elif len(max_indices) > 0 and max_indices[0] <= 5 and len(min_indices) > 0 and min_indices[0] > 5:
            # right side (max) is not reliable, only use left side
            print '! use only left side for baseline'
            baseline_pos = np.int(sum(y_at_min_x)/len(y_at_min_x))

        else:
            baseline_pos = np.int((sum(y_at_max_x)+sum(y_at_min_x))/(len(y_at_max_x)+len(y_at_min_x)))

        print 'baseline (old):', baseline_pos, self.baseline
        #if baseline makes a sudden jump, ignore it and use previous, else sve it
        if abs(baseline_pos - self.baseline) > 20:
            baseline_pos = self.baseline
        else:
            self.baseline = baseline_pos
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
        _root = [0,0]
        _poly = [0,0]
        
        for i in [0,1]:
            if len(sets[i]) != 0:
                x = sets[i][:,0,0]
                y = [flip(y) for y in sets[i][:,0,1]]
                z, residuals, rank, singular_values, rcond = np.polyfit(x, y, 5, full=True)
                print "res:", residuals/len(x)
                #print z
                poly = np.poly1d(z)
                _poly[i]=poly
                z2 = z.copy()
                z2[-1] -= baseline_pos          
                #print z2
                shift = np.poly1d(z2)
                roots = np.roots(shift)
                
                #print roots
                root=np.Inf #init to not a number

                if i==0: #left side
                    x_max = max(np.real(x))
                    roots = filter(lambda _x: np.isreal(_x) and _x>0 and _x<x_max, roots)
                    if len(roots)>0: root = np.int(np.real(max(roots)))
                else: #right side
                    x_min = min(np.real(x))
                    roots = filter(lambda _x: np.isreal(_x) and _x>x_min and _x<1280, roots)
                    if len(roots)>0: root = np.int(np.real(min(roots)))
                
                if not root==np.Inf:
                    deriv = poly.deriv()
                    slope = deriv(root)
                    angle[i] = abs(np.arctan(slope))*180/np.pi
                    _root[i] = root                    
                    
        

#    \--------end fit

        
        
        #return [color] #return pictre with colored boundaries from canny edge detection 
        #return [cont] #return the pic with found contours colored
        #return [lineimg] # return the pictre with the pipette markers from hough line detetction
        #return [cont2] # the connected contours, split in left and right side of pipette
        
        
        
        
        
        if paintPic == True:
            #create pic
            cont3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            #canny edge filter
            mix1 = cv2.add(gray, edges) #construct red channel
            mix2 = cv2.subtract(gray, edges) # constuct blue, green channel
            cont3 = cv2.merge([mix2, mix2, mix1])
            
            #adding contours to pic
            greenshades = [255, 128, 64, 32, 192, 148, 50] + [255]*10
            for i, c in enumerate(contours):
                linecolor  = (0, greenshades[i], 0)#rnd.randint(8,15)*16, 0) #shades of green
                cv2.drawContours(cont3, contours, i, linecolor, 3)
            
            #draw the hough lines (pipette detection)
            for i, l in enumerate(lines):
                #print i, l
                x0, y0, x1, y1 = l
                cv2.line(cont3, (x0, 0), (x1, 1024), (39, 127, 255), 1, 8)
                
            #draw the baseline
            cv2.line(cont3, (1, baseline_pos), (1279, baseline_pos), (0,255,255), 1)

            #draw the fitted poly and the angle
            for i in [0,1]:
                deriv = _poly[i].deriv()
                slope = deriv(_root[i])
                fitline = np.poly1d([slope, _poly[i](root)-slope*_root[i]])
                
                xp = range(1,1279)
                yp = np.int32(np.clip(_poly[i](xp),0,1023))
                pnts = np.array([np.column_stack((xp, yp))])
                
                cv2.polylines(cont3, pnts, False, (255,255*i,0), 1)
                
                dx = 200
                cv2.line(cont3,
                         (_root[i]-dx, int(fitline(_root[i]-dx))),
                         (_root[i]+dx, int(fitline(_root[i]+dx))),
                         (0,0,255), 1)
               
            self.lastpic = cont3
            
        
        
        
        return [angle]
        
        



def histogram(picture, channels=[0]):
    # get and display histogram
    hist = cv2.calcHist( [picture], channels, None, [256], [0, 255] )
    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX);
    #print hist
    bin_count = hist.shape[0]
    #bin_w = 2
    #bin_max_h = 200
    #img = np.ones((int(bin_max_h*1.1), bin_count*bin_w, 3), np.uint8)*[70,255,255]*255 #last list is background color

    #print hist
    for i in xrange(bin_count):
        val = hist[i]
        if val==1: hist_max = i #find the size and the pos of the max
        #h = int(val*bin_max_h)
        #print h
        #cv2.rectangle(img, (i*bin_w+2, int(bin_max_h*1.1)), ((i+1)*bin_w-2, int(bin_max_h*1.1)-h), [int(255*255.0*i/bin_count)]*3, -1)
    #img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    #cv2.imshow('hist', img)       

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