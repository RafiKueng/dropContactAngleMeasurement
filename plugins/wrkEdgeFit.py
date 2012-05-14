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
        
    
    def config(self):
        
        
        self.contrast_adj = 1.1 #simple factor for getting more contrast in picture

        self.canny_low_threshold = 50
        self.canny_hi_threshold = 50*7
        
        self.hough_threshold=30
        self.hough_minLineLength=30
        self.hough_maxLineGap=20



        self.baseline = 377


    def train(self, imgs):
        
        print "training with", len(imgs), "images"
        
        pipette_x_min=[]
        pipette_x_max=[]
        baseline_pos=[]
        
        
        for i, img in enumerate(imgs):
            print i
            gray = np.uint8(np.clip(np.uint32(img) * 1.1, 0, 255))
            edges = np.zeros(np.shape(gray), dtype=np.uint8)
            edges = cv2.Canny(gray,self.canny_low_threshold,self.canny_hi_threshold, edges, 3, L2gradient=True)
            contours, hir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            hl = cv2.HoughLinesP(edges,
                                    50,
                                    np.pi,
                                    threshold=self.hough_threshold,
                                    minLineLength=self.hough_minLineLength,                                
                                    maxLineGap=self.hough_maxLineGap
                                    )
                                    
            if hl!=None:
                lines = hl[0]
                #print lines
                #print "min:", min(lines, key=lambda _: _[0]), "max:", max(lines, key=lambda _: _[0])
    
                tmp_p_min = min(lines, key=lambda _: _[0])[0]
                tmp_p_max = max(lines, key=lambda _: _[0])[0]
                
                pipette_x_min.append(tmp_p_min)
                pipette_x_max.append(tmp_p_max)
        
        
                set_l = []
                set_r = [] 
                for contour in contours:
                    for points in contour:
                        for point in points:
                            #print np.shape(point), len(point), type(point)
                            if point[0]<tmp_p_min+5:
                                set_l.append(np.array([point]))
                            elif point[0]>tmp_p_max+5:
                                set_r.append(np.array([point]))
                
                set_l.sort(key=lambda _: _[0][1])
                set_r.sort(key=lambda _: _[0][1])
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
                    #print '! use only right side for baseline'
                    baseline_pos.append(np.int(sum(y_at_max_x)/len(y_at_max_x)))
        
                elif len(max_indices) > 0 and max_indices[0] <= 5 and len(min_indices) > 0 and min_indices[0] > 5:
                    # right side (max) is not reliable, only use left side
                    #print '! use only left side for baseline'
                    baseline_pos.append(np.int(sum(y_at_min_x)/len(y_at_min_x)))
        
                else:
                    baseline_pos.append(np.int((sum(y_at_max_x)+sum(y_at_min_x))/(len(y_at_max_x)+len(y_at_min_x))))
    
            
            
            
        self.pipette_x_min= sum(pipette_x_min)/len(pipette_x_min)
        self.pipette_x_max= sum(pipette_x_max)/len(pipette_x_max)
        self.baseline_pos= sum(baseline_pos)/len(baseline_pos)

#median mode
        #self.pipette_x_min= int(median(pipette_x_min))
        #self.pipette_x_max= int(median(pipette_x_max))
        #self.baseline_pos= int(median(baseline_pos))
            
        print "training finished:"
        print " pipette_x_min:", self.pipette_x_min, "of", len(pipette_x_min)
        print " pipette_x_max:", self.pipette_x_max, "of", len(pipette_x_max)
        print " baseline_pos:", self.baseline_pos, "of", len(baseline_pos)


    
    

    
    def __call__(self, data, paintPic=True):
        
        angle = h.AngleMeasurement();

        gray = data[self.inp_ch[0]]
        edges = np.zeros(np.shape(gray), dtype=np.uint8)


#    /---- get more contrast ----
        gray = np.uint8(np.clip(np.uint32(gray) * 1.1, 0, 255))
#    \------end contrast



#    /---- canny edge filtering ----
        edges = cv2.Canny(gray,self.canny_low_threshold,self.canny_hi_threshold, edges, 3, L2gradient=True) # low_threshold*3 for high_treshold is recommended by canny
#    \------finished canny
        
        
        
#    /---- getting contours ----
        contours, hir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#    \------finished with contours
        
    

#    /------- distribute the found countour pixels to 2 sets of interessting points, left and right side
        set_l = []
        set_r = [] 
        for contour in contours:
            for points in contour:
                for point in points:
                    #print np.shape(point), len(point), type(point)
                    if point[0]<self.pipette_x_min-30:
                        set_l.append(np.array([point]))
                    elif point[0]>self.pipette_x_max+30:
                        set_r.append(np.array([point]))
        
        set_l.sort(key=lambda _: _[0][1])
        set_r.sort(key=lambda _: _[0][1])
        sets = np.array([np.array(set_l), np.array(set_r)])
#    \--------end distribute points 

        
        
#    /------- fitting a poly to the contour
        def flip(x):
            if x < self.baseline_pos:
                return 2*self.baseline_pos - x
            else:
                return x

        #angle = [0.0,0.0]
        _root = [0,0]
        _poly = [0,0]
        
        for i in [0,1]:
            if len(sets[i]) != 0:
                x = sets[i][:,0,0]
                y = [flip(y) for y in sets[i][:,0,1]]
                z, residuals, rank, singular_values, rcond = np.polyfit(x, y, 5, full=True)
                #print "res:", residuals/len(x)
                #print z
                if len(residuals)>0:
                    angle.residuals[i] = (residuals/len(x))[0]
                else:
                    angle.residuals[i] = -1
                
                #print z
                poly = np.poly1d(z)
                _poly[i]=poly
                
                #print "poly:"
                #print poly                 
                
                z2 = z.copy()
                z2[-1] -= self.baseline_pos          
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
                    angle.angle[i] = abs(np.arctan(slope))*180/np.pi                    
                    _root[i] = root
                    angle.root[i] = root

#    \--------end fit
    
        
        if paintPic == True:
            #create pic
            cont3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            #canny edge filter
            mix1 = cv2.add(gray, edges) #construct red channel
            mix2 = cv2.subtract(gray, edges) # constuct blue, green channel
            cont3 = cv2.merge([mix2, mix2, mix1])
            
            #adding contours to pic
            greenshades = [255, 128, 64, 32, 192, 148, 50] + [255]*64
            for i, c in enumerate(contours):
                linecolor  = (0, greenshades[i], 0)#rnd.randint(8,15)*16, 0) #shades of green
                cv2.drawContours(cont3, contours, i, linecolor, 3)
            
            #draw the hough lines (pipette detection)
            cv2.line(cont3, (self.pipette_x_max, 0), (self.pipette_x_max, 1024), (39, 127, 255), 1, 8)
            cv2.line(cont3, (self.pipette_x_min, 0), (self.pipette_x_min, 1024), (39, 127, 255), 1, 8)
                
            #draw the baseline
            cv2.line(cont3, (1, self.baseline_pos), (1279, self.baseline_pos), (0,255,255), 1)

            #draw the fitted poly and the angle
            for i in [0,1]:
                if _root[i] != np.NaN and _root[i] != np.Inf and _root[i] !=0 and len(sets[i]) != 0:
                    deriv = _poly[i].deriv()
                    slope = deriv(_root[i])
                    fitline = np.poly1d([slope, _poly[i](_root[i])-slope*_root[i]])
                    #print "fitline", fitline
                    #print "root:",i, _root[i]
                    
                    xp = range(1,1279)
                    yp = np.int32(np.clip(_poly[i](xp),0,1023))
                    pnts = np.array([np.column_stack((xp, yp))])
                    
                    cv2.polylines(cont3, pnts, False, (255,255*i,0), 1)
                    
                    dx = 100

              

                    if _root[i]>0 and _root[i]<2000 and fitline(_root[i]) >0 and fitline(_root[i]) <2000:
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




if __name__ == '__main__':
    #getData()
    pass

