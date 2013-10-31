import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.wrkEdgeFit as wrkEdge
import plugins.outSimpleDisplay as outSD
import plugins.outSimpleCSVWriter as outCSV

#initalise plugins
inp = inpSFG.inpSimpleFrameGrabber()
wrk2 = wrkEdge.wrkEdgeFit()
out3 = outCSV.outSimpleCSVWriter()
outDisp = outSD.outSimpleDisplay()

# setup input data tokens for plugins
inp.setup()
wrk2.setup([1])
out3.setup([0,2])
outDisp.setup([0,1])

#configure plugins
inp.config("move.avi")
wrk2.config()
out3.config("csvfile.csv")
outIWrt.config("path/for/images")

# trian the worker with 64 images
trainimg = []
for x in range(64):
    img = inp.getFrameNr(inp.nFrames//64*x)[1]
    trainimg.append(img)
wrk2.train(trainimg)

# reset the reader
inp.setPos(0)

# execute the analysis for the whole movie
for i in range(inp.nFrames):
    data = []
    data.extend(inp())

    # do the work
    data.extend(wrk2(data)) #save each 25th frame

    #output
    if i%25==0: #save each 25th frame
        outIWrt([data[0],wrk2.lastpic])
    out3(data) #write to csv

# clean up    
inp.finish()
wrk2.finish()
out3.finish()