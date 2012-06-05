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
#import random as rnd
import sys
from collections import deque

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
        
        
        self.contrast_adj = 1.1 #1.1 #simple factor for getting more contrast in picture
        self.bright_adj = 10
        
        self.canny_low_threshold = 50
        self.canny_hi_threshold = 50*7
        
        self.hough_threshold=30
        self.hough_minLineLength=30
        self.hough_maxLineGap=20

        #how cloose can contour points be to the pipette, before being ignored..
        self.pip_offset = 20     #was 30 for run 1   


        self.fit_small_closeness = 50 # for the fitting of small angle, points how close to baseline are considered (in px)         


        self.baseline = 377

        self.smooth_over = 5 #smooths (mean, median) over the last x frames
        
        self.queue = deque(maxlen=self.smooth_over)

    def train(self, imgs):
        
        print "wrkEdgeFit: Training the worker with", len(imgs), "images"
        
        pipette_x_min=[]
        pipette_x_max=[]
        baseline_pos=[]
        
        sys.stdout.write('  [')
        for i in range(len(imgs)):
            sys.stdout.write('.')
        sys.stdout.write(']')
        for i in range(len(imgs)+1):
            sys.stdout.write('\b')
        sys.stdout.flush()
        
        
        for i, img in enumerate(imgs):
            sys.stdout.write('*')
            sys.stdout.flush()

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
        
                #print tmp_p_min, tmp_p_max
                
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
    
            
            
        sys.stdout.write('\n')
        sys.stdout.flush()   
        ave_pipette_x_min= sum(pipette_x_min)/len(pipette_x_min)
        ave_pipette_x_max= sum(pipette_x_max)/len(pipette_x_max)
        self.baseline_pos= sum(baseline_pos)/len(baseline_pos)

        #print "min"
        #for i in pipette_x_min:
        #    print i
        #print 'max'
        #for i in pipette_x_max:
        #    print i
        
        # filter out all extrem values (far to much on the right/left side)
        chosen = []
        for val in pipette_x_min:
            if val > ave_pipette_x_min-20:
                chosen.append(val)
        self.pipette_x_min= int(median(chosen))    


        chosen = []
        for val in pipette_x_max:
            if val < ave_pipette_x_max+20:
                chosen.append(val)
        self.pipette_x_max= int(median(chosen))            
#median mode
        #self.pipette_x_min= int(median(pipette_x_min))
        #self.pipette_x_max= int(median(pipette_x_max))
        #self.baseline_pos= int(median(baseline_pos))
        
        print "training finished:"
        print " pipette_x_min:", self.pipette_x_min, "of", len(pipette_x_min)
        print " pipette_x_max:", self.pipette_x_max, "of", len(pipette_x_max)
        print " baseline_pos:", self.baseline_pos, "of", len(baseline_pos)


    
    

    
    def __call__(self, data, saveImg=True):
        
        self.saveImg = saveImg
        
        angle1 = h.AngleMeasurement();
        angle2 = h.AngleMeasurement();
        angle3 = h.AngleMeasurement();


        gray = data[self.inp_ch[0]]
        edges = np.zeros(np.shape(gray), dtype=np.uint8)


#    /---- get more contrast ----
        gray = np.uint8(np.clip(np.uint32(gray) * self.contrast_adj + self.bright_adj, 0, 255))
#    \------end contrast



#    /---- canny edge filtering ----
        edges = cv2.Canny(gray,self.canny_low_threshold,self.canny_hi_threshold, edges, 3, L2gradient=True) # low_threshold*3 for high_treshold is recommended by canny
#    \------finished canny
        
        
        
#    /---- getting contours ----
        contours, hir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#    \------finished with contours
        
    

#    /------- distribute the found countour pixels to 2 sets of interessting points, left and right side
        # delete the part in the middle (pipette)


        
        set_l = []
        set_r = [] 
        for contour in contours:
            for points in contour:
                for point in points:
                    #print np.shape(point), len(point), type(point)
                    if point[0]<self.pipette_x_min-self.pip_offset:
                        set_l.append(np.array([point]))
                    elif point[0]>self.pipette_x_max+self.pip_offset:
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

        #_root = [0,0]
        #_poly = [0,0]
        
        #left and right side
        for i in [0,1]:
            if len(sets[i]) != 0:
                x = np.array(sets[i][:,0,0])
                y = np.array([flip(y) for y in sets[i][:,0,1]])

                #########################
                # 1. way to determine angle: (regular case)
                #   fit polynomial 5th degree to points, upright coorinate system

                z, residuals, rank, singular_values, rcond = np.polyfit(x, y, 5, full=True)
                #print "res:", residuals/len(x)
                #print z
                if len(residuals)>0:
                    angle1.residuals[i] = (residuals/len(x))[0]
                else:
                    angle1.residuals[i] = -1
                
                #print z
                poly = np.poly1d(z)
                angle1.func[i]=poly
                
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
                    angle1.angle[i] = abs(np.arctan(slope))*180/np.pi                    
                    angle1.root[i] = root
                    
                    
                #########################
                # 2. way to determine angle: (small angles)
                #   fit straight line to nearest points, upright coorinate system   
                  
                
                sel = y-self.baseline_pos < self.fit_small_closeness                
                if sum(sel)>10: #if there are 10 pixels or more in the selection, take those....
                    yc = y[sel]
                    xc = x[sel]
                else: #else just take the first 50 points or less
                    yc = y[0:min(50,len(y))]
                    xc = x[0:min(50,len(x))]

             
                
                z, residuals, rank, singular_values, rcond = np.polyfit(xc, yc, 1, full=True)
                #print "res:", residuals/len(x)
                #print z
                if len(residuals)>0:
                    angle2.residuals[i] = (residuals/len(xc))[0]
                else:
                    angle2.residuals[i] = -1
                
                poly2 = np.poly1d(z)
                angle2.func[i]=poly2
                #roots = np.roots(poly2-self.baseline_pos)
                #if len(roots)>1:
                #    print 'len roots >1 in 2'
                #    root = roots[-1]
                #else:
                #    root = roots[0]
                angle2.root[i] = int(np.roots(poly2-self.baseline_pos)[0])
                angle2.angle[i] = abs(np.arctan(poly2[1]))*180/np.pi
                
                
                #########################
                # 3. way to determine angle: (huge angles close to 90)
                #   fit straight line to nearest points, y=x mirrored coorinate system
                
                #self.fit_small_closeness = 50 # for the fitting of small angle, points how close to baseline are considered (in px)           
                
                sel = y-self.baseline_pos < self.fit_small_closeness                
                if sum(sel)>10: #if there are 10 pixels or more in the selection, take those....
                    xc = y[sel]  # and points are mirrored x=y...
                    yc = x[sel]
                else: #else just take the first 50 points or less
                    xc = y[0:min(50,len(y))]
                    yc = x[0:min(50,len(x))]

             
                
                z, residuals, rank, singular_values, rcond = np.polyfit(xc, yc, 1, full=True)
                #print "res:", residuals/len(x)
                #print z
                if len(residuals)>0:
                    angle3.residuals[i] = (residuals/len(xc))[0]
                else:
                    angle3.residuals[i] = -1
                
                invpoly = np.poly1d(z)
                poly = np.poly1d([1./z[0], -z[1]/z[0]])
                angle3.func[i]=poly
                angle3.root[i] = int(invpoly(self.baseline_pos))
                angle3.angle[i] = abs(np.arctan(poly[1]))*180/np.pi                
                

#    \--------end fit



#    /--------choose best fit

        res = h.Result()
        res.angle = h.AngleMeasurement()
        res.angle1 = angle1
        res.angle2 = angle2
        res.angle3 = angle3
        res.chosen = 0
        res.fNr = data[0]

        angarr = [angle1, angle2, angle3]        
        
        #sel = [[True, True], [True, True], [True, True]]



            
            
        for i in [0,1]:
            ang_av = np.average([ang.angle[i] for ang in angarr if not np.isnan(ang.root[i])])
        
            #TODO: make this better.. maybe use something like a rating system
            ch = 1
            if ang_av > 75:
                ch = 3
            elif ang_av < 45:
                ch = 2
                
            if np.isnan(angarr[ch-1].root[i]):
                ch = (ch%3)+1 #if this is nan, switch to next fit TODO: make a better choice...
            
            if angarr[ch-1].residuals[i]>20:
                saveImg = True
            
            res.angle.angle[i] = angarr[ch-1].angle[i]
            res.angle.func[i] = angarr[ch-1].func[i]
            res.angle.residuals[i] = angarr[ch-1].residuals[i]
            res.angle.root[i] = angarr[ch-1].root[i]
            
            res.chosen += ch*10**(1-i) #linke wahl an zehnerstelle, rechte wahl an einer stelle


        rt_av = np.average([ang.root[i] for ang in angarr if not np.isnan(ang.root[i])])
        rt_d = np.sum([(ang.root[i]-rt_av)**2 for ang in angarr if not np.isnan(ang.root[i])])

        #print rt_av, rt_d
        if rt_d > 20:
            self.saveImg = True            
        
        
        mean_angle = h.AngleMeasurement()
        median_angle = h.AngleMeasurement()
        
        self.queue.append(res.angle)
        
        def medi(y):
            z = len(y)
            if not z%2:
                return (y[(z/2)-1] + y[z/2]) / 2.
            return y[z/2]


        for i in [0,1]:
            #print 'gogo', i
            v_ang = []
            v_root = []
            v_res = []
            for ang in self.queue:
                v_ang.append(ang.angle[i])
                v_root.append(ang.root[i])
                v_res.append(ang.residuals[i])
            
            v_ang.sort()              
            v_root.sort()
            v_res.sort()
            
            mean_angle.angle[i] = sum(v_ang) / len(v_ang)
            mean_angle.root[i] = sum(v_root) / len(v_root)
            mean_angle.residuals[i] = sum(v_res) / len(v_res)
            
            median_angle.angle[i] = medi(v_ang)
            median_angle.root[i] = medi(v_root)
            median_angle.residuals[i] = medi(v_res)

        res.mean_angle = mean_angle
        res.median_angle = median_angle

#    \--------end choose



#    /-------------- paint image
        
        if self.saveImg == True:
            #create pic
            cont3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            #canny edge filter
            mix1 = cv2.add(gray, edges) #construct red channel
            mix2 = cv2.subtract(gray, edges) # constuct blue, green channel
            cont3 = cv2.merge([mix2, mix2, mix1])
            
            #adding contours to pic
            #greenshades = [255, 128, 64, 32, 192, 148, 50] + [255]*64
            for i, c in enumerate(contours):
            #    linecolor  = (0, greenshades[i], 0)#rnd.randint(8,15)*16, 0) #shades of green
            #    cv2.drawContours(cont3, contours, i, linecolor, 3)
                 cv2.drawContours(cont3, contours, i, (0,200,0), 3)
            
            #draw the hough lines (pipette detection)
            cv2.line(cont3, (self.pipette_x_max, 0), (self.pipette_x_max, 1024), (39, 127, 255), 1, 8)
            cv2.line(cont3, (self.pipette_x_min, 0), (self.pipette_x_min, 1024), (39, 127, 255), 1, 8)
            cv2.line(cont3, (self.pipette_x_max+self.pip_offset, 0), (self.pipette_x_max+self.pip_offset, 1024), (39, 127, 255), 1, 8)
            cv2.line(cont3, (self.pipette_x_min-self.pip_offset, 0), (self.pipette_x_min-self.pip_offset, 1024), (60, 160, 255), 1, 8)
                
            #draw the baseline
            cv2.line(cont3, (1, self.baseline_pos), (1279, self.baseline_pos), (0,255,255), 1)
            # draw the threshold line
            cv2.line(cont3, (1, self.baseline_pos+self.fit_small_closeness), (1279, self.baseline_pos+self.fit_small_closeness), (0,128,128), 1)

            #draw the fitted poly and the angle
            for j in [0,1,2,3]:
                
                if j==0:
                    ang=angle1
                    col = (255,0,0)
                elif j==1:
                    ang=angle2
                    col = (255,80,0)
                elif j==2:
                    ang=angle3
                    col = (255,255,0)
                elif j==3: #the chosen one
                    ang=res.angle
                    col = (0,0,255)
                    
                for i in [0,1]:
                    root = ang.root[i]
                    poly = ang.func[i]
                    #print poly
                    #print root
                    #print '-----'
                    #print angle1.angle, angle1.func
                    #print angle2.angle, angle2.func
                    
                    if root != np.NaN and root != np.Inf and root !=0 and len(sets[i]) != 0:
                        deriv = poly.deriv()
                        slope = deriv(root)
                        fitline = np.poly1d([slope, poly(root)-slope*root])
                        #print "fitline", fitline
                        #print "root:",i, _root[i]
                        
                        if j<3:
                            xp = range(1,1279)
                            yp = np.int32(np.clip(poly(xp),0,1023))
                            pnts = np.array([np.column_stack((xp, yp))])
                            
                            cv2.polylines(cont3, pnts, False, col, 1)
                        
                        
                        
                        #draw the angle
                        dx = 100 #half of the line length
    
                        if root>0 and root<2000 and fitline(root-dx) >0 and fitline(root-dx) <2000 and fitline(root+dx) >0 and fitline(root+dx) <2000:
                            #if data[0] > 680:
                            #    print 'debug:', root-dx, fitline(root-dx), root+dx, fitline(root+dx), col
                            y1 = fitline(root-dx)
                            y2 = fitline(root+dx)
                            #y1 = y1 if y1 > 0 else 0
                            #y1 = y1 if y1 < 1500 else 1500
                            #y2 = y2 if y2 > 0 else 0
                            #y2 = y2 if y2 < 1500 else 1500                            
                            
                            
                            cv2.line(cont3,
                                     (root-dx, int(y1)),
                                     (root+dx, int(y2)),
                                     col, 1)
            
            cv2.putText(cont3, 'f: %4i t: %6.2fs sel:%1i angL: %4.1f angR: %4.1f'%(data[0], data[2]/1000., res.chosen, res.angle.angle[0], res.angle.angle[1]), (10,30), cv2.FONT_HERSHEY_PLAIN,1.2,(200,200,200))
            self.lastpic = cont3
        
        return [res]
        
        



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

