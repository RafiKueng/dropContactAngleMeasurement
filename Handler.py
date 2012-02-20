# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 17:50:47 2012

@author: rafik
"""

import multiprocessing as mproc
import heapq
import time

class InputHandler(mproc.Process):
    """handels the input plugins, feeds the pipes
        
    will be spawn once    
    """   

    def __init__(self, datapipes, readers):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.datapipes = datapipes
        self.readers = readers
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        self.readers[0].setup('bin/testfile.mpg')

        #time.sleep(5)
        
        for i in testrange:
            print '---------------------------'
            print '%s: get dataframe %.0f @t: %f' % (self.name, i, time.time())
            data = self.readers[0].getData()
            #time.sleep(3)            
            print '%s: send dataframe %.0f to %.0f @t: %f' % (self.name, i, i%2, time.time())
            self.datapipes[i%2].send(data)
            #time.sleep(1)
        
        
        #we're finished, sending signals to workers to close connection
        #time.sleep(10)
        print '%s: finished, tell workers to shut down @t: %f' % (self.name, time.time())
        for pipe in self.datapipes:
            pipe.send(-1)
        print '%s: stopping @t: %f' % (self.name, time.time())
        
       

class WorkerHandler(mproc.Process):
    """handels the processing of the data
    
    can possibly be spawn multiple times (depening on no of cpu cores)    
    """     
    
    def __init__(self, datapipe, result_queue, workers):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.datapipe = datapipe
        self.result_queue = result_queue
        self.workers = workers
        
    def setup(self, *args):
        print '%s: setup @t: %f' % (self.name, time.time())
        for i, worker in enumerate(self.workers):
            worker.setup(args[0])
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        i=0
        
        #for i in testrange:
        while True:
            i=+1
            print '%s: waiting for data %.0f @t: %f' % (self.name, i, time.time())
            data = self.datapipe.recv() #waits till it gets something
            print '%s: got data @t: %f' % (self.name, time.time())
            if data == -1: break
            
            data = self.workers[0].procData(data)        
            print '%s: processed data, put in queue @t: %f' % (self.name, time.time())
            
            #print time.clock()
            self.result_queue.put(data)
        
        #time.sleep(5)
        self.result_queue.put([-1])
        print '%s: stopping @t: %f' % (self.name, time.time())
    
        
#    def __getstate__(self):
#        return 'bla'
#        
#    def __setstate__(self, str):
#        pass



        
class OutputHandler(mproc.Process):
    """handels the output (display, saving) of the data
    
    will be spawn once    
    """     
    
    def __init__(self, result_queue, writers):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.result_queue = result_queue
        self.writers = writers
        #self.writers[0].init()
        self.nrunningworkers = 2 #TODO: get this from super
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        self.writers[0].setup()
        #datacounter = 0
        framecounter = 1
        buffer = [] #list used as heap queue (priority queue)
        #heapq.heappush(buffer, (10000000, []))  #TODO this is only a workaround to prevent in "while buffer[0][0]..." invalid access (there is always at least one bigger than all others in the pipe)
        
        #for i in testrange:
        while True:
            #time.sleep(0.2)
            print '%s: waiting for data @t: %f' % (self.name, time.time())
            data = self.result_queue.get()
            
            #check if quit
            #TODO: maybe do this better later, check if all worker not living (using signals) and queue empty            
            if data[0] == -1:
                self.nrunningworkers -= 1
                if self.nrunningworkers == 0:
                    break
                continue
            #time.sleep(0.5)
            print '%s: got dataframe nr %.0f from queue @t: %f' % (self.name, data[0], time.time())
            
#            for writer in self.writers:
#                writer.writeData(data)            
            
            if data[0] == framecounter:
                print '%s: on time, write it @t: %f' % (self.name, time.time())
                framecounter += 1
                for writer in self.writers:
                    writer.writeData(data)
            else:
                print '%s: ahead of time, write it to buffer @t: %f' % (self.name, time.time())
                #print 'data1', data
                heapq.heappush(buffer, (data[0], data)) #makes already sure the elements in heapq are sorted!!
                print '   len buffer:', len(buffer), buffer[0][0], framecounter, data[0]
            while (len(buffer) > 0 and (buffer[0][0] == framecounter or data[0] >= framecounter+25)): # as soon as right frame is here OR more than 1 sec (25 frames) behind, continue painting
                _, data = heapq.heappop(buffer)
                #print 'data2', data
                framecounter += 1
                for writer in self.writers:
                    writer.writeData(data)
                    pass

        print '%s: stopping @t: %f' % (self.name, time.time())
        
#    def __getstate__(self):
#        return 'bla'
#        
#    def __setstate__(self, str):
#        pass