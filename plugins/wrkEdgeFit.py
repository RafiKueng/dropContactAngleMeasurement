# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 15:17:16 2012

@author: rafik
"""

from Abstract import wrkAbstract

from numpy import array, zeros, shape
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
        
        low_threshold = 70
        edges = cv2.Canny(gray,low_threshold,low_threshold*3, edges, 3) # low_threshold*3 for high_treshold is recommended by canny

#    /---- getting contours ----
        contours, hir = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i, c in enumerate(contours):
            
            color  = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
            cv2.drawContours(cont, contours, i, color, 5)
#    \------finished with contours
        
        mix1 = cv2.add(gray, edges) #construct red channel
        mix2 = cv2.subtract(gray, edges) # constuct blue, green channel
        color = cv2.merge([mix2, mix2, mix1])
        
        #return color
        return cont        


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