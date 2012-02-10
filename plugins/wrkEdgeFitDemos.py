# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 15:17:16 2012

@author: rafik
"""

from Abstract import wrkAbstract

import numpy as np
import cv2
import random as rnd
#import time


class wrkEdgeFit(wrkAbstract):

    def __init__(self):
        pass
    
    def setup(self):
        pass
    
    def procData(self, data):
        #print data[1]
        #print max(data[1]), min(data[1])
        gray = cv2.cvtColor(data[1], cv2.COLOR_BGR2GRAY) # convert to grayscale
        edges = cv2.cvtColor(data[1], cv2.COLOR_BGR2GRAY)
        cont = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        #cv2.multiply(gray, 2, gray)    


#    /---- doing threshold filtering ----
        histmax, thres = histogram(gray)
        bw = cv2.threshold(gray, thres, 255, cv2.THRESH_BINARY)[1]
        bw = cv2.medianBlur(bw, 13)
#    \------finished with contours



#    /---- canny edge filtering ----
        low_threshold = 100
        edges = cv2.Canny(gray,low_threshold,low_threshold*3, edges, 3) # low_threshold*3 for high_treshold is recommended by canny

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
        
       
        #return color
        return cont        


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
    print hist_max, thres
    return hist_max, thres




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